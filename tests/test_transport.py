"""
Unit and API Integration Tests for Bihar Transit Guide & Commute Fare Estimator
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.transport import (
    get_airports,
    get_railway_junctions,
    get_bus_terminals,
    get_all_transport_hubs,
    get_interdistrict_routes,
    get_vehicle_rate_cards,
    estimate_commute_fare
)


class TestTransportModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_airports_catalog(self):
        """Verify Bihar commercial airport gateways."""
        airports = get_airports()
        self.assertGreaterEqual(len(airports), 3)
        codes = [a['code'] for a in airports]
        self.assertIn('PAT', codes)
        self.assertIn('GAY', codes)
        self.assertIn('DBR', codes)

    def test_railway_junctions(self):
        """Verify major railway junctions."""
        junctions = get_railway_junctions()
        self.assertGreaterEqual(len(junctions), 5)
        codes = [j['code'] for j in junctions]
        self.assertIn('PNBE', codes)
        self.assertIn('GAYA', codes)
        self.assertIn('RGD', codes)

    def test_interdistrict_routes(self):
        """Verify transit matrix calculation and filtering."""
        routes = get_interdistrict_routes()
        self.assertGreaterEqual(len(routes), 5)

        gaya_routes = get_interdistrict_routes(destination='Gaya')
        self.assertGreaterEqual(len(gaya_routes), 1)
        r = gaya_routes[0]
        self.assertIn('distance_km', r)
        self.assertIn('train_time_hrs', r)
        self.assertIn('road_time_hrs', r)

    def test_fare_estimation_formulas(self):
        """Verify base fares and incremental distance calculations."""
        # 10 km on auto_reserved: base 40 (first 2 km) + 8 km * 14 = 40 + 112 = 152
        fare = estimate_commute_fare('auto_reserved', 10, is_night=False)
        self.assertEqual(fare['total_estimated_fare_inr'], 152)

        # 10 km on auto_reserved at night: 152 + 25% (38) = 190
        fare_night = estimate_commute_fare('auto_reserved', 10, is_night=True)
        self.assertEqual(fare_night['total_estimated_fare_inr'], 190)

        # e_rickshaw: 2 km base 10
        e_fare = estimate_commute_fare('e_rickshaw', 2, is_night=False)
        self.assertEqual(e_fare['total_estimated_fare_inr'], 10)

    def test_transport_api_hubs(self):
        """Test /api/v1/transport/hubs endpoint."""
        res = self.client.get('/api/v1/transport/hubs')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('airports', data['hubs'])
        self.assertIn('railway_junctions', data['hubs'])

    def test_transport_api_estimate_fare(self):
        """Test /api/v1/transport/estimate-fare endpoint."""
        res = self.client.get('/api/v1/transport/estimate-fare?vehicle_type=cab_hatchback&distance_km=10')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['fare_estimate']['total_estimated_fare_inr'], 0)


if __name__ == '__main__':
    unittest.main()