"""
Unit and API Integration Tests for Rural Immersion & Cultural Volunteerism
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.volunteer import (
    get_all_programs,
    get_program_by_slug,
    get_programs_by_district,
    calculate_skill_match_score,
    validate_volunteer_application
)


class TestVolunteerModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.secret_key = 'test-secret-key'
        cls.app.config['SECRET_KEY'] = 'test-secret-key'
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_programs_catalog(self):
        """Verify rural immersion programs listing."""
        progs = get_all_programs()
        self.assertGreaterEqual(len(progs), 4)
        slugs = [p['slug'] for p in progs]
        self.assertIn('madhubani-art-guild-residency', slugs)
        self.assertIn('organic-makhana-wetland-exchange', slugs)
        self.assertIn('nalanda-heritage-docent-program', slugs)
        self.assertIn('tharu-tribal-eco-village-exchange', slugs)

    def test_program_lookup_by_slug(self):
        """Verify program lookup and district filtering."""
        madhubani = get_program_by_slug('madhubani-art-guild-residency')
        self.assertIsNotNone(madhubani)
        self.assertEqual(madhubani['district'], 'Madhubani')

        m_progs = get_programs_by_district('Madhubani')
        self.assertGreaterEqual(len(m_progs), 1)

    def test_skill_matching_engine(self):
        """Verify skill match scoring logic."""
        score = calculate_skill_match_score(['Digital Photography', 'Art History Interest'], 'madhubani-art-guild-residency')
        self.assertGreater(score, 30)

    def test_application_validation(self):
        """Verify input validation rules."""
        valid, msg = validate_volunteer_application(
            "Ananya Sen",
            "ananya@example.com",
            "+919876543210",
            "madhubani-art-guild-residency",
            "I have 5 years experience in photography and want to document village artisans."
        )
        self.assertTrue(valid)

        # Invalid short name
        invalid_name, _ = validate_volunteer_application("", "a@b.com", "12345678", "madhubani-art-guild-residency", "Motivation text here")
        self.assertFalse(invalid_name)

        # Invalid email
        invalid_email, _ = validate_volunteer_application("Valid Name", "bad-email", "12345678", "madhubani-art-guild-residency", "Motivation text here")
        self.assertFalse(invalid_email)

    def test_volunteer_api_endpoints(self):
        """Test /api/v1/volunteer endpoints."""
        res = self.client.get('/api/v1/volunteer/programs')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Application POST API
        payload = {
            "name": "Priya Sharma",
            "email": "priya@example.com",
            "phone": "+919123456780",
            "program_slug": "organic-makhana-wetland-exchange",
            "skills": "Outdoor Physical Fitness, Agricultural Interest",
            "motivation": "Passionate about sustainable agro-tourism and supporting local farmer cooperatives."
        }
        with self.client.session_transaction() as sess:
            sess['_csrf_token'] = 'test-token-123'
        res_post = self.client.post('/api/v1/volunteer/apply', json=payload, headers={'X-CSRF-Token': 'test-token-123'})
        self.assertEqual(res_post.status_code, 200)
        post_data = res_post.get_json()
        self.assertEqual(post_data['status'], 'success')
        self.assertIn('application_id', post_data)
        self.assertGreater(post_data['skill_match_score_pct'], 0)


if __name__ == '__main__':
    unittest.main()