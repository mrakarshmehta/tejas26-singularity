"""
Unit and API Integration Tests for Bihar Authentic GI Souvenirs & Crafts
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.souvenirs import (
    get_all_souvenirs,
    get_souvenir_by_slug,
    get_souvenirs_by_district,
    get_souvenirs_by_category,
    get_fair_trade_shopping_guidelines
)


class TestSouvenirsModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_souvenirs_catalog(self):
        """Verify presence of signature GI artisan crafts."""
        souvenirs = get_all_souvenirs()
        self.assertGreaterEqual(len(souvenirs), 5)
        slugs = [s['slug'] for s in souvenirs]
        self.assertIn('mithila-madhubani-tussar-scroll', slugs)
        self.assertIn('bhagalpur-tussar-matka-shawl', slugs)
        self.assertIn('sikki-golden-grass-coasters-box', slugs)
        self.assertIn('patna-tikuli-glass-enamel-platter', slugs)
        self.assertIn('gaya-patharkatti-black-stone-sculpture', slugs)

    def test_district_and_category_filtering(self):
        """Verify filtering by district and craft category."""
        madhubani_crafts = get_souvenirs_by_district('Madhubani')
        self.assertGreaterEqual(len(madhubani_crafts), 2)

        silk_crafts = get_souvenirs_by_category('Silk')
        self.assertGreaterEqual(len(silk_crafts), 1)

    def test_fair_trade_guidelines(self):
        """Verify fair trade guidelines data."""
        guidelines = get_fair_trade_shopping_guidelines()
        self.assertGreaterEqual(len(guidelines), 3)
        titles = [g['title'] for g in guidelines]
        self.assertTrue(any('Authenticity Seals' in t for t in titles))

    def test_souvenirs_api_endpoints(self):
        """Test /api/v1/souvenirs API endpoints."""
        res = self.client.get('/api/v1/souvenirs')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single souvenir detail
        res_detail = self.client.get('/api/v1/souvenirs/bhagalpur-tussar-matka-shawl')
        self.assertEqual(res_detail.status_code, 200)
        detail_data = res_detail.get_json()
        self.assertEqual(detail_data['status'], 'success')
        self.assertEqual(detail_data['souvenir']['district'], 'Bhagalpur')

        # Guidelines API
        res_guide = self.client.get('/api/v1/souvenirs/guidelines')
        self.assertEqual(res_guide.status_code, 200)
        self.assertEqual(res_guide.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()

class TestArtisanWorkshops(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_workshops_database(self):
        """Verify presence of signature artisan village workshops."""
        from models.souvenirs import get_all_artisan_workshops
        workshops = get_all_artisan_workshops()
        self.assertGreaterEqual(len(workshops), 2)
        districts = [w['district'] for w in workshops]
        self.assertIn('Madhubani', districts)
        self.assertIn('Bhagalpur', districts)

    def test_workshops_api(self):
        """Test /api/v1/souvenirs/workshops API endpoint."""
        res = self.client.get('/api/v1/souvenirs/workshops')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(data['count'], 2)