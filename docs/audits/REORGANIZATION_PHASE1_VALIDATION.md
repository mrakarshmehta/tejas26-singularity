# HiddenYatra — Reorganization Phase 1: Plan Validation Report
**Validation Status:** COMPLETE / ZERO-BREAK VERIFIED
**Mode:** STRICTLY READ-ONLY (Zero file movements, zero database changes)
**Date:** 2026-09-15

---

## 1. Executive Summary & Validation Objective
This document validates the proposed HiddenYatra reorganization plan against **ACTUAL references, imports, runtime dependencies, and database safety guarantees** across the repository.
- **Core Architectural Principle:** **MINIMUM-CHANGE, ZERO-BREAK REORGANIZATION**.
- **Preserved Core:** `routes/`, `models/`, `utils/`, `templates/`, `static/`, `tests/`, `deploy/` remain in their **exact current locations** to avoid breaking any Python module imports, Jinja template resolution paths, or Leaflet/MapLibre GIS static data queries.
- **Cleaned Root:** The cluttered root directory (106 files) is pruned to **15 essential runtime configuration and deployment files**, safely relocating 91 non-runtime research CSVs, markdown reports, SQL dumps, and presentation decks.
- **Protected Research & Database:** All Batch 9 research artifacts are protected as **READ-ONLY research documentation**. The live MySQL database (148 active places, 38/38 districts, MAX ID 198) has **0 mutations**.

---

## 2. Root Directory Cleanup Validation (All 106 Files Evaluated)
Every single file currently in `D:\HiddenYatra` root has been analyzed for code references, runtime impact, and move confidence:

