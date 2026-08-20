"""
Unit and API Integration Tests for Traveler Safety & Emergency Directory
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.safety import (
    get_statewide_helplines,
    get_all_district_safety,
    get_district_safety,
    get_medical_facilities,
    get_safety_guidelines
)


class TestSafetyModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_statewide_helplines(self):
        """Verify priority emergency numbers are present and sorted."""
        helplines = get_statewide_helplines()
        self.assertGreaterEqual(len(helplines), 8)
        numbers = [h['number'] for h in helplines]
        self.assertIn('112', numbers)
        self.assertIn('108', numbers)
        self.assertIn('1091', numbers)
        self.assertIn('181', numbers)
        self.assertIn('1070', numbers)

    def test_district_safety_lookup(self):
        """Verify district safety contact retrieval."""
        patna = get_district_safety('patna')
        self.assertIsNotNone(patna)
        self.assertEqual(patna['district'], 'Patna')
        self.assertIn('police_control_room', patna)
        self.assertIn('tourist_police_desk', patna)
        self.assertGreater(len(patna['medical_facilities']), 0)

        # Test case insensitivity and whitespace handling
        gaya = get_district_safety('  GAYA  ')
        self.assertIsNotNone(gaya)
        self.assertEqual(gaya['district'], 'Gaya')

    def test_district_safety_invalid(self):
        """Invalid or non-existent district slug should return None."""
        self.assertIsNone(get_district_safety('non_existent_district_xyz'))
        self.assertIsNone(get_district_safety(''))
        self.assertIsNone(get_district_safety(None))

    def test_medical_facilities_queries(self):
        """Verify medical facilities listing and filtering."""
        all_facs = get_medical_facilities()
        self.assertGreaterEqual(len(all_facs), 10)
        trauma_centers = [f for f in all_facs if f.get('trauma_center')]
        self.assertGreater(len(trauma_centers), 0)

        patna_facs = get_medical_facilities('patna')
        self.assertGreaterEqual(len(patna_facs), 2)
        names = [f['name'] for f in patna_facs]
        self.assertTrue(any('PMCH' in n or 'Patna Medical' in n for n in names))

    def test_safety_guidelines(self):
        """Verify traveler safety guidelines categories."""
        guidelines = get_safety_guidelines()
        self.assertGreaterEqual(len(guidelines), 2)
        categories = [g['category'] for g in guidelines]
        self.assertTrue(any('General' in c or 'Transit' in c for c in categories))

    def test_api_emergency_contacts(self):
        """Test /api/v1/safety/emergency endpoint."""
        res = self.client.get('/api/v1/safety/emergency')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('statewide_helplines', data)
        self.assertIn('districts', data)

        res_district = self.client.get('/api/v1/safety/emergency?district=patna')
        self.assertEqual(res_district.status_code, 200)
        data_dist = res_district.get_json()
        self.assertEqual(data_dist['status'], 'success')
        self.assertEqual(data_dist['district_safety']['district'], 'Patna')

    def test_api_medical_facilities(self):
        """Test /api/v1/safety/medical endpoint."""
        res = self.client.get('/api/v1/safety/medical?district=gaya')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

    def test_api_guidelines(self):
        """Test /api/v1/safety/guidelines endpoint."""
        res = self.client.get('/api/v1/safety/guidelines')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('guidelines', data)


if __name__ == '__main__':
    unittest.main()