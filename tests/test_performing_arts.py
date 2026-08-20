"""
Unit and API Integration Tests for Bihar Folk Performing Arts & Music
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.performing_arts import (
    get_all_performing_arts,
    get_art_by_slug,
    get_arts_by_region,
    get_all_folk_instruments
)


class TestPerformingArtsModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_performing_arts(self):
        """Verify presence of traditional folk arts and theater."""
        arts = get_all_performing_arts()
        self.assertGreaterEqual(len(arts), 5)
        slugs = [a['slug'] for a in arts]
        self.assertIn('bidesiya-folk-theater', slugs)
        self.assertIn('manbhum-chhau-dance', slugs)
        self.assertIn('domkach-wedding-theater', slugs)
        self.assertIn('bihari-kajari-monsoon-songs', slugs)
        self.assertIn('mithila-sohar-childbirth-chants', slugs)

    def test_folk_instruments(self):
        """Verify folk instrument catalog."""
        insts = get_all_folk_instruments()
        self.assertGreaterEqual(len(insts), 4)
        names = [i['name'] for i in insts]
        self.assertIn('Dholak', names)
        self.assertIn('Shehnai', names)

    def test_region_filtering(self):
        """Verify region filtering."""
        bhojpur_arts = get_arts_by_region('Bhojpur')
        self.assertGreaterEqual(len(bhojpur_arts), 1)

    def test_performing_arts_api(self):
        """Test /api/v1/performing-arts API endpoints."""
        res = self.client.get('/api/v1/performing-arts')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single art detail
        res_detail = self.client.get('/api/v1/performing-arts/bidesiya-folk-theater')
        self.assertEqual(res_detail.status_code, 200)
        detail_data = res_detail.get_json()
        self.assertEqual(detail_data['status'], 'success')
        self.assertEqual(detail_data['art']['slug'], 'bidesiya-folk-theater')

        # Instruments API
        res_inst = self.client.get('/api/v1/performing-arts/instruments')
        self.assertEqual(res_inst.status_code, 200)
        self.assertEqual(res_inst.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()