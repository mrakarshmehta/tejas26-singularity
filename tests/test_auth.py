"""
Unit tests for Auth Security, Password Complexity & OTP Rate Limiting
"""
import unittest
from utils.email_otp import check_otp_rate_limit
from routes.auth import validate_password_strength

class TestAuthSecurity(unittest.TestCase):

    def test_password_strength_valid(self):
        valid, err = validate_password_strength("SecretPass123")
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_password_strength_short(self):
        valid, err = validate_password_strength("pass1")
        self.assertFalse(valid)
        self.assertIn("8 characters", err)

    def test_password_strength_no_numbers(self):
        valid, err = validate_password_strength("lettersOnlyPass")
        self.assertFalse(valid)

    def test_otp_rate_limiting(self):
        ident = "test_user_rate_limit@example.com"
        ok1, _ = check_otp_rate_limit(ident, max_attempts=2, window_seconds=60)
        ok2, _ = check_otp_rate_limit(ident, max_attempts=2, window_seconds=60)
        ok3, retry = check_otp_rate_limit(ident, max_attempts=2, window_seconds=60)
        self.assertTrue(ok1)
        self.assertTrue(ok2)
        self.assertFalse(ok3)
        self.assertGreater(retry, 0)

if __name__ == '__main__':
    unittest.main()
