# HiddenYatra — Root Directory Cleanup Plan

There are currently **106 files** directly in `D:\HiddenYatra` root.  
To establish a clean, professional production repository, root files are systematically divided into **Essential Files to Keep in Root** and **Files to Reorganize**.

---

## 1. Files That MUST Remain in Root (13 Files)

| Filename | Category | Purpose | Why It Must Stay in Root |
| :--- | :---: | :--- | :--- |
| `app.py` | Configuration | Main Flask application entry point | Standard Flask invocation, WSGI entry point, dev server runner |
| `config.py` | Configuration | Application configuration settings | Core settings imported by `app.py` and across models |
| `requirements.txt` | Configuration | Python package dependency manifest | Standard pip installer target (`pip install -r requirements.txt`) |
| `.env` | Configuration | Local environment secrets & DB credentials | Loaded automatically by python-dotenv from root directory |
| `.env.example` | Configuration | Environment configuration template | Public onboarding template for developers |
| `.env.production.example` | Configuration | Production environment template | Deployment reference for cloud environments |
| `Dockerfile` | Deployment | Docker container specification | Standard Docker build context (`docker build -t hiddenyatra .`) |
| `docker-compose.yml` | Deployment | Multi-container orchestration | Standard Docker Compose orchestration target |
| `render.yaml` | Deployment | Cloud deployment specification | Render.com infrastructure as code configuration |
| `gunicorn.conf.py` | Deployment | Gunicorn WSGI production configuration | Production web server configuration file |
| `wsgi.py` | Deployment | WSGI callable proxy for web servers | Production server entry point |
| `my.ini` | Configuration | Local MySQL 8.4 engine configuration | MySQL daemon configuration file |
| `.gitignore` | Configuration | Git version control exclusions | Git root repository configuration |
| `.dockerignore` | Configuration | Docker build context exclusions | Docker build context configuration |
| `README.md` | Documentation | Primary project documentation & guide | Repository landing page and onboarding documentation |

---

## 2. Files to Relocate (93 Files)

