import unittest
from app import create_app

class UserPhotosTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_user_photos(self):
        response = self.client.get('/place/1/upload-photo')
        # GET on POST-only upload endpoint returns 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