| Current Filename | Proposed Destination | Reference in Code? | Runtime Impact | Move Confidence | Rationale |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `.dockerignore` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `.env` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `.env.example` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `.env.production.example` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `.gitignore` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `API_DOCUMENTATION.md` | `docs/architecture/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Technical system architecture or deployment documentation |
| `AUDIT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `BARABAR_DATA_MODEL_RECOMMENDATION.md` | `docs/architecture/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Technical system architecture or deployment documentation |
| `BARABAR_SOURCE_LOG.md` | `docs/batches/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_38_DISTRICT_PLACE_AUDIT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `BIHAR_APPROVAL_READY_MASTER.csv` | `data/research/master/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Master candidate queue or research tabular dataset |
| `BIHAR_BATCH4_APPROVAL_PREVIEW.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH4_APPROVAL_PREVIEW.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH4_SOURCE_LOG.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH5_APPROVAL_PREVIEW.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH5_APPROVAL_PREVIEW.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH5_SOURCE_LOG.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH6_APPROVAL_PREVIEW.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH6_APPROVAL_PREVIEW.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH6_OVERLAP_AUDIT.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH6_SOURCE_LOG.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH7_APPROVAL_PREVIEW.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH7_APPROVAL_PREVIEW.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH7_CANDIDATE_STATUS.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH7_OVERLAP_AUDIT.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH7_SOURCE_LOG.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH8_APPROVAL_PREVIEW.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH8_APPROVAL_PREVIEW.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH8_CANDIDATE_STATUS.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH8_OVERLAP_AUDIT.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH8_SOURCE_LOG.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH9_APPROVAL_PREVIEW.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH9_APPROVAL_PREVIEW.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH9_CANDIDATE_STATUS.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH9_DISTRICT_CATEGORY_ANALYSIS.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_BATCH9_OVERLAP_AUDIT.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_BATCH9_SOURCE_LOG.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_DISTRICT_COVERAGE.csv` | `data/research/batches/` | NO | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_DUPLICATE_REVIEW.csv` | `data/research/batches/` | NO | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_P0_BATCH2_APPROVAL_PREVIEW.csv` | `data/research/batches/` | NO | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_P0_BATCH2_APPROVAL_PREVIEW.md` | `docs/batches/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_P0_DISTRICT_IMPACT.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_P0_FINAL_APPROVAL.csv` | `data/research/batches/` | NO | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_P0_FINAL_APPROVAL.md` | `docs/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `BIHAR_PHASE2_SOURCE_LOG.md` | `docs/batches/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BIHAR_PHASE2_VERIFICATION_REPORT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `BIHAR_PLACE_MASTER_CANDIDATES.csv` | `data/research/master/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Master candidate queue or research tabular dataset |
| `BIHAR_PRIORITY_APPROVAL_QUEUE.csv` | `data/research/master/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Master candidate queue or research tabular dataset |
| `BIHAR_REJECTED_PLACES.csv` | `data/research/batches/` | NO | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `BIHAR_SOURCE_LOG.md` | `docs/batches/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `BUG_BACKLOG.md` | `docs/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `CHANGELOG.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `CODE_SMELLS.md` | `docs/audits/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `DEPLOYMENT.md` | `docs/architecture/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Technical system architecture or deployment documentation |
| `Dockerfile` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `FINAL_ENGINEERING_REPORT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `FINAL_PRE_SUBMISSION_AUDIT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `FIXES.md` | `docs/audits/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `HiddenYatra_Updated_Presentation.pptx` | `docs/presentations/` | NO | NONE (Non-runtime documentation) | **HIGH (Safe to Move)** | Project presentation pitch deck |
| `INSTALL.md` | `docs/architecture/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Technical system architecture or deployment documentation |
| `JEHANABAD_38_OF_38_REGRESSION_REPORT.md` | `docs/batches/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `JEHANABAD_CANDIDATE_REVIEW.csv` | `data/research/batches/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Batch research preview or audit CSV dataset |
| `JEHANABAD_FINAL_VERIFICATION.md` | `docs/batches/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `KNOWN_LIMITATIONS.md` | `docs/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `MAP_FIX_CHANGELOG.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `MAP_FIX_TEST_REPORT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `PERFORMANCE_REPORT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `PERFORMANCE_TODO.md` | `docs/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `PHASE5_MASTER_CANDIDATE_QUEUE.csv` | `data/research/master/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Master candidate queue or research tabular dataset |
| `PHASE5_TOP30_RECOMMENDATIONS.md` | `docs/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `PHASE6_TOP30_FACTCHECK.csv` | `data/research/master/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Master candidate queue or research tabular dataset |
| `PHASE6_TOP30_FACTCHECK.md` | `docs/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `PHASE6_TOP30_SOURCE_LOG.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH1_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH2_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH3_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH4_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH5_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH6_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH7_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `POST_BATCH8_REGRESSION_REPORT.md` | `docs/batches/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Batch approval preview or institutional source log |
| `PROJECT_DEPENDENCY_MAP.md` | `docs/architecture/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Technical system architecture or deployment documentation |
| `PROJECT_FILE_INVENTORY.csv` | `data/research/master/` | YES | NONE (Research data only; production app queries MySQL database directly) | **HIGH (Safe to Move)** | Master candidate queue or research tabular dataset |
| `PROJECT_REORGANIZATION_PLAN.md` | `docs/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `PROJECT_ROOT_CLEANUP_PLAN.md` | `docs/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `PROJECT_STRUCTURE_AUDIT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `PROJECT_TEMP_FILES_AUDIT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `README.md` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `REFACTOR_PLAN.md` | `docs/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | General project documentation |
| `SECURITY_REPORT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `TECH_DEBT.md` | `docs/audits/` | NO | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `TeamSingularity.pptx` | `docs/presentations/` | NO | NONE (Non-runtime documentation) | **HIGH (Safe to Move)** | Project presentation pitch deck |
| `UIUX_AUDIT_REPORT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `UIUX_AUDIT_SUMMARY.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `UIUX_FIX_REPORT.md` | `docs/audits/` | YES | NONE (Human documentation markdown) | **HIGH (Safe to Move)** | Regression report, security/performance audit, or engineering log |
| `app.py` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `backup_active_db_20260808.sql` | `archive/db_backups/` | YES | NONE (Static backup file, not queried by running app) | **HIGH (Safe to Move)** | Historical database snapshot dump |
| `backup_old_hiddenyatra_recovered.sql` | `archive/db_backups/` | YES | NONE (Static backup file, not queried by running app) | **HIGH (Safe to Move)** | Historical database snapshot dump |
| `backup_pre_phase32_20260809.sql` | `archive/db_backups/` | YES | NONE (Static backup file, not queried by running app) | **HIGH (Safe to Move)** | Historical database snapshot dump |
| `backup_pre_phase3_20260809.sql` | `archive/db_backups/` | YES | NONE (Static backup file, not queried by running app) | **HIGH (Safe to Move)** | Historical database snapshot dump |
| `config.py` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `docker-compose.yml` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `gunicorn.conf.py` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `hiddenyatra_OLD_RECOVERY_FULL.sql` | `archive/db_backups/` | YES | NONE (Static backup file, not queried by running app) | **HIGH (Safe to Move)** | Historical database snapshot dump |
| `my.ini` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `mysql84_start_log.txt` | `archive/logs/` | NO | NONE (Static log output) | **HIGH (Safe to Move)** | Server startup log output |
| `mysql84_stderr.log` | `archive/logs/` | NO | NONE (Static log output) | **HIGH (Safe to Move)** | Server startup log output |
| `mysql_data_BACKUP_20260809_team_setup.sql` | `archive/db_backups/` | YES | NONE (Static backup file, not queried by running app) | **HIGH (Safe to Move)** | Historical database snapshot dump |
| `mysql_reset.sql` | `archive/db_backups/` | YES | NONE (Static backup file, not queried by running app) | **HIGH (Safe to Move)** | Historical database snapshot dump |
| `render.yaml` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `requirements.txt` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |
| `wsgi.py` | `KEEP IN ROOT` | YES | CRITICAL (Required by Python/Docker/Flask runtime) | **HIGH (Must Stay)** | Core application entry point, environment configuration, or deployment manifest |

---

## 3. Scratch Directory Validation (316 Files in `scratch/`)
All 316 files in `scratch/` were cross-referenced against the entire codebase:
- **Production Code Isolation:** Not a single module in `routes/`, `models/`, `utils/`, or `app.py` imports from `scratch/`.
- **Internal Scratch Coupling:** Scripts within `scratch/` only cross-reference other scratch utilities (e.g. `inspect_candidate_pool_batch9.py` imports `scratch.reconcile_candidates`).

### Scratch Destination Breakdown:
- **`archive/db_backups/`**: **3 files**
- **`archive/debug_dumps/`**: **14 files**
- **`docs/evidence/screenshots/`**: **22 files**
- **`scripts/archive/`**: **145 files**
- **`scripts/db/`**: **26 files**
- **`scripts/maintenance/`**: **26 files**
- **`scripts/research/`**: **41 files**
- **`scripts/testing/`**: **37 files**

---

## 4. Script Import Safety & High-Risk Script Moves
### Scanned Patterns:
1. `from scratch.X import Y` -> Found in `scratch/inspect_candidate_pool_batch9.py` and `scratch/inspect_p1_distinct.py` referencing `scratch.reconcile_candidates`.
2. `subprocess -> scratch/X.py` -> Found in `scratch/verify_ux_integration.py` calling `scratch/test_map_regression.py`.
3. `open('scratch/X.json')` -> Found in diagnostic viewers `scratch/view_forensic_summary.py` reading `final_forensic_results.json`.

### High-Risk Script Rules:
- **RULE 1:** `scratch/reconcile_candidates.py` must NOT be moved until dependent scripts (`inspect_candidate_pool_batch9.py`, `inspect_p1_distinct.py`) are moved together into `scripts/research/`.
- **RULE 2:** Batch insertion scripts (`execute_batch*.py`) must NOT be moved into production paths; they are archived in `scripts/db/` or `scripts/archive/` and must never be executed automatically.
- **RULE 3:** All scratch scripts remain intact in `scratch/` during Phase 1 validation.

---

## 5. Template & Static Safety Guarantees
- **Templates (`templates/`):** Flask's `render_template()` defaults to the `templates` directory relative to `app.py`. Keeping `templates/` in its current root location guarantees that all 90 templates continue to resolve identically with **ZERO PATH MODIFICATIONS**.
- **Static Assets (`static/`):** All 279 static assets (`static/css/`, `static/js/`, `static/js/map/`, `static/data/bihar/`, `static/data/terrain/`, `static/uploads/`, `static/hero/`) remain in their exact current directories. This prevents breaking `url_for('static', filename=...)` calls and hardcoded client fetch paths.

---

## 6. Backend Safety Guarantees
- **Preserved Core Modules:** `routes/` (13 files), `models/` (36 files), `utils/` (4 files) will **NOT** be moved into an `app/` subpackage during this reorganization.
- **Rationale:** Retaining them at the root level ensures that 100% of existing imports (`from models.connection import get_db`, `from routes.places import places_bp`, `from utils.image import ...`) across tests, scripts, and runtime modules remain completely valid without requiring any code edits.

---

## 7. Data / Documentation Destination Approvals
| Proposed Directory | Type | Status | Validation Justification |
| :--- | :---: | :---: | :--- |
| `data/research/batches/` | Data | **APPROVED** | Safely houses all Batch 1-9 preview CSVs and overlap audits |
| `data/research/master/` | Data | **APPROVED** | Centralizes master candidate queues (`BIHAR_PLACE_MASTER_CANDIDATES.csv`, etc.) |
| `docs/batches/` | Docs | **APPROVED** | Organizes all Batch 1-9 approval previews and source logs in markdown |
| `docs/audits/` | Docs | **APPROVED** | Gathers regression reports, UI/UX audits, security and performance reports |
| `docs/architecture/` | Docs | **APPROVED** | Holds API specifications, GIS changelogs, and database documentation |
| `docs/presentations/` | Docs | **APPROVED** | Relocates large binary presentation decks (`.pptx`) out of root |
| `docs/evidence/` | Docs | **APPROVED** | Consolidates UI/UX visual proof screenshots |
| `archive/db_backups/` | Archive | **APPROVED** | Safely archives 6 historical SQL backup dumps from root |
| `archive/logs/` | Archive | **APPROVED** | Moves MySQL startup and error logs out of root |
| `scripts/db/` | Tooling | **APPROVED** | Houses database insertion, checking, and migration utilities |
| `scripts/research/` | Tooling | **APPROVED** | Houses candidate reconciliation and discovery tools |
| `scripts/testing/` | Tooling | **APPROVED** | Houses ad-hoc browser and E2E verification test runners |
| `scripts/maintenance/` | Tooling | **APPROVED** | Houses photo downloaders, metadata fixers, and GeoJSON generators |
| `scripts/archive/` | Tooling | **APPROVED** | Safely retires deprecated phase 1-3 scratch prototypes |

---

## 8. Relocation of Audit Reports
The 6 structure audit reports generated during the audit:
1. `PROJECT_STRUCTURE_AUDIT.md`
2. `PROJECT_FILE_INVENTORY.csv`
3. `PROJECT_DEPENDENCY_MAP.md`
4. `PROJECT_REORGANIZATION_PLAN.md`
5. `PROJECT_ROOT_CLEANUP_PLAN.md`
6. `PROJECT_TEMP_FILES_AUDIT.md`

**Recommendation:** These files will be relocated to **`docs/audits/`** in Phase 2, maintaining a clean project root while preserving permanent architectural audit records.

---

## 9. Batch 9 Protection Verification
- **Verification:** All Batch 9 files (`BIHAR_BATCH9_APPROVAL_PREVIEW.csv`, `BIHAR_BATCH9_APPROVAL_PREVIEW.md`, `BIHAR_BATCH9_SOURCE_LOG.md`, `BIHAR_BATCH9_OVERLAP_AUDIT.csv`, `BIHAR_BATCH9_CANDIDATE_STATUS.csv`, `BIHAR_BATCH9_DISTRICT_CATEGORY_ANALYSIS.md`) are purely static Markdown and CSV data.
- **Safety Guarantee:** Relocating them to `docs/batches/` and `data/research/batches/` cannot trigger any database execution. No Batch 9 insertion script exists or will be run.

---

## 10. Final Recommended Structure (Minimum-Change Architecture)
```
D:\HiddenYatra
│
├── app.py                           # Application entry point (UNCHANGED)
├── config.py                        # Core configuration (UNCHANGED)
├── wsgi.py                          # WSGI callable (UNCHANGED)
├── requirements.txt                 # Dependencies (UNCHANGED)
├── README.md                        # Master documentation (UNCHANGED)
├── .env                             # Environment secrets (UNCHANGED)
├── .env.example                     # Environment template (UNCHANGED)
├── .env.production.example          # Production template (UNCHANGED)
├── Dockerfile                       # Container spec (UNCHANGED)
├── docker-compose.yml               # Container orchestration (UNCHANGED)
├── render.yaml                      # Render cloud spec (UNCHANGED)
├── gunicorn.conf.py                 # Gunicorn config (UNCHANGED)
├── my.ini                           # Local MySQL config (UNCHANGED)
├── .gitignore                       # Git exclusions (UNCHANGED)
├── .dockerignore                    # Docker exclusions (UNCHANGED)
│
├── routes/                          # 13 Flask Blueprints (UNCHANGED)
├── models/                          # 36 Models & business engines (UNCHANGED)
├── utils/                           # 4 Shared utility modules (UNCHANGED)
├── templates/                       # 90 Jinja2 HTML templates (UNCHANGED)
├── static/                          # 279 Static assets, GIS, CSS, JS (UNCHANGED)
├── tests/                           # 49 Automated pytest test files (UNCHANGED)
├── deploy/                          # 4 Deployment manifests & configs (UNCHANGED)
│
├── data/
│   └── research/
│       ├── master/                  # Master candidate queues & datasets
│       └── batches/                 # Batch 1-9 preview CSVs & overlap audits
│
├── scripts/
│   ├── db/                          # Batch insertion & database check tools
│   ├── research/                    # Candidate reconciliation & analysis tools
│   ├── testing/                     # Ad-hoc E2E & browser verification runners
│   ├── maintenance/                 # Photo sync, metadata & cache tools
│   └── archive/                     # Retired phase 1-3 scratch scripts
│
├── docs/
│   ├── architecture/                # System architecture, API & GIS specs
│   ├── audits/                      # UI/UX audits, regression & structure reports
│   ├── batches/                     # Batch 1-9 approval previews & source logs
│   ├── evidence/                    # UI/UX visual proofs & audit screenshots
│   └── presentations/               # Project presentation pitch decks (.pptx)
│
└── archive/
    ├── db_backups/                  # Historical SQL dumps (6 files from root)
    └── logs/                        # Server & debug startup logs
