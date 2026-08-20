"""
Unit and API Integration Tests for Bihar Archaeology & Epigraphy Heritage
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.archaeology import (
    get_all_archaeological_sites,
    get_site_by_slug,
    get_sites_by_district,
    get_sites_by_period,
    get_ashokan_edicts,
    get_epigraphy_chronology
)


class TestArchaeologyModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_archaeological_sites(self):
        """Verify list of ancient excavation and epigraphy sites."""
        sites = get_all_archaeological_sites()
        self.assertGreaterEqual(len(sites), 5)
        slugs = [s['slug'] for s in sites]
        self.assertIn('lauriya-nandangarh-ashokan-pillar', slugs)
        self.assertIn('rampurva-ashokan-capitals', slugs)
        self.assertIn('kolhua-vaishali-lion-pillar', slugs)
        self.assertIn('kurkihar-bronze-hoard-site', slugs)
        self.assertIn('telhara-monastic-excavations', slugs)
        self.assertIn('chirand-neolithic-settlement', slugs)

    def test_ashokan_edicts_filtering(self):
        """Verify filtering for Ashokan pillars and Brahmi rock edicts."""
        ashokan = get_ashokan_edicts()
        self.assertGreaterEqual(len(ashokan), 3)
        for s in ashokan:
            self.assertTrue('Ashoka' in s.get('ruler', '') or 'Ashoka' in s.get('title', ''))

    def test_epigraphy_chronology(self):
        """Verify historical timeline eras."""
        chrono = get_epigraphy_chronology()
        self.assertGreaterEqual(len(chrono), 4)
        eras = [c['era'] for c in chrono]
        self.assertTrue(any('Mauryan' in e for e in eras))
        self.assertTrue(any('Pala' in e for e in eras))

    def test_district_and_period_filtering(self):
        """Verify filtering sites by district and historical period."""
        champaran_sites = get_sites_by_district('West Champaran')
        self.assertGreaterEqual(len(champaran_sites), 2)

        pala_sites = get_sites_by_period('Pala')
        self.assertGreaterEqual(len(pala_sites), 1)

    def test_archaeology_api_endpoints(self):
        """Test /api/v1/archaeology API endpoints."""
        res = self.client.get('/api/v1/archaeology/sites')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single site detail
        res_detail = self.client.get('/api/v1/archaeology/sites/lauriya-nandangarh-ashokan-pillar')
        self.assertEqual(res_detail.status_code, 200)
        detail_data = res_detail.get_json()
        self.assertEqual(detail_data['status'], 'success')
        self.assertEqual(detail_data['site']['district'], 'West Champaran')

        # Chronology API
        res_chrono = self.client.get('/api/v1/archaeology/chronology')
        self.assertEqual(res_chrono.status_code, 200)
        chrono_data = res_chrono.get_json()
        self.assertEqual(chrono_data['status'], 'success')
        self.assertGreater(len(chrono_data['chronology']), 0)


if __name__ == '__main__':
    unittest.main()