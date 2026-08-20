"""
Comprehensive 52-Commit Milestone Unified Test Suite
Validates the complete Regional Heritage, Discovery, Safety & Mobility ecosystem:
- Thematic Circuits & Distance Calculation
- Multilingual Place Audio Narrations
- Seasonal Cultural Festivals Calendar
- Certified GI Handicrafts & Artisan Guilds
- Responsible Traveler Code & Eco-Pledge
- Traveler Safety, 24/7 Emergency Helplines & Trauma Hospitals
- Inter-District Transit Hubs & Live Commute Fare Estimator
- AI Trip Planner Cultural & Seasonal Trail Synchronization
- JSON API Contracts & Route Verification
"""
import unittest
from flask import Flask
from routes.api import api_bp
from routes.itinerary import itinerary_bp

from models.circuits import get_all_circuits, get_circuit_by_slug, calculate_circuit_metrics
from models.places import get_place_audio_guide
from models.festivals import get_all_festivals, get_festivals_by_month
from models.crafts import get_all_crafts, get_craft_by_slug, get_artisan_centers_for_craft
from models.eco import get_responsible_travel_code, validate_pledge_submission
from models.safety import get_statewide_helplines, get_district_safety, get_medical_facilities
from models.transport import get_airports, get_railway_junctions, estimate_commute_fare, get_interdistrict_routes
from models.itineraries import get_itinerary_cultural_highlights, calculate_itinerary_budget


class TestMilestone52Ecosystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.secret_key = 'test_secret_key_milestone_52'
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.app.register_blueprint(itinerary_bp)
        cls.client = cls.app.test_client()

    # 1. Thematic Circuits Subsystem
    def test_circuits_subsystem(self):
        circuits = get_all_circuits()
        self.assertGreaterEqual(len(circuits), 5)
        for c in circuits:
            self.assertIn('slug', c)
            self.assertIn('title', c)
            self.assertIn('stops', c)
            self.assertGreater(len(c['stops']), 0)

        buddhist = get_circuit_by_slug('buddhist-circuit')
        self.assertIsNotNone(buddhist)
        self.assertEqual(buddhist['slug'], 'buddhist-circuit')
        metrics = calculate_circuit_metrics('buddhist-circuit')
        self.assertGreater(metrics['avg_km_per_day'], 0)

    # 2. Multilingual Audio Guides Subsystem
    def test_audio_guides_subsystem(self):
        golghar_audio = get_place_audio_guide('golghar')
        self.assertIsNotNone(golghar_audio)
        self.assertIn('languages', golghar_audio)
        self.assertIn('hi', golghar_audio['languages'])
        self.assertIn('en', golghar_audio['languages'])
        self.assertIn('bho', golghar_audio['languages'])

    # 3. Cultural Festivals Subsystem
    def test_festivals_subsystem(self):
        festivals = get_all_festivals()
        self.assertGreaterEqual(len(festivals), 6)
        nov_fests = get_festivals_by_month('November')
        self.assertGreaterEqual(len(nov_fests), 1)
        names = [f['name'] for f in nov_fests]
        self.assertTrue(any('Chhath' in n or 'Sonepur' in n for n in names))

    # 4. GI Crafts Subsystem
    def test_crafts_subsystem(self):
        crafts = get_all_crafts()
        self.assertGreaterEqual(len(crafts), 5)
        madhubani = get_craft_by_slug('madhubani-mithila-painting')
        self.assertIsNotNone(madhubani)
        self.assertTrue(madhubani['gi_status'])
        centers = get_artisan_centers_for_craft('madhubani-mithila-painting')
        self.assertGreaterEqual(len(centers), 1)

    # 5. Eco-Heritage Subsystem
    def test_eco_heritage_subsystem(self):
        code = get_responsible_travel_code()
        self.assertEqual(len(code), 3)
        valid, msg = validate_pledge_submission("Traveler Alpha", "alpha@example.com", "Bihar")
        self.assertTrue(valid)
        invalid, err = validate_pledge_submission("", "bad-email", "")
        self.assertFalse(invalid)

    # 6. Traveler Safety & Emergency Hub
    def test_safety_hub_subsystem(self):
        helplines = get_statewide_helplines()
        self.assertGreaterEqual(len(helplines), 8)
        patna_safety = get_district_safety('patna')
        self.assertIsNotNone(patna_safety)
        self.assertIn('police_control_room', patna_safety)
        medical = get_medical_facilities('patna')
        self.assertGreaterEqual(len(medical), 2)

    # 7. Transit Hubs & Fare Estimator Subsystem
    def test_transit_and_fare_subsystem(self):
        airports = get_airports()
        self.assertGreaterEqual(len(airports), 3)
        railways = get_railway_junctions()
        self.assertGreaterEqual(len(railways), 5)
        routes = get_interdistrict_routes()
        self.assertGreaterEqual(len(routes), 5)

        # Fare calculation
        fare = estimate_commute_fare('cab_hatchback', 10, is_night=False)
        self.assertGreater(fare['total_estimated_fare_inr'], 100)
        self.assertEqual(fare['distance_km'], 10.0)

    # 8. AI Trip Planner Cultural Enrichment
    def test_itinerary_cultural_enrichment(self):
        highlights = get_itinerary_cultural_highlights(travel_month='November', districts=['Gaya'])
        self.assertIn('festivals', highlights)
        self.assertIn('circuits', highlights)
        self.assertGreaterEqual(len(highlights['festivals']), 1)
        self.assertGreaterEqual(len(highlights['circuits']), 1)

    # 9. JSON API Verification
    def test_milestone_api_endpoints(self):
        # Circuits API
        res = self.client.get('/api/v1/circuits')
        self.assertEqual(res.status_code, 200)

        # Festivals API
        res = self.client.get('/api/v1/festivals')
        self.assertEqual(res.status_code, 200)

        # Crafts API
        res = self.client.get('/api/v1/crafts')
        self.assertEqual(res.status_code, 200)

        # Safety API
        res = self.client.get('/api/v1/safety/emergency')
        self.assertEqual(res.status_code, 200)

        # Transport API
        res = self.client.get('/api/v1/transport/hubs')
        self.assertEqual(res.status_code, 200)

        # Fare Estimator API
        res = self.client.get('/api/v1/transport/estimate-fare?vehicle_type=auto_reserved&distance_km=5')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()