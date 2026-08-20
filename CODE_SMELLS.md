# HiddenYatra — Code Smells Analysis Report

This document records code smells, structural anti-patterns, and readability observations identified during static codebase analysis.

---

## 1. Identified Code Smells

1. **Large Handler Function Bodies in `routes/admin.py`**:
   - Several admin view functions perform template context assembly, database updates, file system ops, and audit logging within a single function body.
   - *Recommendation*: Extract business logic into dedicated helper functions or service class methods.

2. **Inline SQL String Placeholders**:
   - Queries in `models/admin_db.py` use multiline strings. While safe against SQL injection due to `%s` tuple parameterization, formatting with `textwrap.dedent` or repository methods improves readability.

3. **Global State Cache in `app.py`**:
   - `_auth_appearance_cache` uses an in-memory dictionary. Under multi-worker Gunicorn deployments, each worker maintains its own isolated memory cache.
   - *Recommendation*: Use Redis for distributed cache invalidation across workers.
