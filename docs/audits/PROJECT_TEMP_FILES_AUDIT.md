# HiddenYatra — Temporary & Debug Files Audit

This document inventories all temporary, diagnostic, generated test outputs, and obsolete files across the project workspace.

---

## 1. Temporary JSON Diagnostic Outputs (`scratch/`)

| Filename | Size | Purpose | Retention Recommendation |
| :--- | :---: | :--- | :--- |
| `audit_dump.json` | 107.8 KB | Place and image inventory snapshot | Archive or purge |
| `final_forensic_results.json` | 110.2 KB | Forensic audit verification output | Archive or purge |
| `interactive_controls_inventory.json`| 118.7 KB | Interactive UI controls scan dump | Archive |
| `e2e_controls_audit_report.json` | 10.2 KB | Automated browser control audit | Archive |
| `homestays_dump.json` | 27.6 KB | Homestays database extraction dump | Move to `data/research/` |
| `live_district_data.json` | 139.5 KB | Scraped live district statistics | Move to `data/research/` |
| `local_district_data.json` | 63.4 KB | Local district comparison data | Move to `data/research/` |
| `batch2_extracted.json` | 13.2 KB | Batch 2 research extraction dump | Archive |
| `batch2_full_md.json` | 20.2 KB | Batch 2 markdown extraction dump | Archive |
| `demo_flow_validation_report.json` | 1.2 KB | Hackathon flow validation log | Archive |

---

## 2. Test Execution Screenshots & Visual Proofs (`scratch/` & `uiux_*/`)

Over 50 PNG and WebP files were generated during automated browser and regression testing:
- Examples: `g4a_01_rajgir_2d.png`, `g4a_02_rajgir_3d_tilt50.png`, `jamui_all_cards_scrolled.png`, `jamui_live_verified.png`.
- **Recommendation:** Consolidate visual test proofs into `docs/evidence/` or `tests/visual_regression/`; purge unneeded one-off test captures.

---

## 3. Server Startup Logs (`D:\HiddenYatra` root)

- `mysql84_start_log.txt` (1.1 KB)
- `mysql84_stderr.log` (1.1 KB)
- **Recommendation:** Relocate to `archive/logs/`.

---

## 4. Legacy Database SQL Snapshots (6 Files in Root)

- Total Size: ~1.8 MB
- Snapshots created prior to major phases (Phase 2, Phase 3, Phase 3.2).
- **Recommendation:** Retain as immutable historical recovery baselines, but move from root to `archive/db_backups/`.
