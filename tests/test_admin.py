"""
Unit tests for Admin Audit Logger and Telemetry Helpers
"""
import unittest
from models.admin_db import format_audit_log_entry

class TestAdminAudit(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
