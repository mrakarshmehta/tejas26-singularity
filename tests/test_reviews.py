import unittest
from app import create_app

class ReviewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_reviews_nonexistent(self):
        response = self.client.get('/api/places/99999/reviews')
        self.assertIn(response.status_code, [200, 404])

if __name__ == '__main__':
    unittest.main()
