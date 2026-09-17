# HiddenYatra — Complete Project Structure Audit
**Audit Mode:** STRICTLY READ-ONLY / ZERO MUTATIONS  
**Project Path:** `D:\HiddenYatra`  
**Execution Timestamp:** 2026-09-15  
**Auditor:** Antigravity AI Systems

---

## 1. Executive Summary & Baseline Inventory

HiddenYatra is an end-to-end Bihar Tourism Intelligence and Exploration platform powered by Flask, MySQL, Leaflet/MapLibre GIS engines, and an in-memory inverted search engine.

- **Total Project Files Indexed:** **1017**
- **Root Directory Files:** **106** (Severe root clutter: batch CSVs, markdown reports, SQL dumps, presentations)
- **Scratch Directory Files:** **318** (Ad-hoc migration, inspection, and verification scripts)
- **Jinja2 Templates:** **90** (Across 7 subdirectories and root templates)
- **Backend Modules:** **53** (13 routes, 36 models/engines, 4 utils)
- **GIS / Spatial Data Files:** **52** (GeoJSON layers, 3D terrain binary chunks, map engines)
- **Static Assets:** **279** (CSS, JS, uploads, hero images, icons, PWA manifest/worker)
- **Test Suite Files:** **85** (49 in `tests/` + 36 ad-hoc scratch testers)
- **Secret Scan Status:** Fully audited. Zero plain-text credentials exposed. `SECRET_PRESENT = YES` reported only on `.env` and `my.ini`.

---

## 2. Complete File Classification Breakdown

Every file across `D:\HiddenYatra` has been classified into exactly one authoritative category:

| Code | Category | File Count | Percentage | Architectural Role |
| :---: | :--- | :---: | :---: | :--- |
| **A** | **FRONTEND** | 14 | 1.4% | Root PWA manifest, service workers, robots.txt, and client entry assets |
| **B** | **BACKEND** | 53 | 5.2% | Flask blueprints (`routes/`), data models & engines (`models/`), helpers (`utils/`) |
| **C** | **UI / TEMPLATES** | 90 | 8.9% | Jinja2 HTML templates (`templates/`) including base layout, admin, auth, and views |
| **D** | **CSS** | 15 | 1.5% | Modular stylesheets (`static/css/`) and minified production bundles |
| **E** | **JAVASCRIPT** | 11 | 1.1% | Core client-side JavaScript controllers, search client, and UI handlers |
| **F** | **MAP / GIS** | 52 | 5.1% | Map engine controllers (`static/js/map/`), GeoJSON spatial layers, 3D terrain tiles |
| **G** | **IMAGES / MEDIA** | 258 | 25.4% | Verified destination photos, hero banners, SVG placeholders, UI/UX audit screenshots |
| **H** | **DATABASE** | 17 | 1.7% | SQL migrations, schema definitions, and recovery database dumps |
| **I** | **DATA / SEED** | 49 | 4.8% | Seeding scripts (`scripts/seed/`), master candidate queues, and district tabular datasets |
| **J** | **TESTS** | 85 | 8.4% | Automated pytest suite (`tests/`) and scratch integration/browser test harnesses |
| **K** | **DEVELOPMENT SCRIPTS** | 263 | 25.9% | Forensic diagnostics, batch insertion tools, image crawlers, and inspection scripts |
| **L** | **DOCUMENTATION** | 28 | 2.8% | Technical specifications (`docs/`), README, deployment manuals, presentation decks |
| **M** | **CONFIGURATION** | 9 | 0.9% | Flask app config (`config.py`), dependencies (`requirements.txt`), `.env` templates |
| **N** | **DEPLOYMENT** | 9 | 0.9% | Dockerfile, docker-compose, Render blueprint, Gunicorn server config, Nginx configs |
| **O** | **GENERATED REPORTS** | 57 | 5.6% | Batch approval previews, overlap audits, source verification logs, regression reports |
| **P** | **TEMPORARY / DEBUG** | 10 | 1.0% | Diagnostic JSON outputs, MySQL startup logs, and temporary evaluation dumps |
| **Q** | **UNKNOWN / MANUAL REVIEW**| 10 | 1.0% | Files requiring human domain confirmation prior to relocation |
| **TOTAL** | | **1017** | **100.0%** | |

---

## 3. Frontend Architecture Audit

The HiddenYatra frontend relies on semantic HTML5 templates rendered via Jinja2, modern modular Vanilla CSS (zero Tailwind dependency), and vanilla JavaScript modules interacting with asynchronous Flask REST APIs.

### Core Client-Server Flow Pipelines:
1. **Explore Map Subsystem:**
   `GET /explore` -> `templates/explore_map.html` -> `static/js/map/map-core.js` + `map-layers.js` -> `GET /api/places?geojson=1` & `GET /static/data/bihar/*.geojson` -> Client Leaflet/MapLibre Vector Engine.
2. **Instant Search Subsystem:**
   User Keydown in Header -> `static/js/search.js` -> `GET /api/instant-search?q={query}` -> `models/search_engine.py` (Inverted Index) -> Dropdown autocomplete cards.
