"""
Unified Milestone Integration Test Suite for HiddenYatra
Verifies all 9 core subsystems and cross-domain search integration:
1. Archaeology, Epigraphy & Numismatics
2. Weather, Micro-climates & AQI Advisories
3. Folk Performing Arts, Theater & Musical Instruments
4. Certified Local Tour Guides & Storyteller Registry
5. Eco-Trails, Wilderness Treks & Campsites
6. Authentic GI Souvenirs & Artisan Workshops
7. Ancient Scholars, Treatises & Nalanda Library Towers
8. Multi-Currency Trip Budget Planner & Cost Estimator
9. Interactive Heritage Trivia Quiz & Digital Badges
10. Universal Cross-Domain Search Engine
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.search_engine import search_cross_domain_heritage
from models.archaeology import get_all_archaeological_sites, get_all_numismatic_hoards
from models.weather import get_all_district_weather, classify_aqi_level
from models.performing_arts import get_all_performing_arts, get_all_folk_instruments
from models.guides import get_all_guides, validate_guide_inquiry
from models.treks import get_all_treks, get_all_eco_campsites
from models.souvenirs import get_all_souvenirs, get_all_artisan_workshops
from models.intellectual_heritage import get_all_scholars, get_all_ancient_universities
from models.budget_planner import calculate_trip_budget, convert_currency
from models.quiz import get_all_quiz_questions, evaluate_quiz_submission


class TestMilestone138Integration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_archaeology_and_numismatics_subsystem(self):
        sites = get_all_archaeological_sites()
        self.assertGreaterEqual(len(sites), 5)
        hoards = get_all_numismatic_hoards()
        self.assertGreaterEqual(len(hoards), 3)

    def test_weather_and_aqi_subsystem(self):
        weather = get_all_district_weather()
        self.assertGreaterEqual(len(weather), 5)
        self.assertEqual(classify_aqi_level(45)['label'], 'Good')

    def test_performing_arts_subsystem(self):
        arts = get_all_performing_arts()
        self.assertGreaterEqual(len(arts), 5)
        instruments = get_all_folk_instruments()
        self.assertGreaterEqual(len(instruments), 4)

    def test_tour_guides_subsystem(self):
        guides = get_all_guides()
        self.assertGreaterEqual(len(guides), 5)
        valid, _ = validate_guide_inquiry("Traveler", "t@example.com", "9999999999", "ven-dharmapala-bodh-gaya", "2026-12-01", 2)
        self.assertTrue(valid)

    def test_eco_treks_subsystem(self):
        treks = get_all_treks()
        self.assertGreaterEqual(len(treks), 5)
        camps = get_all_eco_campsites()
        self.assertGreaterEqual(len(camps), 2)

    def test_souvenirs_subsystem(self):
        souvenirs = get_all_souvenirs()
        self.assertGreaterEqual(len(souvenirs), 5)
        workshops = get_all_artisan_workshops()
        self.assertGreaterEqual(len(workshops), 2)

    def test_intellectual_heritage_subsystem(self):
        scholars = get_all_scholars()
        self.assertGreaterEqual(len(scholars), 4)
        univs = get_all_ancient_universities()
        self.assertGreaterEqual(len(univs), 3)

    def test_budget_planner_subsystem(self):
        calc = calculate_trip_budget('heritage', 4, 2, 'USD')
        self.assertGreater(calc['total_amount'], 0)
        conv = convert_currency(8650, 'USD')
        self.assertEqual(conv['amount'], 100.0)

    def test_quiz_engine_subsystem(self):
        questions = get_all_quiz_questions()
        self.assertGreaterEqual(len(questions), 5)
        res = evaluate_quiz_submission({'q-aryabhata-discovery': 1})
        self.assertGreaterEqual(res['score'], 1)

    def test_universal_cross_domain_search(self):
        # Test searching cross-domain terms
        arch_res = search_cross_domain_heritage('lauriya')
        self.assertGreaterEqual(len(arch_res), 1)

        art_res = search_cross_domain_heritage('bidesiya')
        self.assertGreaterEqual(len(art_res), 1)

        guide_res = search_cross_domain_heritage('dharmapala')
        self.assertGreaterEqual(len(guide_res), 1)

        trek_res = search_cross_domain_heritage('mandar')
        self.assertGreaterEqual(len(trek_res), 1)

        souv_res = search_cross_domain_heritage('tikuli')
        self.assertGreaterEqual(len(souv_res), 1)

        scholar_res = search_cross_domain_heritage('aryabhata')
        self.assertGreaterEqual(len(scholar_res), 1)


if __name__ == '__main__':
    unittest.main()