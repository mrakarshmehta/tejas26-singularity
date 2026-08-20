"""
Unit tests for Festivals & Cultural Events Model
"""
import unittest
from models.festivals import (
    get_all_festivals,
    get_festival_by_slug,
    get_festivals_by_month,
    get_festivals_by_district
)

class TestFestivalsModel(unittest.TestCase):

    def test_get_all_festivals_count(self):
        fests = get_all_festivals()
        self.assertIsInstance(fests, list)
        self.assertGreaterEqual(len(fests), 6)

    def test_chhath_puja_details(self):
        chhath = get_festival_by_slug('chhath-puja')
        self.assertIsNotNone(chhath)
        self.assertEqual(chhath['month_num'], 10)
        self.assertIn('Patna', chhath['primary_districts'])

    def test_get_festivals_by_month(self):
        nov_fests = get_festivals_by_month(11)
        self.assertGreaterEqual(len(nov_fests), 1)
        slugs = [f['slug'] for f in nov_fests]
        self.assertIn('sonpur-mela', slugs)

    def test_get_festivals_by_district(self):
        nalanda_fests = get_festivals_by_district('Nalanda')
        self.assertGreaterEqual(len(nalanda_fests), 1)
        self.assertEqual(nalanda_fests[0]['slug'], 'rajgir-mahotsav')

if __name__ == '__main__':
    unittest.main()
