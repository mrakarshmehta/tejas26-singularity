"""
HiddenYatra — Unit Test Suite for Phase G4A Google Custom 3D Terrain POC.
Tests WebGL support detection, 64x64 grid generation, exaggeration scaling,
WebGLOverlayView lifecycle hooks, Three.js integration, and cleanup.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app


class TestHYMapTerrain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['MAP_ENGINE'] = 'google'
        os.environ['GOOGLE_MAPS_API_KEY'] = 'test-terrain-api-key'
        os.environ['GOOGLE_MAPS_MAP_ID'] = 'test-terrain-map-id'

        import importlib
        import config as cfg_mod
        importlib.reload(cfg_mod)

        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def test_terrain_asset_files_exist(self):
        """Verify map-google-terrain.js and map-google-terrain-mesh.js exist on disk."""
        mesh_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain-mesh.js')
        mgr_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain.js')

        self.assertTrue(os.path.exists(mesh_path), f"Missing {mesh_path}")
        self.assertTrue(os.path.exists(mgr_path), f"Missing {mgr_path}")

    def test_explore_template_includes_three_and_terrain_scripts(self):
        """Verify explore_map.html includes Three.js and Google 3D Terrain scripts."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')

        self.assertIn('three.min.js', html)
        self.assertIn('map-google-terrain-mesh.js', html)
        self.assertIn('map-google-terrain.js', html)

    def test_terrain_mesh_factory_exports_and_grid_constants(self):
        """Verify HYGoogleTerrainMeshFactory exports 64x64 grid and bounds for Rajgir Hills."""
        mesh_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain-mesh.js')
        with open(mesh_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('root.HYGoogleTerrainMeshFactory = GoogleTerrainMeshFactory', content)
        self.assertIn('GRID_SIZE = 64', content)
        self.assertIn('minLat: 24.95', content)
        self.assertIn('maxLat: 25.05', content)
        self.assertIn('minLng: 85.38', content)
        self.assertIn('maxLng: 85.48', content)
        self.assertIn('createRajgirTerrainMesh', content)
        self.assertIn('updateExaggeration', content)

    def test_terrain_mesh_hypsometric_tinting_and_normals(self):
        """Verify terrain mesh computes vertex colors and computeVertexNormals."""
        mesh_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain-mesh.js')
        with open(mesh_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('getElevationColor', content)
        self.assertIn('computeVertexNormals', content)
        self.assertIn('vertexColors: true', content)

    def test_terrain_manager_webgl_overlay_view_lifecycle(self):
        """Verify HYGoogleTerrainManager implements all 5 WebGLOverlayView lifecycle hooks."""
        mgr_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain.js')
        with open(mgr_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('root.HYGoogleTerrainManager = GoogleTerrainManager', content)
        self.assertIn('new google.maps.WebGLOverlayView()', content)
        self.assertIn('this.overlay.onAdd', content)
        self.assertIn('this.overlay.onContextRestored', content)
        self.assertIn('this.overlay.onDraw', content)
        self.assertIn('this.overlay.onContextLost', content)
        self.assertIn('this.overlay.onRemove', content)

    def test_terrain_manager_coordinate_transformer_usage(self):
        """Verify terrain manager uses transformer.fromLatLngAltitude for georeferencing."""
        mgr_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain.js')
        with open(mgr_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('transformer.fromLatLngAltitude', content)
        self.assertIn('transformer.getCameraParams', content)
        self.assertIn('resetState()', content)

    def test_terrain_manager_exaggeration_and_controls(self):
        """Verify terrain manager supports dynamic exaggeration and Rajgir camera focus."""
        mgr_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain.js')
        with open(mgr_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('setExaggeration', content)
        self.assertIn('getExaggeration', content)
        self.assertIn('focusRajgir', content)
        self.assertIn('enable()', content)
        self.assertIn('disable()', content)
        self.assertIn('destroy()', content)

    def test_map_modes_google_3d_terrain_integration(self):
        """Verify map-modes.js triggers terrainManager on 3D terrain mode selection in Google mode."""
        modes_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-modes.js')
        with open(modes_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('terrainManager.enable()', content)
        self.assertIn('terrainManager.focusRajgir()', content)
        self.assertIn('terrainManager.disable()', content)

    def test_google_adapter_has_terrain_manager_lifecycle(self):
        """Verify MapGoogleAdapter instantiates and cleans up terrainManager."""
        google_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google.js')
        with open(google_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('this.terrainManager = root.HYGoogleTerrainManager', content)
        self.assertIn('this.terrainManager.destroy()', content)

    def test_terrain_mesh_exact_source_provenance_and_attribution(self):
        """Verify terrain mesh contains exact attribution and source URLs."""
        mesh_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain-mesh.js')
        with open(mesh_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('SRTM', content)
        self.assertIn('USGS', content)
        self.assertIn('Mapzen Joerd', content)
        self.assertIn('https://registry.opendata.aws/terrain-tiles/', content)
        self.assertIn('attribution:', content)

    def test_terrain_manager_has_vector_and_tilt_getters(self):
        """Verify terrain manager includes getRenderingType, getCurrentTilt, and getCurrentHeading."""
        mgr_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain.js')
        with open(mgr_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('getRenderingType()', content)
        self.assertIn('getCurrentTilt()', content)
        self.assertIn('getCurrentHeading()', content)

    def test_g4b3_loader_integration_and_multichunk_lifecycle(self):
        """Verify HYGoogleTerrainManager integrates HYGoogleTerrainLoader and handles multi-chunk lifecycle."""
        mgr_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain.js')
        mesh_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-terrain-mesh.js')
        with open(mgr_path, 'r', encoding='utf-8') as f:
            mgr_content = f.read()
        with open(mesh_path, 'r', encoding='utf-8') as f:
            mesh_content = f.read()

        # Manager checks
        self.assertIn('HYGoogleTerrainLoader', mgr_content)
        self.assertIn('this.activeChunks = new Map()', mgr_content)
        self.assertIn('this.chunkStatus = new Map()', mgr_content)
        self.assertIn('_onCameraChange()', mgr_content)
        self.assertIn('_disposeChunk(tileKey)', mgr_content)
        self.assertIn('_onTileEvicted(tileKey, tileData)', mgr_content)

        # Mesh factory checks
        self.assertIn('createTileTerrainMesh', mesh_content)
        self.assertIn('updateTileExaggeration', mesh_content)

    def test_explore_template_includes_terrain_loader_script(self):
        """Verify explore_map.html includes map-google-terrain-loader.js."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')

        self.assertIn('map-google-terrain-loader.js', html)


if __name__ == '__main__':
    unittest.main()
