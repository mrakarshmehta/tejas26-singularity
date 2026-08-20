"""
Comprehensive Contract & Routing Verification for the 35-Commit Milestone
"""
import unittest
from models.circuits import get_all_circuits, get_circuit_by_slug
from models.festivals import get_all_festivals
from models.crafts import get_all_crafts
from models.eco import get_responsible_travel_code

class TestDiscoveryContract(unittest.TestCase):

    def test_circuits_contract(self):
        circuits = get_all_circuits()
        self.assertGreaterEqual(len(circuits), 5)
        for c in circuits:
            self.assertIn('slug', c)
            self.assertIn('name', c)
            self.assertIn('stops', c)

    def test_festivals_contract(self):
        festivals = get_all_festivals()
        self.assertGreaterEqual(len(festivals), 6)
        for f in festivals:
            self.assertIn('slug', f)
            self.assertIn('month_num', f)
            self.assertIn('primary_districts', f)

    def test_crafts_contract(self):
        crafts = get_all_crafts()
        self.assertGreaterEqual(len(crafts), 5)
        for cr in crafts:
            self.assertIn('slug', cr)
            self.assertIn('gi_status', cr)
            self.assertIn('prominent_villages', cr)

    def test_eco_contract(self):
        pillars = get_responsible_travel_code()
        self.assertEqual(len(pillars), 3)

if __name__ == '__main__':
    unittest.main()
