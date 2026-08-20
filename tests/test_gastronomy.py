"""
Unit and API Integration Tests for Bihar Culinary Heritage & Gastronomy Trails
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.gastronomy import (
    get_all_dishes,
    get_dish_by_slug,
    get_dishes_by_district,
    get_dishes_by_dietary,
    get_gi_tagged_dishes,
    get_culinary_trails
)


class TestGastronomyModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_dishes_present(self):
        """Verify presence of signature heritage delicacies."""
        dishes = get_all_dishes()
        self.assertGreaterEqual(len(dishes), 6)
        slugs = [d['slug'] for d in dishes]
        self.assertIn('litti-chokha', slugs)
        self.assertIn('silao-khaja', slugs)
        self.assertIn('gaya-tilkut', slugs)
        self.assertIn('mithila-makhana-kheer', slugs)
        self.assertIn('bihari-sattu-sherbet', slugs)

    def test_gi_tagged_dishes(self):
        """Verify GI certification filters."""
        gi_dishes = get_gi_tagged_dishes()
        self.assertGreaterEqual(len(gi_dishes), 2)
        gi_slugs = [d['slug'] for d in gi_dishes]
        self.assertIn('silao-khaja', gi_slugs)
        self.assertIn('mithila-makhana-kheer', gi_slugs)

    def test_dietary_filtering(self):
        """Verify dietary tag filters."""
        vegan = get_dishes_by_dietary('vegan')
        self.assertGreaterEqual(len(vegan), 2)
        gluten_free = get_dishes_by_dietary('gluten-free')
        self.assertGreaterEqual(len(gluten_free), 2)

    def test_district_filtering(self):
        """Verify filtering dishes by regional origin."""
        nalanda_dishes = get_dishes_by_district('Nalanda')
        self.assertGreaterEqual(len(nalanda_dishes), 1)
        self.assertTrue(any(d['slug'] == 'silao-khaja' for d in nalanda_dishes))

    def test_culinary_trails(self):
        """Verify regional food trails."""
        trails = get_culinary_trails()
        self.assertGreaterEqual(len(trails), 2)
        for t in trails:
            self.assertIn('title', t)
            self.assertIn('dishes_included', t)
            self.assertIn('duration_days', t)

    def test_gastronomy_api(self):
        """Test /api/v1/gastronomy endpoints."""
        res = self.client.get('/api/v1/gastronomy/dishes')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single dish detail
        res_detail = self.client.get('/api/v1/gastronomy/dishes/litti-chokha')
        self.assertEqual(res_detail.status_code, 200)
        dish_data = res_detail.get_json()
        self.assertEqual(dish_data['status'], 'success')
        self.assertEqual(dish_data['dish']['slug'], 'litti-chokha')

        # Trails API
        res_trails = self.client.get('/api/v1/gastronomy/trails')
        self.assertEqual(res_trails.status_code, 200)
        trails_data = res_trails.get_json()
        self.assertEqual(trails_data['status'], 'success')
        self.assertGreater(len(trails_data['trails']), 0)


if __name__ == '__main__':
    unittest.main()