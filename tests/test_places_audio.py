"""
Unit tests for Multilingual Audio Guide Model & API Endpoint
"""
import unittest
from models.places import get_place_audio_guide, PLACE_AUDIO_GUIDES_DB

class TestPlaceAudioGuides(unittest.TestCase):

    def test_audio_guide_golghar_present(self):
        guide = get_place_audio_guide('golghar')
        self.assertIsNotNone(guide)
        self.assertIn('languages', guide)
        self.assertIn('en', guide['languages'])
        self.assertIn('hi', guide['languages'])
        self.assertIn('bho', guide['languages'])

    def test_audio_guide_duration_and_narrator(self):
        guide = get_place_audio_guide('mahabodhi')
        self.assertIsNotNone(guide)
        self.assertGreater(guide['duration_sec'], 60)
        self.assertTrue(len(guide['narrator']) > 0)

    def test_audio_guide_non_existent(self):
        guide = get_place_audio_guide('random_unknown_place_xyz')
        self.assertIsNone(guide)

if __name__ == '__main__':
    unittest.main()
