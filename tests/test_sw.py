"""
Unit tests for PWA Service Worker Manifest & Offline Fallback Configuration
"""
import unittest
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestPWAConfig(unittest.TestCase):

    def test_manifest_json_structure(self):
        manifest_path = os.path.join(PROJECT_ROOT, 'static', 'manifest.json')
        self.assertTrue(os.path.exists(manifest_path))
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        self.assertIn('name', manifest)
        self.assertIn('start_url', manifest)
        self.assertIn('display', manifest)

    def test_sw_contains_offline_cache(self):
        sw_path = os.path.join(PROJECT_ROOT, 'static', 'sw.js')
        self.assertTrue(os.path.exists(sw_path))
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw_code = f.read()
        self.assertIn('/offline', sw_code)


if __name__ == '__main__':
    unittest.main()