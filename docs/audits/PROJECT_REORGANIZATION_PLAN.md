# HiddenYatra — Complete Project Reorganization Plan

## 1. Architectural Motivation

HiddenYatra has evolved rapidly across 9 major data batches, resulting in high functional quality but severe root-level clutter and ad-hoc script dispersal:
- Over 100 files sit directly in `D:\HiddenYatra` root.
- Over 300 scripts and outputs sit inside `scratch/`.
- Batch candidate CSVs, approval preview markdown logs, and regression reports are intermingled with production source code.

This plan defines a safe, deterministic, zero-downtime reorganization methodology.

---

## 2. Proposed Target Directory Architecture

```
D:\HiddenYatra
│
├── app/                              # Flask application package
│   ├── __init__.py                   # Application factory (create_app)
│   ├── config.py                     # Configuration settings
│   ├── routes/                       # Blueprints (api, admin, places, auth, etc.)
│   ├── models/                       # Database models and table definitions
│   ├── services/                     # Business logic (search_engine, itineraries, weather)
│   └── utils/                        # Shared helpers (security, image, formatting)
│
├── templates/                        # Jinja2 HTML templates
│   ├── layouts/                      # base.html, admin/base.html
│   ├── public/                       # Landing, browse, crafts, culture views
│   ├── places/                       # place.html, district.html
│   ├── map/                          # explore_map.html
│   ├── itinerary/                    # itinerary.html, budget_planner.html
│   ├── auth/                         # login.html, signup.html, reset.html
│   ├── admin/                        # Admin dashboard and management views
│   ├── partials/                     # Reusable UI fragments (_header, _footer)
│   └── errors/                       # 404.html, 500.html, etc.
│
├── static/                           # Public static web assets
│   ├── css/                          # Stylesheets (modular + minified)
│   ├── js/                           # Client JavaScript & Map engine controllers
│   ├── data/                         # GeoJSON spatial layers & 3D terrain binary chunks
│   ├── images/                       # Brand logos, icons, SVGs, placeholders
│   └── uploads/                      # User and place photo media storage
│
├── data/                             # Data assets and research repository
│   ├── seed/                         # Initial database seed definitions
│   ├── research/                     # Candidate queues and fact-checking tables
│   │   ├── master/                   # BIHAR_PLACE_MASTER_CANDIDATES.csv, etc.
│   │   └── batches/                  # Batch 1-9 preview CSVs and overlap audits
│   └── backups/                      # Historical SQL dumps (migrated from root)
│
├── scripts/                          # Operational & development tooling
│   ├── db/                           # Migrations, seeding, and database checks
│   ├── research/                     # Candidate reconciliation and discovery scripts
│   ├── maintenance/                  # Photo sync, metadata fixes, cache warming
│   └── testing/                      # Ad-hoc E2E test runners and verification tools
│
├── tests/                            # Automated pytest test suite
│   ├── unit/                         # Unit tests (models, utils, search)
│   ├── integration/                  # Route, API, and blueprint integration tests
│   └── e2e/                          # Full workflow and browser tests
│
├── docs/                             # Engineering & project documentation
│   ├── architecture/                 # Architecture, API specs, database dictionary
│   ├── batches/                      # Batch 1-9 preview markdown logs & source logs
│   ├── audits/                       # UI/UX audits, regression reports, forensic logs
│   └── deployment/                   # Server, Docker, and Nginx documentation
│
├── deploy/                           # Deployment manifests & service configs
│   ├── Dockerfile                    # (or keep in root)
│   ├── docker-compose.yml            # (or keep in root)
│   ├── nginx.conf
│   └── hiddenyatra.service
│
├── archive/                          # Retired prototypes, old reports, scratch dumps
│
├── .env                              # Local environment secrets (STAYS IN ROOT)
├── .env.example                      # Environment template (STAYS IN ROOT)
├── requirements.txt                  # Python dependencies (STAYS IN ROOT)
├── app.py                            # Application entry point wrapper (STAYS IN ROOT)
└── README.md                         # Main repository readme (STAYS IN ROOT)
```

---

## 3. Phased Migration Execution Strategy

To eliminate risk to the live MySQL database (148 active destinations) and ensure uninterrupted web service, migration must occur in 5 distinct phases:

### Phase 1: Pure Documentation & Research Consolidation (Risk: ZERO)
- Move all Batch 1–9 Preview and Source Log Markdown files (`BIHAR_BATCH*_SOURCE_LOG.md`, `BIHAR_BATCH*_APPROVAL_PREVIEW.md`) from root to `docs/batches/`.
- Move all Regression and Audit Markdown reports (`POST_BATCH*_REGRESSION_REPORT.md`, `UIUX_*.md`) from root to `docs/audits/`.
- Move presentation files (`*.pptx`) to `docs/presentations/`.
- Move historical SQL dumps (`backup_*.sql`) to `data/backups/`.
- Move batch candidate CSVs (`BIHAR_BATCH*.csv`, `PHASE5_*.csv`) to `data/research/batches/`.

### Phase 2: Scratch Workspace Reorganization (Risk: ZERO)
- Clean up `scratch/`:
  - Move database insertion and check scripts into `scripts/db/`.
  - Move candidate reconciliation tools into `scripts/research/`.
  - Move maintenance scripts (`sync_photos.py`, etc.) into `scripts/maintenance/`.
  - Move ad-hoc test scripts into `tests/scratch_testers/`.
  - Move obsolete scratch JSON outputs into `archive/debug_dumps/`.

### Phase 3: Templates Standardization (Risk: MEDIUM)
- Move error templates (`404.html`, etc.) into `templates/errors/`.
- Update `app.py` errorhandler render calls (`render_template('errors/404.html')`).
- Keep view template names stable to prevent breaking route handlers.

### Phase 4: Application Module Encapsulation (Risk: HIGH)
- Wrap Flask core into an `app/` package, leaving a thin `app.py` proxy in root:
  ```python
  # root app.py proxy
  from app import create_app
  app = create_app()
  if __name__ == '__main__':
      app.run()
  ```
- Separate services (`search_engine.py`, `itineraries.py`, `weather.py`) from database models (`places.py`, `districts.py`).

### Phase 5: Post-Reorganization Regression Verification
- Run complete test suite: `pytest tests/`.
- Verify database invariance: Active places count must remain exactly 148, Max ID 198, Districts 38.
- Verify map rendering, search auto-complete, and place detail views via browser subagent.