| Filename | Category | Current Size | Recommended Destination | Rationale |
| :--- | :---: | :---: | :--- | :--- |
| `BIHAR_BATCH4_APPROVAL_PREVIEW.csv` | Generated Report | 7.6 KB | `data/research/batches/` | Historical research preview table |
| `BIHAR_BATCH4_APPROVAL_PREVIEW.md` | Generated Report | 23.7 KB | `docs/batches/` | Historical batch documentation log |
| `BIHAR_BATCH4_SOURCE_LOG.md` | Generated Report | 12.6 KB | `docs/batches/` | Batch 4 institutional source documentation |
| `BIHAR_BATCH5_APPROVAL_PREVIEW.csv` | Generated Report | 6.4 KB | `data/research/batches/` | Historical research preview table |
| `BIHAR_BATCH5_APPROVAL_PREVIEW.md` | Generated Report | 25.5 KB | `docs/batches/` | Historical batch documentation log |
| `BIHAR_BATCH5_SOURCE_LOG.md` | Generated Report | 8.8 KB | `docs/batches/` | Batch 5 institutional source documentation |
| `BIHAR_BATCH6_APPROVAL_PREVIEW.csv` | Generated Report | 8.2 KB | `data/research/batches/` | Historical research preview table |
| `BIHAR_BATCH6_APPROVAL_PREVIEW.md` | Generated Report | 35.1 KB | `docs/batches/` | Historical batch documentation log |
| `BIHAR_BATCH6_OVERLAP_AUDIT.csv` | Generated Report | 9.5 KB | `data/research/batches/` | Spatial distance overlap audit table |
| `BIHAR_BATCH6_SOURCE_LOG.md` | Generated Report | 11.4 KB | `docs/batches/` | Batch 6 institutional source documentation |
| `BIHAR_BATCH7_APPROVAL_PREVIEW.csv` | Generated Report | 9.7 KB | `data/research/batches/` | Historical research preview table |
| `BIHAR_BATCH7_APPROVAL_PREVIEW.md` | Generated Report | 32.0 KB | `docs/batches/` | Historical batch documentation log |
| `BIHAR_BATCH7_CANDIDATE_STATUS.csv` | Generated Report | 10.1 KB | `data/research/batches/` | Candidate reconciliation status table |
| `BIHAR_BATCH7_OVERLAP_AUDIT.csv` | Generated Report | 16.0 KB | `data/research/batches/` | Spatial distance overlap audit table |
| `BIHAR_BATCH7_SOURCE_LOG.md` | Generated Report | 18.8 KB | `docs/batches/` | Batch 7 institutional source documentation |
| `BIHAR_BATCH8_APPROVAL_PREVIEW.csv` | Generated Report | 8.1 KB | `data/research/batches/` | Historical research preview table |
| `BIHAR_BATCH8_APPROVAL_PREVIEW.md` | Generated Report | 20.4 KB | `docs/batches/` | Historical batch documentation log |
| `BIHAR_BATCH8_CANDIDATE_STATUS.csv` | Generated Report | 7.1 KB | `data/research/batches/` | Candidate reconciliation status table |
| `BIHAR_BATCH8_OVERLAP_AUDIT.csv` | Generated Report | 4.7 KB | `data/research/batches/` | Spatial distance overlap audit table |
| `BIHAR_BATCH8_SOURCE_LOG.md` | Generated Report | 14.8 KB | `docs/batches/` | Batch 8 institutional source documentation |
| `BIHAR_BATCH9_APPROVAL_PREVIEW.csv` | Generated Report | 8.6 KB | `data/research/batches/` | Active Batch 9 preview table |
| `BIHAR_BATCH9_APPROVAL_PREVIEW.md` | Generated Report | 23.9 KB | `docs/batches/` | Active Batch 9 preview documentation |
| `BIHAR_BATCH9_CANDIDATE_STATUS.csv` | Generated Report | 7.3 KB | `data/research/batches/` | Active Batch 9 candidate status table |
| `BIHAR_BATCH9_DISTRICT_CATEGORY_ANALYSIS.md` | Generated Report | 6.4 KB | `docs/batches/` | Active Batch 9 balance analysis |
| `BIHAR_BATCH9_OVERLAP_AUDIT.csv` | Generated Report | 4.7 KB | `data/research/batches/` | Active Batch 9 spatial overlap audit |
| `BIHAR_BATCH9_SOURCE_LOG.md` | Generated Report | 16.5 KB | `docs/batches/` | Active Batch 9 authoritative sources |
| `BIHAR_38_DISTRICT_PLACE_AUDIT.md` | Generated Report | 262.1 KB | `docs/audits/` | Comprehensive 38-district baseline audit |
| `BIHAR_PHASE2_VERIFICATION_REPORT.md`| Generated Report | 224.6 KB | `docs/audits/` | Phase 2 full regression report |
| `POST_BATCH1_REGRESSION_REPORT.md` | Generated Report | 14.7 KB | `docs/audits/` | Post-Batch 1 verification report |
| `POST_BATCH2_REGRESSION_REPORT.md` | Generated Report | 13.3 KB | `docs/audits/` | Post-Batch 2 verification report |
| `POST_BATCH3_REGRESSION_REPORT.md` | Generated Report | 14.1 KB | `docs/audits/` | Post-Batch 3 verification report |
| `POST_BATCH4_REGRESSION_REPORT.md` | Generated Report | 12.8 KB | `docs/audits/` | Post-Batch 4 verification report |
| `POST_BATCH5_REGRESSION_REPORT.md` | Generated Report | 13.6 KB | `docs/audits/` | Post-Batch 5 verification report |
| `POST_BATCH6_REGRESSION_REPORT.md` | Generated Report | 18.6 KB | `docs/audits/` | Post-Batch 6 verification report |
| `POST_BATCH7_REGRESSION_REPORT.md` | Generated Report | 14.5 KB | `docs/audits/` | Post-Batch 7 verification report |
| `POST_BATCH8_REGRESSION_REPORT.md` | Generated Report | 18.2 KB | `docs/audits/` | Post-Batch 8 verification report |
| `UIUX_AUDIT_REPORT.md` | Generated Report | 31.8 KB | `docs/audits/` | Full UI/UX audit report |
| `UIUX_AUDIT_SUMMARY.md` | Generated Report | 12.2 KB | `docs/audits/` | UI/UX executive summary |
| `UIUX_FIX_REPORT.md` | Generated Report | 16.0 KB | `docs/audits/` | UI/UX repairs documentation |
| `MAP_FIX_CHANGELOG.md` | Documentation | 11.3 KB | `docs/architecture/` | GIS & Map fixes log |
| `MAP_FIX_TEST_REPORT.md` | Generated Report | 16.1 KB | `docs/audits/` | GIS Map test validation report |
| `FINAL_ENGINEERING_REPORT.md` | Documentation | 8.3 KB | `docs/` | Engineering milestone summary |
| `FINAL_PRE_SUBMISSION_AUDIT.md` | Generated Report | 17.3 KB | `docs/audits/` | Pre-submission system audit |
| `CHANGELOG.md` | Documentation | 3.5 KB | `docs/` | Platform release notes changelog |
| `API_DOCUMENTATION.md` | Documentation | 7.5 KB | `docs/architecture/` | REST API contract documentation |
| `DEPLOYMENT.md` | Documentation | 1.7 KB | `docs/deployment/` | Production deployment guide |
| `INSTALL.md` | Documentation | 1.5 KB | `docs/` | Local installation instructions |
| `SECURITY_REPORT.md` | Generated Report | 2.8 KB | `docs/audits/` | Application security audit |
| `PERFORMANCE_REPORT.md` | Generated Report | 1.8 KB | `docs/audits/` | Performance benchmark audit |
| `BIHAR_PLACE_MASTER_CANDIDATES.csv` | Data / Seed | 117.6 KB | `data/research/master/` | Master candidate dataset |
| `BIHAR_PRIORITY_APPROVAL_QUEUE.csv` | Data / Seed | 66.3 KB | `data/research/master/` | Master priority candidate queue |
| `BIHAR_APPROVAL_READY_MASTER.csv` | Data / Seed | 159.7 KB | `data/research/master/` | Consolidated approved candidate queue |
| `PHASE5_MASTER_CANDIDATE_QUEUE.csv` | Data / Seed | 57.3 KB | `data/research/master/` | Phase 5 candidate queue |
| `backup_active_db_20260808.sql` | Database Dump | 83.3 KB | `archive/db_backups/` | Historical database snapshot |
| `backup_old_hiddenyatra_recovered.sql`| Database Dump | 319.1 KB | `archive/db_backups/` | Historical database snapshot |
| `backup_pre_phase3_20260809.sql` | Database Dump | 324.6 KB | `archive/db_backups/` | Historical database snapshot |
| `backup_pre_phase32_20260809.sql` | Database Dump | 360.9 KB | `archive/db_backups/` | Historical database snapshot |
| `hiddenyatra_OLD_RECOVERY_FULL.sql` | Database Dump | 319.1 KB | `archive/db_backups/` | Historical database snapshot |
| `mysql_data_BACKUP_20260809_team_setup.sql`| Database Dump | 365.6 KB | `archive/db_backups/` | Historical database snapshot |
| `HiddenYatra_Updated_Presentation.pptx`| Documentation | 18.9 MB | `docs/presentations/` | Pitch deck presentation |
| `TeamSingularity.pptx` | Documentation | 27.4 MB | `docs/presentations/` | Team Hackathon presentation |
| `mysql84_start_log.txt` | Temporary / Debug| 1.1 KB | `archive/logs/` | MySQL startup log output |
| `mysql84_stderr.log` | Temporary / Debug| 1.1 KB | `archive/logs/` | MySQL stderr log output |
