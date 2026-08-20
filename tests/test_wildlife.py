"""
Unit and API Integration Tests for Bihar Wildlife Sanctuaries & Eco-Reserves
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.wildlife import (
    get_all_sanctuaries,
    get_sanctuary_by_slug,
    get_sanctuaries_by_district,
    get_ramsar_wetlands,
    get_safari_guidelines,
    get_endangered_species_list
)


class TestWildlifeModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_sanctuaries_present(self):
        """Verify list of key national parks and sanctuaries."""
        sanctuaries = get_all_sanctuaries()
        self.assertGreaterEqual(len(sanctuaries), 5)
        slugs = [s['slug'] for s in sanctuaries]
        self.assertIn('valmiki-tiger-reserve', slugs)
        self.assertIn('vikramshila-dolphin-sanctuary', slugs)
        self.assertIn('kanwar-lake-bird-sanctuary', slugs)
        self.assertIn('bhimbandh-wildlife-sanctuary', slugs)
        self.assertIn('kaimur-wildlife-sanctuary', slugs)

    def test_ramsar_wetlands(self):
        """Verify Ramsar wetland site identification."""
        wetlands = get_ramsar_wetlands()
        self.assertGreaterEqual(len(wetlands), 1)
        self.assertTrue(any(w['slug'] == 'kanwar-lake-bird-sanctuary' for w in wetlands))

    def test_safari_guidelines(self):
        """Verify presence of conservation and safari guidelines."""
        guidelines = get_safari_guidelines()
        self.assertGreaterEqual(len(guidelines), 3)
        topics = [g['topic'] for g in guidelines]
        self.assertTrue(any('Plastic-Free' in t or 'Permit' in t for t in topics))

    def test_endangered_species(self):
        """Verify key endangered fauna tracking."""
        species = get_endangered_species_list()
        self.assertGreaterEqual(len(species), 10)
        self.assertTrue(any('Tiger' in s for s in species))
        self.assertTrue(any('Dolphin' in s for s in species))

    def test_wildlife_api(self):
        """Test /api/v1/wildlife endpoints."""
        res = self.client.get('/api/v1/wildlife/sanctuaries')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single detail
        res_detail = self.client.get('/api/v1/wildlife/sanctuaries/valmiki-tiger-reserve')
        self.assertEqual(res_detail.status_code, 200)
        s_data = res_detail.get_json()
        self.assertEqual(s_data['status'], 'success')
        self.assertEqual(s_data['sanctuary']['district'], 'West Champaran')

        # Species API
        res_species = self.client.get('/api/v1/wildlife/species')
        self.assertEqual(res_species.status_code, 200)
        self.assertEqual(res_species.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()