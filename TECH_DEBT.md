# HiddenYatra — Technical Debt & Limitations Registry

This document records architectural items, deployment constraints, and external dependencies that cannot safely be modified automatically.

---

## 1. Development WSGI Server Execution (`TD-01`)
- **Category**: Deployment / Infrastructure
- **Description**: Local execution relies on Flask's built-in Werkzeug development web server.
- **Status**: Production VPS deployment requires Gunicorn or uWSGI behind Nginx (`gunicorn wsgi:app` configured in `docker-compose.yml` and `gunicorn.conf.py`).
- **Verification Status**: VERIFIED in Dockerfile and Compose setup. Local standalone execution NOT VERIFIED for Gunicorn.

## 2. Database Migration Engine (`TD-02`)
- **Category**: Database Management
- **Description**: Database schema changes currently rely on raw SQL migration scripts in `scripts/migrations/`.
- **Status**: Integrating Alembic / Flask-Migrate is recommended for long-term schema migration tracking.
- **Verification Status**: MySQL raw schema initialization VERIFIED. Automated migration rollbacks NOT VERIFIED.
