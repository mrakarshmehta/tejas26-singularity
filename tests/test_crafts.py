"""
Unit tests for GI Crafts & Artisan Guilds Model
"""
import unittest
from models.crafts import (
    get_all_crafts,
    get_craft_by_slug,
    get_artisan_centers_for_craft,
    get_crafts_by_district
)

class TestCraftsModel(unittest.TestCase):

    def test_get_all_crafts_includes_core_arts(self):
        crafts = get_all_crafts()
        self.assertIsInstance(crafts, list)
        self.assertGreaterEqual(len(crafts), 5)
        slugs = [c['slug'] for c in crafts]
        self.assertIn('madhubani-mithila-painting', slugs)
        self.assertIn('bhagalpuri-tussar-silk', slugs)
        self.assertIn('sikki-grass-craft', slugs)

    def test_get_craft_by_slug(self):
        madhubani = get_craft_by_slug('madhubani-mithila-painting')
        self.assertIsNotNone(madhubani)
        self.assertEqual(madhubani['origin_district'], 'Madhubani')
        self.assertIn('Jitwarpur', madhubani['prominent_villages'])

    def test_get_artisan_centers_for_craft(self):
        centers = get_artisan_centers_for_craft('bhagalpuri-tussar-silk')
        self.assertGreaterEqual(len(centers), 1)
        self.assertIn('Champanagar', centers[0]['location'])

    def test_get_crafts_by_district(self):
        bhagalpur_crafts = get_crafts_by_district('Bhagalpur')
        self.assertGreaterEqual(len(bhagalpur_crafts), 1)

if __name__ == '__main__':
    unittest.main()
