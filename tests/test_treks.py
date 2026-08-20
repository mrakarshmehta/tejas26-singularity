"""
Unit and API Integration Tests for Bihar Eco-Trails & Trekking Expeditions
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.treks import (
    get_all_treks,
    get_trek_by_slug,
    get_treks_by_district,
    get_treks_by_difficulty,
    get_trekking_safety_guidelines
)


class TestTreksModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_treks_database(self):
        """Verify list of eco-trails and mountain expeditions."""
        treks = get_all_treks()
        self.assertGreaterEqual(len(treks), 5)
        slugs = [t['slug'] for t in treks]
        self.assertIn('mandar-hill-granite-ascent', slugs)
        self.assertIn('brahmayoni-peak-trail', slugs)
        self.assertIn('dungeshwari-pragbodhi-hill-trail', slugs)
        self.assertIn('rohtasgarh-fort-plateau-trek', slugs)
        self.assertIn('tutla-bhawani-canyon-trek', slugs)

    def test_difficulty_and_district_filtering(self):
        """Verify filtering treks by difficulty and district."""
        rohtas_treks = get_treks_by_district('Rohtas')
        self.assertGreaterEqual(len(rohtas_treks), 2)

        mod_treks = get_treks_by_difficulty('Moderate')
        self.assertGreaterEqual(len(mod_treks), 2)

    def test_safety_guidelines(self):
        """Verify Leave No Trace and safety guidelines."""
        guidelines = get_trekking_safety_guidelines()
        self.assertGreaterEqual(len(guidelines), 4)
        principles = [g['principle'] for g in guidelines]
        self.assertTrue(any('Leave No Trace' in p for p in principles))

    def test_treks_api_endpoints(self):
        """Test /api/v1/treks API endpoints."""
        res = self.client.get('/api/v1/treks')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single trek detail
        res_detail = self.client.get('/api/v1/treks/mandar-hill-granite-ascent')
        self.assertEqual(res_detail.status_code, 200)
        detail_data = res_detail.get_json()
        self.assertEqual(detail_data['status'], 'success')
        self.assertEqual(detail_data['trek']['district'], 'Banka')

        # Safety API
        res_safety = self.client.get('/api/v1/treks/safety')
        self.assertEqual(res_safety.status_code, 200)
        self.assertEqual(res_safety.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()

class TestEcoCampsites(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_campsites_data(self):
        """Verify presence of signature eco-campsites."""
        from models.treks import get_all_eco_campsites
        campsites = get_all_eco_campsites()
        self.assertGreaterEqual(len(campsites), 2)
        districts = [c['district'] for c in campsites]
        self.assertIn('West Champaran', districts)
        self.assertIn('Rohtas', districts)

    def test_campsites_api(self):
        """Test /api/v1/treks/campsites endpoint."""
        res = self.client.get('/api/v1/treks/campsites')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(data['count'], 2)

class TestTrekFitnessGuidelines(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_fitness_levels_data(self):
        """Verify fitness level grades."""
        from models.treks import get_trek_fitness_levels
        levels = get_trek_fitness_levels()
        self.assertEqual(len(levels), 3)
        grades = [l['grade'] for l in levels]
        self.assertIn('Easy', grades)
        self.assertIn('Moderate', grades)
        self.assertIn('Challenging', grades)

    def test_fitness_api(self):
        """Test /api/v1/treks/fitness endpoint."""
        res = self.client.get('/api/v1/treks/fitness')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['count'], 3)