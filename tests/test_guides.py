"""
Unit and API Integration Tests for Verified Tour Guides & Booking Inquiries
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.guides import (
    get_all_guides,
    get_guide_by_slug,
    get_guides_by_district,
    get_guides_by_language,
    get_guides_by_specialization,
    validate_guide_inquiry
)


class TestGuidesModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_all_guides_catalog(self):
        """Verify list of certified tourist guides."""
        guides = get_all_guides()
        self.assertGreaterEqual(len(guides), 5)
        slugs = [g['slug'] for g in guides]
        self.assertIn('ven-dharmapala-bodh-gaya', slugs)
        self.assertIn('dr-alok-mishra-nalanda-rajgir', slugs)
        self.assertIn('sunita-devi-mithila-folk-art', slugs)
        self.assertIn('ramesh-tharu-valmiki-safari', slugs)
        self.assertIn('simran-singh-patna-heritage', slugs)

    def test_language_and_district_filtering(self):
        """Verify language proficiencies and district filters."""
        japanese_guides = get_guides_by_language('Japanese')
        self.assertGreaterEqual(len(japanese_guides), 1)
        self.assertEqual(japanese_guides[0]['slug'], 'dr-alok-mishra-nalanda-rajgir')

        gaya_guides = get_guides_by_district('Gaya')
        self.assertGreaterEqual(len(gaya_guides), 1)

    def test_booking_inquiry_validation(self):
        """Verify inquiry input validation rules."""
        valid, msg = validate_guide_inquiry(
            "Amit Kumar",
            "amit@example.com",
            "+919876543210",
            "ven-dharmapala-bodh-gaya",
            "2026-11-20",
            4
        )
        self.assertTrue(valid)

        # Invalid short name
        inv_name, _ = validate_guide_inquiry("", "a@b.com", "12345678", "ven-dharmapala-bodh-gaya", "2026-11-20")
        self.assertFalse(inv_name)

        # Invalid group size
        inv_size, _ = validate_guide_inquiry("Amit", "a@b.com", "12345678", "ven-dharmapala-bodh-gaya", "2026-11-20", -5)
        self.assertFalse(inv_size)

    def test_guides_api_endpoints(self):
        """Test /api/v1/guides API endpoints."""
        res = self.client.get('/api/v1/guides')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Single guide detail
        res_detail = self.client.get('/api/v1/guides/ven-dharmapala-bodh-gaya')
        self.assertEqual(res_detail.status_code, 200)
        detail_data = res_detail.get_json()
        self.assertEqual(detail_data['status'], 'success')
        self.assertEqual(detail_data['guide']['district'], 'Gaya')

        # Inquiry POST endpoint
        inquiry_payload = {
            "name": "Sarah Jenkins",
            "email": "sarah@example.com",
            "phone": "+447911123456",
            "guide_slug": "dr-alok-mishra-nalanda-rajgir",
            "travel_date": "2026-12-05",
            "group_size": 2
        }
        res_inquire = self.client.post('/api/v1/guides/inquire', json=inquiry_payload)
        self.assertEqual(res_inquire.status_code, 200)
        inq_data = res_inquire.get_json()
        self.assertEqual(inq_data['status'], 'success')
        self.assertIn('inquiry_id', inq_data)


if __name__ == '__main__':
    unittest.main()

class TestGuideEthicsStandards(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_ethics_standards_data(self):
        """Verify guide ethics standards list."""
        from models.guides import get_guide_ethics_standards
        standards = get_guide_ethics_standards()
        self.assertGreaterEqual(len(standards), 3)
        titles = [s['standard_title'] for s in standards]
        self.assertTrue(any('Licensing' in t for t in titles))
        self.assertTrue(any('First-Aid' in t for t in titles))

    def test_ethics_api(self):
        """Test /api/v1/guides/ethics API endpoint."""
        res = self.client.get('/api/v1/guides/ethics')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(data['count'], 3)