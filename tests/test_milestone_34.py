"""
Unified Milestone 34 Integration & Ecosystem Test Suite
Validates the complete Virtual Tours, Gastronomy, Wildlife, Volunteerism,
and Universal Discovery Search subsystems.
"""
import unittest
from flask import Flask
from routes.api import api_bp

from models.panoramas import get_all_panoramas, get_panorama_by_slug
from models.gastronomy import get_all_dishes, get_gi_tagged_dishes, get_culinary_trails
from models.wildlife import get_all_sanctuaries, get_ramsar_wetlands
from models.volunteer import get_all_programs, calculate_skill_match_score, validate_volunteer_application
from models.search_engine import search_cross_domain_heritage


class TestMilestone34Ecosystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    # 1. Virtual 360 Panoramas
    def test_panoramas_ecosystem(self):
        panos = get_all_panoramas()
        self.assertGreaterEqual(len(panos), 5)
        for p in panos:
            self.assertIn('slug', p)
            self.assertIn('resolution', p)
            self.assertGreater(len(p['hotspots']), 0)
        
        mb = get_panorama_by_slug('mahabodhi-temple-sanctum')
        self.assertIsNotNone(mb)
        self.assertEqual(mb['district'], 'Gaya')

    # 2. Gastronomy & Food Trails
    def test_gastronomy_ecosystem(self):
        dishes = get_all_dishes()
        self.assertGreaterEqual(len(dishes), 6)
        gi_dishes = get_gi_tagged_dishes()
        self.assertGreaterEqual(len(gi_dishes), 2)
        trails = get_culinary_trails()
        self.assertGreaterEqual(len(trails), 2)

    # 3. Wildlife Sanctuaries & Ramsar Sites
    def test_wildlife_ecosystem(self):
        sanctuaries = get_all_sanctuaries()
        self.assertGreaterEqual(len(sanctuaries), 5)
        ramsar = get_ramsar_wetlands()
        self.assertGreaterEqual(len(ramsar), 1)

    # 4. Rural Volunteerism & Skill Matching
    def test_volunteer_ecosystem(self):
        progs = get_all_programs()
        self.assertGreaterEqual(len(progs), 4)
        score = calculate_skill_match_score(['Digital Photography'], 'madhubani-art-guild-residency')
        self.assertGreater(score, 0)
        valid, _ = validate_volunteer_application('Rahul Verma', 'rahul@example.com', '+919876543210', 'madhubani-art-guild-residency', 'Excited to contribute to rural art documentation.')
        self.assertTrue(valid)

    # 5. Universal Search Engine
    def test_universal_search_engine(self):
        r_buddhist = search_cross_domain_heritage('buddhist')
        self.assertGreaterEqual(len(r_buddhist), 1)
        r_dolphin = search_cross_domain_heritage('dolphin')
        self.assertGreaterEqual(len(r_dolphin), 1)
        r_khaja = search_cross_domain_heritage('khaja')
        self.assertGreaterEqual(len(r_khaja), 1)

    # 6. JSON API Verification
    def test_milestone_34_api_endpoints(self):
        # Panoramas
        res_p = self.client.get('/api/v1/panoramas')
        self.assertEqual(res_p.status_code, 200)

        # Gastronomy
        res_g = self.client.get('/api/v1/gastronomy/dishes')
        self.assertEqual(res_g.status_code, 200)

        # Wildlife
        res_w = self.client.get('/api/v1/wildlife/sanctuaries')
        self.assertEqual(res_w.status_code, 200)

        # Volunteer
        res_v = self.client.get('/api/v1/volunteer/programs')
        self.assertEqual(res_v.status_code, 200)

        # Universal Search
        res_s = self.client.get('/api/v1/universal-search?q=makhana')
        self.assertEqual(res_s.status_code, 200)
        self.assertEqual(res_s.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()