"""
Unit tests for Map Haversine Distance & Radius Filtering
"""
import unittest
from models.places import calculate_haversine_distance, get_bounding_box

class TestMapProximity(unittest.TestCase):

    def test_haversine_patna_to_gaya(self):
        # Patna: 25.5941, 85.1376; Gaya: 24.7914, 85.0002
        dist = calculate_haversine_distance(25.5941, 85.1376, 24.7914, 85.0002)
        self.assertGreater(dist, 80)
        self.assertLess(dist, 110)

    def test_haversine_same_point(self):
        dist = calculate_haversine_distance(25.0, 85.0, 25.0, 85.0)
        self.assertEqual(dist, 0.0)

    def test_bounding_box_generation(self):
        bbox = get_bounding_box(25.0, 85.0, radius_km=25)
        self.assertLess(bbox['min_lat'], 25.0)
        self.assertGreater(bbox['max_lat'], 25.0)
        self.assertLess(bbox['min_lon'], 85.0)
        self.assertGreater(bbox['max_lon'], 85.0)

if __name__ == '__main__':
    unittest.main()
