"""
HiddenYatra — Unit Test Suite for Phase G4B-1R Authentic DEM Ingestion Pipeline.
Validates binary header format, real NASA SRTM source provenance, SHA-256 integrity,
Int16 quantization accuracy, zero border seam mismatches, NoData handling, and synthetic data guards.
"""
import os
import sys
import math
import json
import struct
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.preprocess_dem_tiles import (
    TERRAIN_DIR,
    HEADER_MAGIC,
    FORMAT_VERSION,
    VERTEX_GRID_SIZE,
    TOTAL_SAMPLES,
    NODATA_INT16,
    QUANTIZATION_SCALE,
    SRTM1RasterReader,
    decode_hyelev_file,
    encode_hyelev_file,
    validate_neighbor_seams,
    run_pipeline,
)


class TestHYMapTerrainTilesPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manifest_path = os.path.join(TERRAIN_DIR, "manifest.json")
        with open(cls.manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)

    def test_01_synthetic_generator_strictly_absent(self):
        """Synthetic Data Guard: Verify sample_continuous_elevation does NOT exist in preprocessing script."""
        import scripts.preprocess_dem_tiles as prep_mod
        self.assertFalse(
            hasattr(prep_mod, 'sample_continuous_elevation'),
            "sample_continuous_elevation MUST NOT exist in production preprocessing pipeline!"
        )

    def test_02_pipeline_aborts_safely_when_real_dem_unavailable(self):
        """Synthetic Data Guard: Verify run_pipeline returns False and generates zero files without real DEM."""
        res = run_pipeline(None)
        self.assertFalse(res)

        res_nonexistent = run_pipeline("/path/to/nonexistent/directory")
        self.assertFalse(res_nonexistent)

    def test_03_manifest_structure_and_real_source_provenance(self):
        """Verify manifest.json exists, is_synthetic_test_data is False, and contains authentic DEM attribution."""
        self.assertEqual(self.manifest["version"], "1.0")
        self.assertFalse(self.manifest["is_synthetic_test_data"])
        self.assertEqual(self.manifest["tile_size_cells"], 64)
        self.assertEqual(self.manifest["vertex_grid_size"], 65)
        self.assertEqual(self.manifest["sample_count_per_tile"], 4225)
        self.assertEqual(self.manifest["header_size_bytes"], 40)
        self.assertEqual(self.manifest["file_size_bytes_uncompressed"], 8490)

        source = self.manifest["source"]
        self.assertIn("NASA", source["dataset"])
        self.assertIn("SRTM", source["dataset"])
        self.assertIn("attribution", source)
        self.assertIn("license", source)
        self.assertIn("source_url", source)

    def test_04_manifest_contains_all_six_source_sha256_hashes(self):
        """Verify manifest.json records valid 64-character SHA-256 hashes for all 6 source HGT rasters."""
        expected_rasters = [
            "N24E083.hgt", "N24E084.hgt", "N24E085.hgt",
            "N24E086.hgt", "N24E087.hgt", "N25E085.hgt"
        ]
        source_files = self.manifest["source_files"]
        for r in expected_rasters:
            self.assertIn(r, source_files)
            sha = source_files[r]
            self.assertEqual(len(sha), 64, f"Invalid SHA-256 hash length for {r}")

    def test_05_binary_header_and_payload_integrity(self):
        """Verify every generated .hyelev tile starts with 'HYEL', version 1, and size 8490 bytes."""
        for tile_key, meta in self.manifest["tiles"].items():
            tile_path = os.path.join(TERRAIN_DIR, meta["file"])
            self.assertTrue(os.path.exists(tile_path), f"Missing tile file: {tile_path}")

            with open(tile_path, 'rb') as f:
                data = f.read()

            self.assertEqual(len(data), 8490, f"Tile {tile_key} size must be 8490 bytes")
            header_dict, samples = decode_hyelev_file(data)
            self.assertEqual(header_dict["z"], meta["z"])
            self.assertEqual(header_dict["x"], meta["x"])
            self.assertEqual(header_dict["y"], meta["y"])
            self.assertEqual(header_dict["gridWidth"], 65)
            self.assertEqual(header_dict["gridHeight"], 65)
            self.assertEqual(header_dict["sampleCount"], 4225)
            self.assertEqual(len(samples), 4225)

            # Assert no NaNs or Infs in valid generated tiles
            self.assertTrue(all(not math.isnan(s) and not math.isinf(s) for s in samples))

    def test_06_int16_quantization_and_reconstruction_fidelity(self):
        """Verify Int16 reconstruction error with QUANTIZATION_SCALE=0.03125m is <= 0.015625m."""
        for tile_key, meta in self.manifest["tiles"].items():
            self.assertLessEqual(
                meta["maxQuantizationError"],
                0.015625,
                f"Quantization error exceeded in {tile_key}: {meta['maxQuantizationError']}m"
            )

    def test_07_zero_border_seam_mismatches(self):
        """Verify 100% exact zero-tolerance shared-border vertex matching across all adjacent tiles."""
        tiles_data = {}
        for tile_key, meta in self.manifest["tiles"].items():
            tile_path = os.path.join(TERRAIN_DIR, meta["file"])
            with open(tile_path, 'rb') as f:
                data = f.read()
            _, decoded = decode_hyelev_file(data)
            tiles_data[(meta["z"], meta["x"], meta["y"])] = decoded

        seams_checked, mismatches = validate_neighbor_seams(tiles_data)
        self.assertGreater(seams_checked, 1000, "Should have validated over 1,000 shared border vertices")
        self.assertEqual(mismatches, 0, f"Detected {mismatches} shared border seam mismatches!")

    def test_08_nodata_handling(self):
        """Verify NoData marker (-32768) decodes to NaN safely."""
        dummy_header = struct.pack(
            '<4sH B x I I H H I f f f f',
            HEADER_MAGIC, FORMAT_VERSION, 9, 374, 219, 65, 65, 4225, 0.0, 100.0, 0.0, QUANTIZATION_SCALE
        )
        dummy_payload = struct.pack('<4225h', *([NODATA_INT16] * 4225))
        dummy_data = dummy_header + dummy_payload

        _, decoded = decode_hyelev_file(dummy_data)
        self.assertEqual(len(decoded), 4225)
        self.assertTrue(all(math.isnan(val) for val in decoded))

    def test_09_real_elevation_ranges_reflect_authentic_geography(self):
        """Verify real elevation ranges match physical topography (e.g. Kaimur > 500m, Rajgir > 200m)."""
        tiles = self.manifest["tiles"]
        # Check Rajgir tile
        rajgir_tile = tiles.get("11/1507/878")
        self.assertIsNotNone(rajgir_tile)
        self.assertGreater(rajgir_tile["maxElevation"], 200.0)

        # Check Kaimur tile
        kaimur_tile = tiles.get("11/1499/879")
        self.assertIsNotNone(kaimur_tile)
        self.assertGreater(kaimur_tile["maxElevation"], 500.0)


if __name__ == '__main__':
    unittest.main()
