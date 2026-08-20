"""
Unit and API Integration Tests for Multi-Currency Trip Budget Planner
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.budget_planner import (
    calculate_trip_budget,
    convert_currency,
    get_all_currencies,
    get_all_travel_tiers
)


class TestBudgetPlannerModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_currencies_database(self):
        """Verify supported global currencies."""
        currencies = get_all_currencies()
        self.assertIn('INR', currencies)
        self.assertIn('USD', currencies)
        self.assertIn('EUR', currencies)
        self.assertIn('JPY', currencies)

    def test_travel_tiers(self):
        """Verify presence of budget tiers."""
        tiers = get_all_travel_tiers()
        self.assertIn('backpacker', tiers)
        self.assertIn('heritage', tiers)
        self.assertIn('luxury', tiers)
        self.assertGreater(tiers['luxury']['daily_rate_inr'], tiers['backpacker']['daily_rate_inr'])

    def test_budget_calculation(self):
        """Verify trip budget calculation formulas."""
        # 3 days, 2 travelers, heritage tier (₹4,500/day/person)
        # Expected total: 4500 * 3 * 2 = 27000 INR
        budget = calculate_trip_budget('heritage', 3, 2, 'INR')
        self.assertEqual(budget['total_amount_inr'], 27000)
        self.assertEqual(budget['total_amount'], 27000)
        self.assertIn('stay', budget['itemized_breakdown'])

        # In USD
        usd_budget = calculate_trip_budget('heritage', 3, 2, 'USD')
        self.assertGreater(usd_budget['total_amount'], 0)
        self.assertEqual(usd_budget['currency'], 'USD')

    def test_budget_api_endpoints(self):
        """Test /api/v1/budget API endpoints."""
        res = self.client.get('/api/v1/budget/calculate?tier=luxury&days=5&travelers=2&currency=EUR')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['budget']['tier'], 'luxury')
        self.assertEqual(data['budget']['currency'], 'EUR')

        # Tiers API
        res_tiers = self.client.get('/api/v1/budget/tiers')
        self.assertEqual(res_tiers.status_code, 200)
        self.assertEqual(res_tiers.get_json()['status'], 'success')

        # Currencies API
        res_curr = self.client.get('/api/v1/budget/currencies')
        self.assertEqual(res_curr.status_code, 200)
        self.assertEqual(res_curr.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()

class TestDistrictCostIndex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_district_cost_factors(self):
        """Verify district price multipliers."""
        from models.budget_planner import get_district_cost_index, get_district_adjusted_budget
        index = get_district_cost_index()
        self.assertIn('patna', index)
        self.assertIn('madhubani', index)

        patna_cost = get_district_adjusted_budget(1000, 'patna')
        self.assertGreater(patna_cost, 1000)

        madhubani_cost = get_district_adjusted_budget(1000, 'madhubani')
        self.assertLess(madhubani_cost, 1000)

    def test_cost_index_api(self):
        """Test /api/v1/budget/district-cost-index endpoint."""
        res = self.client.get('/api/v1/budget/district-cost-index')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(data['count'], 4)

class TestTippingAndCashGuidelines(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_tipping_guidelines_data(self):
        """Verify tipping guidelines list."""
        from models.budget_planner import get_tipping_and_cash_guidelines
        tips = get_tipping_and_cash_guidelines()
        self.assertGreaterEqual(len(tips), 3)
        services = [t['service'] for t in tips]
        self.assertTrue(any('Guides' in s for s in services))
        self.assertTrue(any('UPI' in s for s in services))

    def test_tipping_api(self):
        """Test /api/v1/budget/tipping-guidelines endpoint."""
        res = self.client.get('/api/v1/budget/tipping-guidelines')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(data['count'], 3)