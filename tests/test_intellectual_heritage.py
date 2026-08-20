"""
Unit and API Integration Tests for Bihar Intellectual Heritage & Ancient Scholars
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.intellectual_heritage import (
    get_all_scholars,
    get_scholar_by_slug,
    get_all_ancient_universities,
    get_university_by_slug
)


class TestIntellectualHeritageModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_scholars_catalog(self):
        """Verify presence of ancient polymaths and thinkers."""
        scholars = get_all_scholars()
        self.assertGreaterEqual(len(scholars), 4)
        slugs = [s['slug'] for s in scholars]
        self.assertIn('aryabhata-astronomer-mathematician', slugs)
        self.assertIn('chanakya-kautilya-statecraft-philosopher', slugs)
        self.assertIn('acharya-shilabhadra-nalanda-chancellor', slugs)
        self.assertIn('mahakavi-vidyapati-maithil-kokil', slugs)

    def test_ancient_universities_catalog(self):
        """Verify ancient monastic universities and library archives."""
        univs = get_all_ancient_universities()
        self.assertGreaterEqual(len(univs), 3)
        slugs = [u['slug'] for u in univs]
        self.assertIn('nalanda-monastic-university', slugs)
        self.assertIn('vikramashila-tantric-university', slugs)
        self.assertIn('telhara-monastic-complex', slugs)

    def test_scholars_api_endpoints(self):
        """Test /api/v1/scholars API endpoints."""
        res = self.client.get('/api/v1/scholars')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single scholar detail
        res_detail = self.client.get('/api/v1/scholars/aryabhata-astronomer-mathematician')
        self.assertEqual(res_detail.status_code, 200)
        detail_data = res_detail.get_json()
        self.assertEqual(detail_data['status'], 'success')
        self.assertIn('Aryabhatiya', detail_data['scholar']['primary_treatise'])

        # Universities API
        res_univ = self.client.get('/api/v1/scholars/universities')
        self.assertEqual(res_univ.status_code, 200)
        univ_data = res_univ.get_json()
        self.assertEqual(univ_data['status'], 'success')
        self.assertGreaterEqual(univ_data['count'], 3)


if __name__ == '__main__':
    unittest.main()