# HiddenYatra — Engineering Fixes Log

This document provides a detailed breakdown of all code changes, root causes, file diffs, and verification steps applied during the audit.

---

## 1. Logout Route Method Flexibility (`FIX-01`)
- **Root Cause**: `@auth_bp.route('/logout', methods=['POST'])` rejected `GET` requests, causing `405 Method Not Allowed` exceptions during direct navigation or redirects.
- **Affected File**: `routes/auth.py` (Line 376)
- **Fix Applied**: Updated decorator to `@auth_bp.route('/logout', methods=['GET', 'POST'])`.
- **Verification**: Executed `e2e_verify.py` — `/logout` returns `302 Found` redirect cleanly.

## 2. Admin Logout Route Method Flexibility (`FIX-02`)
- **Root Cause**: `@admin_bp.route('/logout', methods=['POST'])` rejected `GET` requests from admin toolbar logout buttons.
- **Affected File**: `routes/admin.py` (Line 130)
- **Fix Applied**: Updated decorator to `@admin_bp.route('/logout', methods=['GET', 'POST'])`.
- **Verification**: Tested admin logout navigation link — returns `302 Found` redirect to index cleanly.

## 3. Admin Login True Black AMOLED Dark Theme (`FIX-03`)
- **Root Cause**: Fragile inline `<style>` tags in `login.html` prevented higher-specificity global dark theme styles from overriding card backgrounds.
- **Affected Files**: `templates/admin/login.html`, `static/css/admin.css`, `static/css/admin.min.css`
- **Fix Applied**: Linked `admin.min.css?v=10` via `extra_css` block in `login.html` and added high-specificity `html[data-theme="dark"] .hy-light-login-wrapper` selectors with `#000000` backgrounds.
- **Verification**: Captured live browser DevTools screenshot and computed styles (`backgroundColor: rgb(0,0,0)`).

## 4. Asset Minification & Cache Busting (`FIX-04`)
- **Root Cause**: Browsers served cached `v=9` CSS files containing old color definitions.
- **Affected Files**: `templates/base.html`, `templates/admin/login.html`, all 13 minified `.min.css`/`.min.js` files.
- **Fix Applied**: Ran `scripts/tools/minify_assets.py` and bumped asset version query string to `?v=10`.
- **Verification**: HTTP GET on `http://127.0.0.1:5000/static/css/admin.min.css?v=10` returned status `200 OK` with fresh rules.

## 5. Blueprint Unit Test Expansion (`FIX-05`)
- **Root Cause**: `routes/community.py`, `routes/reviews.py`, `routes/user_photos.py`, and `routes/wishlist.py` lacked dedicated unit test modules.
- **Affected Files**: `tests/test_community.py`, `tests/test_reviews.py`, `tests/test_user_photos.py`, `tests/test_wishlist.py`.
- **Fix Applied**: Created 4 new test files extending `unittest.TestCase`.
- **Verification**: Executed `python -m unittest discover tests` — **106 tests passed**.
