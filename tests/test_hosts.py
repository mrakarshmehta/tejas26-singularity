"""
Unit tests for Host & Homestay Booking Logic
"""
import unittest
from datetime import date, timedelta
from models.hosts import validate_stay_dates, check_listing_capacity, calculate_stay_pricing

class TestHostBooking(unittest.TestCase):

    def test_valid_date_range(self):
        today = date.today()
        cin = (today + timedelta(days=2)).strftime('%Y-%m-%d')
        cout = (today + timedelta(days=5)).strftime('%Y-%m-%d')
        is_valid, err, nights = validate_stay_dates(cin, cout)
        self.assertTrue(is_valid)
        self.assertIsNone(err)
        self.assertEqual(nights, 3)

    def test_past_check_in_date_fails(self):
        cin = '2020-01-01'
        cout = '2020-01-05'
        is_valid, err, _ = validate_stay_dates(cin, cout)
        self.assertFalse(is_valid)
        self.assertIn('past', err.lower())

    def test_pricing_calculation(self):
        quote = calculate_stay_pricing(price_per_night=1000, nights=3, guests=2)
        self.assertEqual(quote['base_stay_amount'], 3000)
        self.assertEqual(quote['nights'], 3)
        self.assertGreater(quote['total_amount'], 3000)

    def test_capacity_check(self):
        valid, _ = check_listing_capacity(max_guests=4, requested_guests=3)
        self.assertTrue(valid)
        invalid, _ = check_listing_capacity(max_guests=2, requested_guests=5)
        self.assertFalse(invalid)

if __name__ == '__main__':
    unittest.main()