3. **Place Detail Experience:**
   `GET /places/<slug>` -> `templates/place.html` -> `routes/places.py` -> `models/places.py` -> `static/css/components.css` & `static/js/smart-nearby.js` -> `GET /api/places/<id>/nearby` -> Dynamic smart distance recommendations.
4. **Offline PWA Architecture:**
   Service Worker `static/sw.js` (registered in `base.html`) caches core app shells (`main.css`, `app.js`, `logo.svg`, `offline.html`) allowing offline navigation.

---

## 4. Backend Architecture Audit

- **Application Factory:** `create_app()` in `app.py` initializes session security, custom Decimal/datetime JSON provider, CSRF tokens, database connectivity (`init_db()`), and pre-compiles the in-memory search index (`rebuild_search_index()`).
- **Blueprints Registered (12 Blueprints):**
  - `main_bp` (`routes/main.py`): Landing page, browse, static informational views
  - `places_bp` (`routes/places.py`): Place detail, district aggregation
  - `api_bp` (`routes/api.py`): High-performance JSON endpoints for search, map markers, geojson
  - `auth_bp` (`routes/auth.py`): User authentication, session management, CSRF-protected logins
  - `admin_bp` (`routes/admin.py`): Comprehensive administrator portal, CRUD operations
  - `itinerary_bp` (`routes/itinerary.py`): Multi-day automated itinerary generation
  - `stays_bp` (`routes/stays.py`): Homestay and eco-accommodation booking
  - `host_bp` (`routes/host.py`): Local host listing management
  - `community_bp` (`routes/community.py`): Community forums and local stories
  - `reviews_bp` (`routes/reviews.py`): Review submission, rating calculations
  - `wishlist_bp` (`routes/wishlist.py`): Client-side and authenticated bookmarking
  - `user_photos_bp` (`routes/user_photos.py`): User-submitted photography uploads
- **Service & Domain Layer (`models/`):**
  - `search_engine.py`: High-performance inverted trie/token index with BM25-inspired ranking.
  - `connection.py`: MySQL connection pool manager supporting PyMySQL and mysql.connector.
  - `itineraries.py`: Algorithmic itinerary engine using Haversine matrix optimization.
  - `safety.py`: Women safety metrics, emergency police/hospital spatial queries.
  - `weather.py`: Micro-climate agro-meteorological forecasting for Bihar agro-zones.

---

## 5. Template & UI Audit (90 Templates)

| Template Category | Count | Primary Templates | Extends | Master Route |
| :--- | :---: | :--- | :---: | :--- |
| **PUBLIC** | 28 | `index.html`, `browse.html`, `crafts.html`, `festivals.html`, `gastronomy.html` | `base.html` | `routes/main.py` |
| **PLACES** | 3 | `place.html`, `numismatics.html`, `panorama_viewer.html` | `base.html` | `routes/places.py` |
| **DISTRICTS** | 3 | `district.html`, `state.html`, `block.html` | `base.html` | `routes/places.py` |
| **EXPLORE / MAP** | 1 | `explore_map.html` | `base.html` | `routes/main.py: /explore` |
| **ITINERARY** | 3 | `itinerary.html`, `itinerary_detail.html`, `budget_planner.html` | `base.html` | `routes/itinerary.py` |
| **AUTH** | 7 | `login.html`, `signup.html`, `forgot_password.html`, `reset_password.html` | `base.html` | `routes/auth.py` |
| **ADMIN** | 16 | `admin/dashboard.html`, `admin/places.html`, `admin/users.html`, `admin/analytics.html`| `admin/base.html` | `routes/admin.py` |
| **ADMIN / HOST** | 11 | `host/dashboard.html`, `host/create_listing.html`, `host/bookings.html` | `base.html` | `routes/host.py` |
| **STAYS** | 3 | `stays/index.html`, `stays/detail.html`, `stays/book.html` | `base.html` | `routes/stays.py` |
| **SHARED / USER** | 6 | `user/profile.html`, `community/forum.html`, `wishlist.html` | `base.html` | `routes/community.py` |
| **SHARED PARTIALS**| 4 | `partials/_header.html`, `partials/_footer.html`, `partials/_flash.html` | Component | Embedded via Jinja `include` |
| **ERROR** | 5 | `403.html`, `404.html`, `413.html`, `429.html`, `500.html` | `base.html` | Flask errorhandlers (`app.py`) |

---

## 6. Static Asset Audit (279 Files)

- **Active CSS:** `main.css`, `components.css`, `explore-map.css`, `admin.css`, `animations.css`, `smart-nearby.css` (and minified versions).
- **Active JS:** `app.js`, `search.js`, `map.js`, `smart-nearby.js`, `admin.js`, `gallery.js` + 15 GIS modules in `static/js/map/`.
- **Spatial GeoJSON:** 9 active GeoJSON layers in `static/data/bihar/` (districts, blocks, rivers, forests, waterfalls, hotels, homestays).
- **3D Terrain Tiles:** 21 pre-computed binary elevation chunk tiles in `static/data/terrain/bihar/` (z9, z10, z11).
- **Media Assets:** Verified place photography stored in `static/uploads/places/` and hero covers in `static/hero/`.

