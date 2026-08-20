"""
Unified Integration Test Suite for the 35-Commit Discovery Milestone
Runs tests across circuits, audio guides, festivals, crafts, and eco modules.
"""
import unittest
import sys

# Import test suites
from tests.test_circuits import TestCircuitsModel
from tests.test_places_audio import TestPlacesAudioGuide
from tests.test_festivals import TestFestivalsModel
from tests.test_crafts import TestCraftsModel
from tests.test_eco import TestEcoModel

def load_discovery_test_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestCircuitsModel))
    suite.addTests(loader.loadTestsFromTestCase(TestPlacesAudioGuide))
    suite.addTests(loader.loadTestsFromTestCase(TestFestivalsModel))
    suite.addTests(loader.loadTestsFromTestCase(TestCraftsModel))
    suite.addTests(loader.loadTestsFromTestCase(TestEcoModel))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(load_discovery_test_suite())
    sys.exit(0 if result.wasSuccessful() else 1)