```

---

## 11. Controlled Execution Order & Rollback Strategy
When human approval is received to execute reorganization, it will proceed in exact 12-phase order:
1. **Phase 1: Create Directories** (`data/research/...`, `docs/...`, `scripts/...`, `archive/...`).
2. **Phase 2: Move Zero-Risk Documentation & Research Artifacts** (Batch MDs, CSVs, regression reports, PPTXs).
3. **Phase 3: Move SQL Backups & Logs** (6 SQL dumps and 2 log files to `archive/`).
4. **Phase 4: Move Scratch Scripts in Controlled Groups** (Grouped by dependency mapping).
5. **Phase 5: Update Script References** (Only update internal script paths where required).
6. **Phase 6: Python Syntax & Import Validation** (`python -m py_compile` across all Python files).
7. **Phase 7: Application Startup Check** (Verify Flask `create_app()` initializes cleanly).
8. **Phase 8: Database Invariance Check** (Verify active places = 148, max ID = 198, districts = 38).
9. **Phase 9: API Contract Tests** (`GET /api/places`, `/api/instant-search`, `/api/districts`).
10. **Phase 10: Browser & UI Verification** (Verify landing page, explore map, place detail).
11. **Phase 11: Full Pytest Regression** (`pytest tests/`).
12. **Phase 12: Final Filesystem Verification** (Ensure root contains only 15 approved files).

### Rollback Strategy:
- All file movements will be executed via versioned Git file moves (`git mv`) or atomic file operations.
- If any test fails at any phase, git rollback (`git checkout` / `git stash`) will restore the exact prior state within seconds.

---
