import unittest
from app import create_app

class WishlistTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_wishlist_page(self):
        response = self.client.get('/wishlist')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
