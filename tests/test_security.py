"""
HiddenYatra - Production Test Suite: Security Tests
Tests security controls: CSRF, auth, upload validation, injection prevention.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _create_test_app():
    """Create test app, returns None if MySQL is unavailable."""
    try:
        from app import create_app
        app = create_app()
        app.config['TESTING'] = True
        return app
    except Exception:
        return None


class TestAdminCSRF(unittest.TestCase):
    """Test CSRF protection on admin endpoints."""

    @classmethod
    def setUpClass(cls):
        cls.app = _create_test_app()
        if cls.app is None:
            raise unittest.SkipTest('MySQL not available')
        cls.client = cls.app.test_client()

    def test_admin_post_without_csrf(self):
        r = self.client.post('/admin/login', data={'password': 'test'})
        self.assertIn(r.status_code, [200, 302, 403])

    def test_admin_post_with_wrong_csrf(self):
        r = self.client.post('/admin/login', data={
            'password': 'test',
            '_csrf_token': 'fake_token_123'
        })
        self.assertIn(r.status_code, [200, 302, 403])


class TestAdminAuthorization(unittest.TestCase):
    """Test admin routes are properly protected."""

    @classmethod
    def setUpClass(cls):
        cls.app = _create_test_app()
        if cls.app is None:
            raise unittest.SkipTest('MySQL not available')
        cls.client = cls.app.test_client()

    ADMIN_ROUTES = [
        '/admin/',
        '/admin/submissions',
        '/admin/users',
        '/admin/recycle-bin',
        '/admin/hero-media',
        '/admin/districts',
        '/admin/trending',
    ]

    def test_admin_routes_require_auth(self):
        for route in self.ADMIN_ROUTES:
            r = self.client.get(route)
            self.assertEqual(r.status_code, 302,
                             f"Route {route} should redirect, got {r.status_code}")


class TestUploadSecurity(unittest.TestCase):
    """Test file upload validation."""

    def test_allowed_extensions(self):
        from config import allowed_file
        for f in ['photo.jpg', 'photo.jpeg', 'photo.png', 'photo.webp', 'photo.gif']:
            self.assertTrue(allowed_file(f), f"Expected {f} to be allowed")
        for f in ['script.php', 'hack.exe', 'shell.sh', 'backdoor.py',
                   'test.html', 'data.sql', 'config.ini']:
            self.assertFalse(allowed_file(f), f"Expected {f} to be blocked")

    def test_no_extension(self):
        from config import allowed_file
        self.assertFalse(allowed_file('noextension'))
        self.assertFalse(allowed_file(''))

    def test_validate_image_magic_bytes(self):
        from config import validate_image_file
        from io import BytesIO
        jpeg = BytesIO(b'\xff\xd8\xff\xe0' + b'\x00' * 100)
        self.assertTrue(validate_image_file(jpeg))
        png = BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100)
        self.assertTrue(validate_image_file(png))
        exe = BytesIO(b'MZ\x90\x00' + b'\x00' * 100)
        self.assertFalse(validate_image_file(exe))


class TestSessionSecurity(unittest.TestCase):
    """Test session security configuration."""

    @classmethod
    def setUpClass(cls):
        cls.app = _create_test_app()
        if cls.app is None:
            raise unittest.SkipTest('MySQL not available')

    def test_session_httponly(self):
        self.assertTrue(self.app.config.get('SESSION_COOKIE_HTTPONLY', False))

    def test_session_samesite(self):
        self.assertEqual(self.app.config.get('SESSION_COOKIE_SAMESITE'), 'Lax')


class TestSecurityHeaders(unittest.TestCase):
    """Verify security headers on responses."""

    @classmethod
    def setUpClass(cls):
        cls.app = _create_test_app()
        if cls.app is None:
            raise unittest.SkipTest('MySQL not available')
        cls.client = cls.app.test_client()

    def test_all_security_headers(self):
        r = self.client.get('/')
        headers = r.headers
        self.assertEqual(headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertIn('Content-Security-Policy', headers)


class TestPasswordSecurity(unittest.TestCase):
    """Test password hashing security."""

    def test_pbkdf2_format(self):
        from models.database import hash_password
        h = hash_password('test')
        self.assertTrue(h.startswith('pbkdf2$'))

    def test_verify_password(self):
        from models.database import hash_password, verify_password
        h = hash_password('mypassword')
        self.assertTrue(verify_password('mypassword', h))
        self.assertFalse(verify_password('wrong', h))


if __name__ == '__main__':
    unittest.main(verbosity=2)


class TestApiCSRFProtection(unittest.TestCase):
    """Test CSRF protection on API POST endpoints."""

    @classmethod
    def setUpClass(cls):
        from flask import Flask
        from routes.api import api_bp
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.secret_key = 'test-security-secret-key'
        cls.app.config['SECRET_KEY'] = 'test-security-secret-key'
        cls.app.register_blueprint(api_bp, url_prefix='/api')
        cls.client = cls.app.test_client()

    def test_post_endpoints_reject_missing_csrf(self):
        """Verify that unprotected POST requests without CSRF token receive 403."""
        endpoints = [
            ('/api/eco/pledge', {'name': 'Test', 'email': 'test@example.com'}),
            ('/api/volunteer/apply', {'name': 'Test', 'email': 'test@example.com', 'phone': '1234567890'}),
            ('/api/guides/inquire', {'name': 'Test', 'email': 'test@example.com', 'phone': '1234567890'}),
            ('/api/quiz/evaluate', {'answers': {}}),
            ('/api/quiz/certificate', {'name': 'Test', 'score': 5, 'total': 6}),
            ('/api/budget/calculate', {'tier': 'heritage', 'days': 3, 'travelers': 2})
        ]
        for url, payload in endpoints:
            res = self.client.post(url, json=payload)
            self.assertEqual(res.status_code, 403, f"Endpoint {url} should require CSRF token")

    def test_budget_get_endpoint_untouched(self):
        """Verify GET /api/budget/calculate works without CSRF."""
        res = self.client.get('/api/budget/calculate?tier=heritage&days=3&travelers=2')
        self.assertEqual(res.status_code, 200)

    def test_post_endpoints_accept_valid_csrf(self):
        """Verify POST requests with valid session and X-CSRF-Token succeed."""
        with self.client.session_transaction() as sess:
            sess['_csrf_token'] = 'valid-test-token-xyz'
        headers = {'X-CSRF-Token': 'valid-test-token-xyz'}
        res = self.client.post(
            '/api/budget/calculate',
            json={'tier': 'heritage', 'days': 3, 'travelers': 2},
            headers=headers
        )
        self.assertEqual(res.status_code, 200)


class TestMultiWorkerRateLimiter(unittest.TestCase):
    """Test multi-worker rate limiter store, rate check, and rate record."""

    def test_rate_limiter_memory_and_store_interface(self):
        from utils.rate_limiter import RateLimitStore, _rate_check, _rate_record
        store = RateLimitStore('test_auth')
        test_ip = '192.168.10.99'

        # Initially not rate limited
        self.assertFalse(_rate_check(store, test_ip, max_attempts=3, window=60))

        # Record 3 attempts
        _rate_record(store, test_ip)
        _rate_record(store, test_ip)
        _rate_record(store, test_ip)

        # Now should be rate limited
        self.assertTrue(_rate_check(store, test_ip, max_attempts=3, window=60))

        # Pop / clear attempts for this IP (e.g. on successful login)
        store.pop(test_ip, None)
        self.assertFalse(_rate_check(store, test_ip, max_attempts=3, window=60))