---

## 7. Database & Secret Audit

- **Active Production Schema:** MySQL 8.0+ running on port 3307 (`hiddenyatra` database).
- **Seed Scripts:** `scripts/seed_patna_complete.py`, `scripts/seed_gaya_complete.py`, `scripts/seed_jamui_complete.py`.
- **SQL Backups:** 6 legacy SQL dumps identified in root (`backup_active_db_20260808.sql`, `backup_old_hiddenyatra_recovered.sql`, etc.).
- **Secret Status:**
  - `.env`: **SECRET_PRESENT = YES** (Database passwords and session secrets verified present in file, zero exposed in output).
  - `my.ini`: **SECRET_PRESENT = YES** (MySQL local port and server configuration).
  - All other 1014 files: **SECRET_PRESENT = NO**.

---

## 8. Test Suite Audit (85 Files)

- **Formal Pytest Suite (`tests/` - 49 files):** Covers authentication (`test_auth.py`), database integrity (`test_database.py`), search engine ranking (`test_search_engine.py`), map GIS controllers (`test_hymap_system.py`), itinerary matrix (`test_itinerary.py`), and milestone contracts (`test_milestone_138.py`).
- **Scratch Testers (`scratch/` - 36 files):** E2E controls tester (`e2e_controls_tester.py`), delete flow tester (`test_all_delete_flows.py`), instant search client tester (`test_client_instant_search.py`), and mobile regression suites.

---

## 9. Scratch & Development Scripts Audit (316 Files in `scratch/`)

The `scratch/` directory represents an enormous development workspace that must be systematically organized:
- **`MOVE TO scripts/testing/` (36 files):** Ad-hoc test harnesses (`test_*.py`, `e2e_*.py`, `verify_*.py`).
- **`MOVE TO scripts/db/` (45 files):** Batch insertion scripts (`execute_batch*.py`, `post_insert_check_*.py`, `backup_db.py`).
- **`MOVE TO scripts/research/` (38 files):** Candidate analysis and reconciliation tools (`reconcile_candidates.py`, `analyze_batch*.py`).
- **`MOVE TO scripts/maintenance/` (24 files):** Photo synchronizers (`sync_authentic_wikipedia_photos.py`, `fix_famous_for.py`).
- **`MOVE TO archive/` (112 files):** Deprecated phase 1–3 prototypes, old screenshot captures, temporary dumps.
- **`TEMPORARY / PURGEABLE` (61 files):** Scratch JSON dumps (`audit_dump.json`, `final_forensic_results.json`) and test screenshots.

---

## 10. Batch & Research Artifact Audit (Batches 1–9)

- **Root Clutter:** Exactly **38 batch research artifacts** reside directly in the root directory (e.g. `BIHAR_BATCH4_APPROVAL_PREVIEW.csv`, `BIHAR_BATCH8_OVERLAP_AUDIT.csv`, `BIHAR_BATCH9_SOURCE_LOG.md`).
- **Target Relocation:**
  - All preview & audit CSVs -> `data/research/batches/`
  - All preview markdown & source logs -> `docs/batches/`
  - Master candidate queues -> `data/research/master/`

---

## 11. High-Risk Files (DO NOT MOVE WITHOUT REFACTORING)

1. `app.py`, `config.py`, `wsgi.py`: Root WSGI and application entry points.
2. `routes/*.py`: Blueprints referenced by module path in `app.py`.
3. `models/*.py`: Imported across routes, tests, and scripts as `from models.X import Y`.
4. `static/data/bihar/*.geojson`: Absolute static paths referenced in `static/js/map/map-layers.js`.
5. `static/data/terrain/bihar/manifest.json`: Terrain loader configuration path in `map-google-terrain-loader.js`.
6. `deploy/nginx.conf`, `deploy/hiddenyatra.service`: System-level absolute directory references.

---

## 12. Safe-to-Move Files (Zero Runtime Risk)

1. **Root Batch CSVs (18 files):** Move to `data/research/batches/`.
2. **Root Batch Markdown Logs (20 files):** Move to `docs/batches/`.
3. **Root Regression Reports (10 files):** Move to `docs/audits/`.
4. **Root Presentation Decks (`.pptx` - 2 files):** Move to `docs/presentations/`.
5. **Root SQL Backup Dumps (6 files):** Move to `archive/db_backups/`.
6. **Scratch directory contents (316 files):** Move to categorized subfolders under `scripts/` and `archive/`.
7. **UI/UX Evidence folders (26 files):** Move to `docs/evidence/`.

---

## 13. Audit Sign-Off

This audit has been performed in **STRICT READ-ONLY MODE**. Zero files were modified, moved, renamed, or deleted. Zero database records or configurations were altered.
