"""
Unit tests for Thematic Heritage Circuits & Tourist Trails Model
"""
import unittest
from models.circuits import (
    get_all_circuits,
    get_circuit_by_slug,
    get_circuit_places,
    calculate_circuit_metrics,
    filter_circuits_by_theme
)

class TestCircuitsModel(unittest.TestCase):

    def test_get_all_circuits_contains_core_trails(self):
        circuits = get_all_circuits()
        self.assertIsInstance(circuits, list)
        self.assertGreaterEqual(len(circuits), 5)
        slugs = [c['slug'] for c in circuits]
        self.assertIn('buddhist-circuit', slugs)
        self.assertIn('jain-circuit', slugs)
        self.assertIn('eco-wildlife-circuit', slugs)

    def test_get_circuit_by_slug_valid(self):
        buddhist = get_circuit_by_slug('buddhist-circuit')
        self.assertIsNotNone(buddhist)
        self.assertEqual(buddhist['slug'], 'buddhist-circuit')
        self.assertEqual(buddhist['duration_days'], 4)
        self.assertEqual(buddhist['total_distance_km'], 340)
        self.assertGreaterEqual(len(buddhist['stops']), 4)

    def test_get_circuit_by_slug_invalid(self):
        result = get_circuit_by_slug('non-existent-trail-99')
        self.assertIsNone(result)

    def test_calculate_circuit_metrics(self):
        metrics = calculate_circuit_metrics('buddhist-circuit')
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics['duration_days'], 4)
        self.assertGreater(metrics['avg_km_per_day'], 0)
        self.assertIn('suggested_transport', metrics)

    def test_filter_circuits_by_theme(self):
        spiritual = filter_circuits_by_theme('spiritual')
        self.assertGreaterEqual(len(spiritual), 1)
        nature = filter_circuits_by_theme('nature')
        self.assertGreaterEqual(len(nature), 1)

if __name__ == '__main__':
    unittest.main()
