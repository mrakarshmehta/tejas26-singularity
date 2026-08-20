"""
Unit and API Integration Tests for Virtual 360 Panoramas & Viewpoints
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.panoramas import (
    get_all_panoramas,
    get_panorama_by_slug,
    get_panorama_by_id,
    get_panoramas_by_district,
    get_panoramas_by_category,
    get_panorama_hotspots
)


class TestPanoramasModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_panoramas_catalog(self):
        """Verify list of virtual 360 photo spheres."""
        panos = get_all_panoramas()
        self.assertGreaterEqual(len(panos), 5)
        for p in panos:
            self.assertIn('slug', p)
            self.assertIn('title', p)
            self.assertIn('resolution', p)
            self.assertIn('coordinates', p)
            self.assertGreater(len(p.get('hotspots', [])), 0)

    def test_get_panorama_by_slug(self):
        """Verify panorama lookup by slug and place slug."""
        mahabodhi = get_panorama_by_slug('mahabodhi-temple-sanctum')
        self.assertIsNotNone(mahabodhi)
        self.assertEqual(mahabodhi['district'], 'Gaya')
        self.assertTrue(mahabodhi['audio_narration_available'])

        nalanda = get_panorama_by_slug('nalanda-ruins')
        self.assertIsNotNone(nalanda)
        self.assertEqual(nalanda['district'], 'Nalanda')

    def test_get_panorama_by_district_and_category(self):
        """Verify filtering by district and category theme."""
        gaya_panos = get_panoramas_by_district('Gaya')
        self.assertGreaterEqual(len(gaya_panos), 1)

        spiritual = get_panoramas_by_category('Spiritual Heritage')
        self.assertGreaterEqual(len(spiritual), 1)

    def test_get_panorama_hotspots(self):
        """Verify coordinate pitch and yaw hotspots for interactive exploration."""
        hotspots = get_panorama_hotspots('mahabodhi-temple-sanctum')
        self.assertGreaterEqual(len(hotspots), 2)
        hs = hotspots[0]
        self.assertIn('pitch', hs)
        self.assertIn('yaw', hs)
        self.assertIn('title', hs)

    def test_api_panoramas_endpoints(self):
        """Test /api/v1/panoramas and detail endpoints."""
        res = self.client.get('/api/v1/panoramas')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single detail
        res_detail = self.client.get('/api/v1/panoramas/mahabodhi-temple-sanctum')
        self.assertEqual(res_detail.status_code, 200)
        data_detail = res_detail.get_json()
        self.assertEqual(data_detail['status'], 'success')
        self.assertEqual(data_detail['panorama']['slug'], 'mahabodhi-temple-sanctum')

        # Hotspots
        res_hs = self.client.get('/api/v1/panoramas/mahabodhi-temple-sanctum/hotspots')
        self.assertEqual(res_hs.status_code, 200)
        data_hs = res_hs.get_json()
        self.assertEqual(data_hs['status'], 'success')
        self.assertGreater(data_hs['count'], 0)


if __name__ == '__main__':
    unittest.main()