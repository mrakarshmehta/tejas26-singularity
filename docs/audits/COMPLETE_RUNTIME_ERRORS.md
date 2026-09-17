# HiddenYatra — Complete Runtime Errors & Defect Catalog

**Project:** `D:\HiddenYatra`  
**Audit Mode:** Read-Only / Forensic Failure Analysis  
**Protocol:** Strictly Documenting Discovered Defects (Zero Fixes Applied)  
**Date:** 2026-09-17  

---

## 1. Defect Classification Summary

| Issue ID | Severity | Category | Affected Subsystem | Defect Summary |
| :---: | :---: | :---: | :--- | :--- |
| **ERR-01** | **CRITICAL** | Code / Runtime | `routes/main.py` | Missing `abort` import; triggers 500 error on unmapped slugs |
| **ERR-02** | **CRITICAL** | Code / Runtime | `routes/host.py` | Missing `abort` import; triggers 500 error on unmapped host IDs |
| **ERR-03** | **MEDIUM** | Media / Data | `static/uploads/places/` | 9 place photo records in DB point to files missing on disk (404 in console) |
| **ERR-04** | **LOW** | Media / Mock | `static/uploads/hosts/` | 3 demo stay listings reference placeholder cover images missing on disk |
| **ERR-05** | **LOW** | External / CDN | `https://cdnjs.cloudflare.com` | Three.js CDN script blocked in offline/sandbox headless runs |
| **ERR-06** | **LOW** | Python Runtime | `models/admin_db.py:580` | `datetime.datetime.utcnow()` deprecation warning |
| **ERR-07** | **INFORMATIONAL**| Scripts / Path | `scripts/` | 69 historical scripts reference obsolete `scratch/` dump paths |

---

## 2. Detailed Forensic Analysis

### ERR-01: NameError on `abort(404)` in `routes/main.py`
- **Severity:** **CRITICAL**
- **Trigger:** Calling any entity detail route in `routes/main.py` with an invalid or non-existent slug.
- **Observed Routes:**
  - `/archaeology/<slug>`
  - `/circuit/<slug>`
  - `/craft/<slug>`
  - `/festival/<slug>`
  - `/gastronomy/<slug>`
  - `/guides/<slug>`
  - `/intellectual-heritage/<slug>`
  - `/performing-arts/<slug>`
  - `/souvenirs/<slug>`
  - `/treks/<slug>`
  - `/virtual-tour/<slug>`
  - `/weather/<slug>`
  - `/wildlife/<slug>`
- **Observed Traceback:**
  ```text
  File "routes/main.py", line 420, in virtual_tour_viewer
    abort(404)
  NameError: name 'abort' is not defined
  ```
- **Root Cause:** Line 2 of `routes/main.py` contains `from flask import Blueprint, render_template, request`. The identifier `abort` was not included in the import list.
- **Remediation Required (Post-Audit):** Update import statement to `from flask import Blueprint, render_template, request, abort`.

---

### ERR-02: NameError on `abort(404)` in `routes/host.py`
- **Severity:** **CRITICAL**
- **Trigger:** Requesting a host profile or listing ID that does not exist or has been soft-deleted.
- **Root Cause:** Line 5 of `routes/host.py` imports `Blueprint, render_template, request, redirect, url_for, flash, session, jsonify`, omitting `abort`.
- **Remediation Required (Post-Audit):** Add `abort` to the `from flask import (...)` tuple in `routes/host.py`.

---

### ERR-03: Missing Uploaded Photo Files for Database Places
- **Severity:** **MEDIUM**
- **Observed 404 URLs:**
  - `/static/uploads/places/88_8d6a2e08.jpg`
  - `/static/uploads/places/18_62928207.jpg`
  - `/static/uploads/places/15_e4a95edb.jpg`
  - `/static/uploads/places/14_b7d64066.jpg`
  - `/static/uploads/places/17_b740209f.jpg`
  - `/static/uploads/places/92_8b31ff60.jpg`
  - `/static/uploads/places/90_1a9b8ca2.jpg`
  - `/static/uploads/places/23_648d33c8.jpg`
  - `/static/uploads/places/110_1338d68d.jpg`
- **Root Cause:** Historical seed scripts created place records pointing to generated image filenames that were either removed or not checked into git.
- **UI Impact:** The frontend falls back gracefully to CSS gradient cards, but browser console logs 404 errors.

---

### ERR-04: Missing Demo Stay Listing Covers
- **Severity:** **LOW**
- **Observed 404 URLs:**
  - `/static/uploads/hosts/listings/stay_demo_madhubani_cover.jpg`
  - `/static/uploads/hosts/listings/stay_demo_bhagalpur_cover.jpg`
  - `/static/uploads/hosts/listings/stay_demo_simultala_cover.jpg`
- **Root Cause:** Mock listings seeded into the stays database reference example filenames.

---

### ERR-05: Offline Sandbox Failure for Three.js CDN
- **Severity:** **LOW**
- **Observed Log:** `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js - Failed to load resource: net::ERR_FAILED`
- **Root Cause:** When running headless browser tests in an offline/firewalled container, external CDN requests fail.
- **Remediation Recommendation:** Vendor `three.min.js` locally in `static/js/vendor/` to allow full 3D offline PWA functionality.

---

### ERR-06: `datetime.utcnow()` Deprecation Warning
- **Severity:** **LOW**
- **Trace:** `models/admin_db.py:580: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version.`
- **Root Cause:** Python 3.12+ deprecated `utcnow()` in favor of `datetime.now(datetime.UTC)`.

---

### ERR-07: Obsolete `scratch/` References in Non-Production Scripts
- **Severity:** **INFORMATIONAL**
- **Breakdown:** 69 total occurrences: 58 in `scripts/archive/`, 8 in `scripts/maintenance/`, 3 in `scripts/testing/`.
- **Root Cause:** Artifacts from past interactive development sessions prior to Phase 2 filesystem reorganization.
