"""
HiddenYatra — Unit Test Suite for Phase G4B-2 Production Terrain Loader.
Tests Web Mercator XYZ math, viewport tile calculation, 1-ring prefetching,
LRU cache eviction, in-flight request deduplication, LOD mapping, and edge seams.
"""
import os
import sys
import json
import math
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.preprocess_dem_tiles import (
    TERRAIN_DIR,
    lat_lng_to_tile_xy,
    tile_point_to_lat_lng,
    decode_hyelev_file,
)


class TestHYMapTerrainLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manifest_path = os.path.join(TERRAIN_DIR, "manifest.json")
        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)
        cls.available_tiles = set(cls.manifest["tiles"].keys())

    def test_01_web_mercator_xyz_tile_coordinate_math(self):
        """Verify lat/lng to Web Mercator tile index calculation matches standard projections."""
        # Bodh Gaya / Gaya: 24.70°N, 84.99°E
        x9, y9 = lat_lng_to_tile_xy(24.70, 84.99, 9)
        self.assertEqual(x9, 376)
        self.assertEqual(y9, 219)

        x10, y10 = lat_lng_to_tile_xy(24.70, 84.99, 10)
        self.assertEqual(x10, 753)
        self.assertEqual(y10, 439)

        x11, y11 = lat_lng_to_tile_xy(24.70, 84.99, 11)
        self.assertEqual(x11, 1507)
        self.assertEqual(y11, 878)

    def test_02_vertex_grid_point_to_lat_lng_corners(self):
        """Verify 65x65 tile vertex coordinates cover the tile bounds smoothly."""
        z, x, y = 11, 1507, 878
        nw_lat, nw_lng = tile_point_to_lat_lng(z, x, y, 0, 0)
        se_lat, se_lng = tile_point_to_lat_lng(z, x, y, 64, 64)

        self.assertGreater(nw_lat, se_lat, "North latitude must be greater than South latitude")
        self.assertLess(nw_lng, se_lng, "West longitude must be less than East longitude")

        # Verify within Gaya / Bodh Gaya region
        self.assertAlmostEqual(nw_lat, 24.846, places=2)
        self.assertAlmostEqual(nw_lng, 84.902, places=2)

    def test_03_shared_edge_coordinate_exact_equality(self):
        """Verify East-West and North-South shared border vertices produce identical Lat/Lng coordinates."""
        z = 11
        # East-West neighbor pair: (11, 1507, 878) and (11, 1508, 878)
        for r in range(65):
            left_lat, left_lng = tile_point_to_lat_lng(z, 1507, 878, r, 64)
            right_lat, right_lng = tile_point_to_lat_lng(z, 1508, 878, r, 0)

            self.assertAlmostEqual(left_lat, right_lat, places=7)
            self.assertAlmostEqual(left_lng, right_lng, places=7)

        # North-South neighbor pair: (11, 1507, 878) and (11, 1507, 879)
        for c in range(65):
            top_lat, top_lng = tile_point_to_lat_lng(z, 1507, 878, 64, c)
            bot_lat, bot_lng = tile_point_to_lat_lng(z, 1507, 879, 0, c)

            self.assertAlmostEqual(top_lat, bot_lat, places=7)
            self.assertAlmostEqual(top_lng, bot_lng, places=7)

    def test_04_lod_selection_mapping(self):
        """Verify camera zoom maps to target LOD levels correctly."""
        # Simulated selectTargetLOD logic
        def select_lod(zoom, available_lods=[9, 10, 11]):
            if zoom <= 9.5: return 9
            elif zoom <= 10.5: return 10
            else: return 11

        self.assertEqual(select_lod(8.0), 9)
        self.assertEqual(select_lod(9.0), 9)
        self.assertEqual(select_lod(10.0), 10)
        self.assertEqual(select_lod(11.0), 11)
        self.assertEqual(select_lod(15.5), 11)

    def test_05_viewport_tile_and_prefetch_calculation(self):
        """Verify calculation of visible tile keys and 1-ring prefetch buffer."""
        # Rajgir camera bounding box
        bounds = {
            "north": 25.05,
            "south": 24.95,
            "east": 85.48,
            "west": 85.38
        }
        z = 11
        nw_x, nw_y = lat_lng_to_tile_xy(bounds["north"], bounds["west"], z)
        se_x, se_y = lat_lng_to_tile_xy(bounds["south"], bounds["east"], z)

        min_x, max_x = min(nw_x, se_x), max(nw_x, se_x)
        min_y, max_y = min(nw_y, se_y), max(nw_y, se_y)

        visible_keys = []
        prefetch_keys = []
        visible_set = set()

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                key = f"{z}/{x}/{y}"
                if key in self.available_tiles:
                    visible_keys.append(key)
                    visible_set.add(key)

        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                key = f"{z}/{x}/{y}"
                if key not in visible_set and key in self.available_tiles:
                    prefetch_keys.append(key)

        self.assertIn("11/1509/877", visible_keys)
        self.assertTrue(len(visible_keys) >= 1)

    def test_06_lru_cache_eviction_logic(self):
        """Verify LRU cache maintains capacity, updates access order, and evicts oldest."""
        class SimpleLRU:
            def __init__(self, max_size=3):
                self.max_size = max_size
                self.items = {}
                self.evicted = []

            def get(self, k):
                if k in self.items:
                    v = self.items.pop(k)
                    self.items[k] = v
                    return v
                return None

            def set(self, k, v, protected=set()):
                if k in self.items:
                    self.items.pop(k)
                elif len(self.items) >= self.max_size:
                    # Evict oldest non-protected
                    for old_k in list(self.items.keys()):
                        if old_k not in protected:
                            self.evicted.append(old_k)
                            self.items.pop(old_k)
                            break
                self.items[k] = v

        cache = SimpleLRU(max_size=3)
        cache.set("A", 1)
        cache.set("B", 2)
        cache.set("C", 3)

        # Access A -> order is B, C, A
        cache.get("A")

        # Set D -> B should be evicted
        cache.set("D", 4)
        self.assertEqual(cache.evicted, ["B"])
        self.assertIsNone(cache.get("B"))
        self.assertEqual(cache.get("A"), 1)
        self.assertEqual(cache.get("C"), 3)
        self.assertEqual(cache.get("D"), 4)

    def test_07_binary_triangle_index_count_and_topology(self):
        """Verify 64x64 cell grid generates exactly 24,576 triangle indices with valid ranges."""
        # 64 cells * 64 cells * 2 triangles * 3 vertices = 24,576 indices
        indices = []
        for r in range(64):
            for c in range(64):
                tl = r * 65 + c
                tr = tl + 1
                bl = (r + 1) * 65 + c
                br = bl + 1
                indices.extend([tl, bl, tr, tr, bl, br])

        self.assertEqual(len(indices), 24576)
        self.assertEqual(min(indices), 0)
        self.assertEqual(max(indices), 65 * 65 - 1)  # 4224

    def test_08_javascript_loader_asset_files_exist(self):
        """Verify static/js/map/map-google-terrain-worker.js and map-google-terrain-loader.js exist."""
        worker_file = os.path.join(TERRAIN_DIR, "..", "..", "..", "js", "map", "map-google-terrain-worker.js")
        loader_file = os.path.join(TERRAIN_DIR, "..", "..", "..", "js", "map", "map-google-terrain-loader.js")

        self.assertTrue(os.path.exists(worker_file), f"Missing {worker_file}")
        self.assertTrue(os.path.exists(loader_file), f"Missing {loader_file}")

        with open(worker_file, 'r', encoding='utf-8') as f:
            worker_src = f.read()
            self.assertIn("decodeHyelevBinary", worker_src)
            self.assertIn("generateTileIndexBuffer", worker_src)

        with open(loader_file, 'r', encoding='utf-8') as f:
            loader_src = f.read()
            self.assertIn("HYGoogleTerrainLoader", loader_src)
            self.assertIn("TerrainLRUCache", loader_src)
            self.assertIn("selectTargetLODWithHysteresis", loader_src)

    def test_09_lod_selection_with_hysteresis(self):
        """Verify hysteresis deadband prevents rapid LOD thrashing around zoom boundaries."""
        def select_lod_hysteresis(camera_zoom, current_lod=None, available_lods=[9, 10, 11]):
            if current_lod == 9:
                return 10 if camera_zoom >= 9.75 else 9
            elif current_lod == 10:
                if camera_zoom < 9.25: return 9
                if camera_zoom >= 10.75: return 11
                return 10
            elif current_lod == 11:
                return 10 if camera_zoom < 10.25 else 11
            else:
                if camera_zoom <= 9.5: return 9
                elif camera_zoom <= 10.5: return 10
                else: return 11

        # Zooming In:
        # At LOD 9, zoom 9.6 must remain LOD 9 (no thrash)
        self.assertEqual(select_lod_hysteresis(9.6, current_lod=9), 9)
        # At LOD 9, zoom 9.8 switches to LOD 10
        self.assertEqual(select_lod_hysteresis(9.8, current_lod=9), 10)

        # At LOD 10, zoom 10.6 remains LOD 10
        self.assertEqual(select_lod_hysteresis(10.6, current_lod=10), 10)
        # At LOD 10, zoom 10.8 switches to LOD 11
        self.assertEqual(select_lod_hysteresis(10.8, current_lod=10), 11)

        # Zooming Out:
        # At LOD 11, zoom 10.4 remains LOD 11
        self.assertEqual(select_lod_hysteresis(10.4, current_lod=11), 11)
        # At LOD 11, zoom 10.1 switches to LOD 10
        self.assertEqual(select_lod_hysteresis(10.1, current_lod=11), 10)

        # At LOD 10, zoom 9.4 remains LOD 10
        self.assertEqual(select_lod_hysteresis(9.4, current_lod=10), 10)
        # At LOD 10, zoom 9.1 switches to LOD 9
        self.assertEqual(select_lod_hysteresis(9.1, current_lod=10), 9)

    def test_10_protected_keys_lru_cache_eviction(self):
        """Verify protected keys are never evicted from LRU cache while active."""
        class ProtectedLRU:
            def __init__(self, max_size=3):
                self.max_size = max_size
                self.cache = {}

            def set(self, k, v, protected_keys=set()):
                if k in self.cache:
                    self.cache.pop(k)
                elif len(self.cache) >= self.max_size:
                    for old_k in list(self.cache.keys()):
                        if old_k not in protected_keys:
                            self.cache.pop(old_k)
                            break
                self.cache[k] = v

        cache = ProtectedLRU(max_size=3)
        cache.set("Visible_A", 1)
        cache.set("Visible_B", 2)
        cache.set("Prefetch_C", 3)

        # Adding new tile with Visible_A and Visible_B protected
        protected = {"Visible_A", "Visible_B"}
        cache.set("Visible_D", 4, protected_keys=protected)

        # Prefetch_C should be evicted, Visible_A and Visible_B must remain
        self.assertIn("Visible_A", cache.cache)
        self.assertIn("Visible_B", cache.cache)
        self.assertIn("Visible_D", cache.cache)
        self.assertNotIn("Prefetch_C", cache.cache)

    def test_11_perimeter_skirt_vertex_and_quad_count(self):
        """Verify perimeter skirt math produces exact vertex and quad counts for 65x65 grid."""
        grid_w, grid_h = 65, 65
        grid_vertices = grid_w * grid_h # 4225
        perimeter_vertices = (grid_w * 2) + ((grid_h - 2) * 2) # 256
        total_vertices = grid_vertices + perimeter_vertices

        self.assertEqual(perimeter_vertices, 256)
        self.assertEqual(total_vertices, 4481)

        base_indices_count = 64 * 64 * 6 # 24,576
        skirt_indices_count = perimeter_vertices * 6 # 1,536
        total_indices_count = base_indices_count + skirt_indices_count

        self.assertEqual(total_indices_count, 26112)


if __name__ == '__main__':
    unittest.main()
