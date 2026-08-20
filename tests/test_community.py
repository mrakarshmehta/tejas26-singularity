import unittest
from app import create_app
from models.database import get_db

class CommunityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_suggest_place_get(self):
        response = self.client.get('/suggest')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Suggest', response.data)

    def test_my_submissions_anonymous_redirect(self):
        response = self.client.get('/my-submissions')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
