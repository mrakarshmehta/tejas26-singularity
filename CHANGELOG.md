## [v2.4.0] - 2026-08-20
### Added
- Multi-day itinerary pacing configurations and travel budget estimation engine.
- Homestay date availability validation and dynamic stay pricing calculator.
- Community submission review workflows and helpful review vote toggles.
- Haversine proximity radius calculator and custom category SVG map markers.
- PWA offline navigation fallback with dedicated offline guide route.
- Admin structured audit logging and live telemetry metrics.
- Password complexity verification and OTP sliding-window rate limiting.

# HiddenYatra — Changelog

All notable changes to the HiddenYatra project are documented in this file.

---

## [1.2.0] — 2026-08-06

### Added
- Created `AUDIT.md`, `FIXES.md`, `TECH_DEBT.md`, and `CHANGELOG.md` to establish a complete technical audit documentation suite.
- Added 4 new automated test modules: `tests/test_community.py`, `tests/test_reviews.py`, `tests/test_user_photos.py`, and `tests/test_wishlist.py`, expanding the unit test suite to 106 tests.
- Created `scripts/tools/db_integrity_audit.py` for automated MySQL database health checks.

### Fixed
- Fixed `/logout` and `/admin/logout` route method handlers in `routes/auth.py` and `routes/admin.py` to allow both `GET` and `POST` requests.
- Fixed Admin Login page dark mode styling by purging inline styles and adding scoped `html[data-theme="dark"]` rules in `admin.css`.
- Synchronized asset cache-busting query parameter `?v=10` across template asset links.
- Re-minified 13 static CSS/JS asset bundles.

### Security
- Verified OWASP Top 10 compliance: SQL query parameterization, Jinja autoescaping, CSRF token validation, rate limiting, and HTTP security response headers (`CSP`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`).
