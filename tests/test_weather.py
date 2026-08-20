"""
Unit and API Integration Tests for Bihar Weather, Microclimate & AQI Advisory
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.weather import (
    get_all_district_weather,
    get_district_weather_by_slug,
    classify_aqi_level,
    get_seasonal_packing_advice,
    AQI_LEVELS
)


class TestWeatherModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_district_weather_database(self):
        """Verify district meteorological profiles."""
        districts = get_all_district_weather()
        self.assertGreaterEqual(len(districts), 5)
        slugs = [d['slug'] for d in districts]
        self.assertIn('patna', slugs)
        self.assertIn('gaya', slugs)
        self.assertIn('nalanda', slugs)
        self.assertIn('west-champaran', slugs)
        self.assertIn('rohtas', slugs)

    def test_aqi_classification_ranges(self):
        """Verify AQI classification helper."""
        good = classify_aqi_level(40)
        self.assertEqual(good['label'], 'Good')

        mod = classify_aqi_level(150)
        self.assertEqual(mod['label'], 'Moderate')

        poor = classify_aqi_level(250)
        self.assertEqual(poor['label'], 'Poor')

        invalid = classify_aqi_level('invalid_data')
        self.assertEqual(invalid['label'], 'Unknown')

    def test_seasonal_packing_advice(self):
        """Verify packing advice generator based on month and microclimate."""
        winter_advice = get_seasonal_packing_advice('patna', 12)
        self.assertEqual(winter_advice['season_detected'], 'winter')
        self.assertIn('woolens', winter_advice['recommendation'].lower())

        monsoon_advice = get_seasonal_packing_advice('rohtas', 7)
        self.assertEqual(monsoon_advice['season_detected'], 'monsoon')
        self.assertIn('boots', monsoon_advice['recommendation'].lower())

    def test_weather_api_endpoints(self):
        """Test /api/v1/weather API endpoints."""
        res = self.client.get('/api/v1/weather/districts')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single district detail
        res_detail = self.client.get('/api/v1/weather/districts/gaya')
        self.assertEqual(res_detail.status_code, 200)
        detail_data = res_detail.get_json()
        self.assertEqual(detail_data['status'], 'success')
        self.assertEqual(detail_data['weather']['district'], 'Gaya')

        # Packing advice API
        res_pack = self.client.get('/api/v1/weather/packing-advice?district=patna&month=1')
        self.assertEqual(res_pack.status_code, 200)
        pack_data = res_pack.get_json()
        self.assertEqual(pack_data['status'], 'success')
        self.assertEqual(pack_data['advice']['season_detected'], 'winter')


if __name__ == '__main__':
    unittest.main()