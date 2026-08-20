"""
Unit tests for Admin Audit Logger and Telemetry Security
"""
import unittest
from flask import Flask
from models.admin_db import format_audit_log_entry
from routes.admin import admin_bp


class TestAdminAuditAndTelemetry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.secret_key = 'test-admin-secret-key'
        cls.app.register_blueprint(admin_bp)

    def setUp(self):
        self.client = self.app.test_client()

    def test_format_audit_log_entry(self):
        entry = format_audit_log_entry(
            admin_id=1,
            action_type='APPROVE_SUBMISSION',
            target_type='place_submission',
            target_id=42,
            details={'reason': 'verified historic place'}
        )
        self.assertEqual(entry['admin_id'], 1)
        self.assertEqual(entry['action'], 'APPROVE_SUBMISSION')
        self.assertEqual(entry['target_id'], 42)
        self.assertIn('timestamp', entry)

    def test_system_telemetry_unauthenticated_redirect(self):
        """Unauthenticated requests must redirect to admin login."""
        res = self.client.get('/admin/api/system-telemetry')
        self.assertEqual(res.status_code, 302)
        self.assertIn('/admin/login', res.headers.get('Location', ''))

    def test_system_telemetry_authenticated_access(self):
        """Authenticated admin sessions receive system health metrics."""
        with self.client.session_transaction() as sess:
            sess['admin_logged_in'] = True

        res = self.client.get('/admin/api/system-telemetry')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('python_version', data)
        self.assertIn('platform', data)


if __name__ == '__main__':
    unittest.main()