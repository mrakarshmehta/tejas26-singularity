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

def test_submission_status_meta(self):
        """Verify status meta returns correct labels and editability."""
        from models.places import get_submission_status_meta
        pending = get_submission_status_meta('pending')
        self.assertEqual(pending['label'], 'Under Review')
        self.assertTrue(pending['can_edit'])

        approved = get_submission_status_meta('approved')
        self.assertEqual(approved['label'], 'Published')
        self.assertFalse(approved['can_edit'])

if __name__ == '__main__':
    unittest.main()
