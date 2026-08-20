"""
Unit tests for Sustainable Tourism & Eco-Pledge Module
"""
import unittest
from models.eco import get_responsible_travel_code, validate_pledge_submission

class TestEcoModel(unittest.TestCase):

    def test_get_responsible_travel_pillars(self):
        pillars = get_responsible_travel_code()
        self.assertIsInstance(pillars, list)
        self.assertEqual(len(pillars), 3)
        pillar_names = [p['pillar_name'] for p in pillars]
        self.assertIn('Zero-Trace Heritage Preservation', pillar_names)

    def test_validate_pledge_submission_valid(self):
        is_valid, msg = validate_pledge_submission("Rohan Sharma", "rohan@example.com", "Bihar")
        self.assertTrue(is_valid)

    def test_validate_pledge_submission_invalid_name(self):
        is_valid, msg = validate_pledge_submission("", "rohan@example.com", "Bihar")
        self.assertFalse(is_valid)

    def test_validate_pledge_submission_invalid_email(self):
        is_valid, msg = validate_pledge_submission("Rohan Sharma", "invalid-email", "Bihar")
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()
