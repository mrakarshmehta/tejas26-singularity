# HiddenYatra — Known Limitations & Unverified Features

This document provides a realistic, evidence-based list of operational constraints, deployment requirements, and features that cannot be verified automatically.

---

## 1. WSGI Web Server (Production Execution)
- **Constraint**: The local test environment runs on Flask's built-in Werkzeug development web server (`app.py`).
- **Production Requirement**: Production deployment on a Linux VPS requires running Gunicorn (`gunicorn wsgi:app`) with Nginx reverse proxy.
- **Verification Status**:
  - Werkzeug development server: **VERIFIED**
  - Gunicorn execution in Docker container: **NOT VERIFIED** (requires live Docker runtime daemon)

## 2. Database Migration Rollback Engine
- **Constraint**: Schema modifications currently rely on raw SQL migration scripts in `scripts/migrations/mysql_schema.sql`.
- **Recommendation**: Integrating Flask-Migrate / Alembic for structured schema revision history.
- **Verification Status**:
  - Direct MySQL schema execution: **VERIFIED**
  - Automated migration rollback tracking: **NOT VERIFIED**

## 3. Third-Party Leaflet Map Tiles
- **Constraint**: Map view tile loading relies on OpenStreetMap (`https://*.tile.openstreetmap.org`) and CartoDB tile servers.
- **Verification Status**:
  - OpenStreetMap tiles: **VERIFIED** (Requires active internet connection on client browser)
