# HiddenYatra — Architectural Refactoring Plan

This document outlines long-term structural refactoring initiatives to enhance maintainability, modularity, and testability.

---

## 1. Planned Refactoring Initiatives

1. **Service Layer Abstraction (`models/services.py`)**:
   - Extract raw SQL queries in `models/services.py` into dedicated model repository classes (e.g. `PlaceRepository`, `DistrictRepository`, `NearbyServiceRepository`).
   - Standardize return types using Python `dataclasses` or `Pydantic` models instead of raw dictionaries.

2. **PEP 484 Type Annotation Coverage**:
   - Add explicit Python type hints across all utility modules (`utils/security.py`, `utils/image.py`, `utils/slugs.py`).

3. **Database Migration Engine**:
   - Migrate database schema management from raw SQL files (`scripts/migrations/mysql_schema.sql`) to Flask-Migrate / Alembic for automated revision control.

4. **Modular Admin Blueprint Decomposition**:
   - Split `routes/admin.py` (1400+ lines) into modular sub-blueprints: `admin_places.py`, `admin_districts.py`, `admin_users.py`, `admin_submissions.py`, `admin_appearance.py`.
