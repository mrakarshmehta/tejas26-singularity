# HiddenYatra — Media Restoration Forensic Analysis Report
**Project:** `D:\HiddenYatra`  
**Phase:** Media Restoration Forensic Analysis (Read-Only)  
**Protocol:** Strict Read-Only Analysis / No Database or Code Mutations  
**Date:** 2026-09-17  
**Status:** **ANALYSIS COMPLETE — WAITING FOR HUMAN REVIEW**

---

## Executive Summary

A comprehensive, forensic investigation into all missing media references across the HiddenYatra project was conducted.

### Current Verified Baseline:
- **Active Places in Database (`deleted_at IS NULL`):** `148`
- **Maximum Place ID (`MAX(id)`):** `198`
- **Districts Represented:** `38/38`
- **Active Places with Valid Local Image on Disk:** `24`
- **Active Places with Non-Empty `cover_image` Missing from Disk:** `39`
- **Active Places with Empty `cover_image` String:** `85`
- **Mock Stay Images Under Investigation:** `3` (`stay_rajgir.jpg`, `stay_bodhgaya.jpg`, `stay_valmiki.jpg`)
- **Total Registered Project Images in Repository:** `246` (excluding `.git`)
- **Database Status:** Strictly invariant. Zero `UPDATE`, `INSERT`, or `DELETE` operations performed.

---

## 1. Complete Missing Cover Image Inventory (39 Active Places)

The table below documents every active place record in MySQL where `cover_image` references a filename not present in `static/uploads/places/`.

| Place ID | Place Name | Slug | District | Current `cover_image` | Expected Local Path | File Exists | Same-Name Elsewhere | Likely Matching Project Image | Priority | Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 4 | Gandhi Maidan Patna | `gandhi-maidan-patna` | Patna | `4_e35a3775.jpg` | `static/uploads/places/4_e35a3775.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 7 | Great Buddha Statue, Bodh Gaya | `great-buddha-statue-bodh-gaya` | Gaya | `7_07864df2.jpg` | `static/uploads/places/7_07864df2.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 11 | Vikramshila University Ruins | `vikramshila-university-ruins` | Bhagalpur | `11_1fe6a5df.jpg` | `static/uploads/places/11_1fe6a5df.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 12 | Mandar Hill | `mandar-hill` | Bhagalpur | `12_0bd5f87c.jpg` | `static/uploads/places/12_0bd5f87c.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 14 | Sher Shah Suri Tomb, Sasaram | `sher-shah-suri-tomb-sasaram` | Rohtas | `14_b7d64066.jpg` | `static/uploads/places/14_b7d64066.jpg` | **NO** | **NO** | **NO** | **CRITICAL** | NEEDS VERIFIED EXTERNAL SOURCE |
| 15 | Rohtasgarh Fort | `rohtasgarh-fort` | Rohtas | `15_e4a95edb.jpg` | `static/uploads/places/15_e4a95edb.jpg` | **NO** | **NO** | **NO** | **CRITICAL** | NEEDS VERIFIED EXTERNAL SOURCE |
| 17 | Valmiki National Park | `valmiki-national-park` | West Champaran | `17_b740209f.jpg` | `static/uploads/places/17_b740209f.jpg` | **NO** | **NO** | **NO** | **CRITICAL** | NEEDS VERIFIED EXTERNAL SOURCE |
| 18 | Kesariya Stupa | `kesariya-stupa` | East Champaran | `18_62928207.jpg` | `static/uploads/places/18_62928207.jpg` | **NO** | **NO** | **NO** | **CRITICAL** | NEEDS VERIFIED EXTERNAL SOURCE |
| 19 | Munger Fort | `munger-fort` | Munger | `19_f8e0df37.jpg` | `static/uploads/places/19_f8e0df37.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 23 | Battle of Buxar Memorial | `battle-of-buxar-memorial` | Buxar | `23_648d33c8.jpg` | `static/uploads/places/23_648d33c8.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 24 | Mundeshwari Temple | `mundeshwari-temple` | Kaimur | `24_4ade4525.jpg` | `static/uploads/places/24_4ade4525.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 25 | Janaki Sthan Temple | `janaki-sthan-temple` | Sitamarhi | `25_44f72cfb.jpg` | `static/uploads/places/25_44f72cfb.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 26 | Darbhanga Raj (Laxmi Vilas Palace) | `darbhanga-raj-laxmi-vilas-palace` | Darbhanga | `26_36923c93.jpg` | `static/uploads/places/26_36923c93.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 27 | Litchi Gardens & Jubba Sahni Park | `litchi-gardens-jubba-sahni-park` | Muzaffarpur | `27_ad3dd309.jpg` | `static/uploads/places/27_ad3dd309.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 28 | Veer Kunwar Singh Fort, Jagdishpur | `veer-kunwar-singh-fort-jagdishpur` | Bhojpur | `28_657838b5.jpg` | `static/uploads/places/28_657838b5.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 88 | Bihar Museum | `bihar-museum-patna` | Patna | `88_8d6a2e08.jpg` | `static/uploads/places/88_8d6a2e08.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 89 | Mahavir Mandir, Patna | `mahavir-mandir-patna` | Patna | `89_b37be6d8.jpg` | `static/uploads/places/89_b37be6d8.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 90 | Badi Patan Devi Temple | `badi-patan-devi-temple-patna` | Patna | `90_1a9b8ca2.jpg` | `static/uploads/places/90_1a9b8ca2.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 91 | Kumhrar Archaeological Site | `kumhrar-archaeological-site-patna` | Patna | `91_ef2dc735.jpg` | `static/uploads/places/91_ef2dc735.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 92 | Agam Kuan & Shitala Devi Temple | `agam-kuan-shitala-devi-temple-patna` | Patna | `92_8b31ff60.jpg` | `static/uploads/places/92_8b31ff60.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 93 | Sanjay Gandhi Jaivik Udyan (Patna Zoo) | `sanjay-gandhi-jaivik-udyan-patna-zoo` | Patna | `93_2291d60f.jpg` | `static/uploads/places/93_2291d60f.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 94 | Buddha Smriti Park | `buddha-smriti-park-patna` | Patna | `94_bcaa7b9e.jpg` | `static/uploads/places/94_bcaa7b9e.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 95 | Maner Sharif | `maner-sharif-patna` | Patna | `95_manersharif.jpg` | `static/uploads/places/95_manersharif.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 96 | Patna Planetarium (Indira Gandhi Planetarium) | `patna-planetarium-indira-gandhi-planetarium` | Patna | `96_96121707.jpg` | `static/uploads/places/96_96121707.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 97 | Padri Ki Haveli (St. Mary's Church) | `padri-ki-haveli-patna` | Patna | `97_da1a079e.jpg` | `static/uploads/places/97_da1a079e.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 98 | Sabhyata Dwar (Civilization Gate) | `sabhyata-dwar-patna` | Patna | `98_afa89fe2.png` | `static/uploads/places/98_afa89fe2.png` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 99 | Eco Park (Rajdhani Vatika) | `eco-park-rajdhani-vatika-patna` | Patna | `99_96ef9a4b.jpg` | `static/uploads/places/99_96ef9a4b.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 100 | JP Ganga Path (Patna Marine Drive) | `jp-ganga-path-patna-marine-drive` | Patna | `100_a5bcbd56.jpg` | `static/uploads/places/100_a5bcbd56.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 101 | ISKCON Temple Patna | `iskcon-temple-patna` | Patna | `101_8dca9c86.jpg` | `static/uploads/places/101_8dca9c86.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 102 | Royal Thai Monastery | `royal-thai-monastery-bodh-gaya` | Gaya | `102_1673960f.jpg` | `static/uploads/places/102_1673960f.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 103 | Indosan Nipponji (Japanese Temple) | `indosan-nipponji-japanese-temple-bodh-gaya` | Gaya | `103_3a37da44.jpg` | `static/uploads/places/103_3a37da44.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 104 | Dungeshwari Cave Temples (Mahakala Caves) | `dungeshwari-cave-temples-mahakala-caves-gaya` | Gaya | `104_cc3529be.jpg` | `static/uploads/places/104_cc3529be.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 105 | Pretshila Hill & Ram Kund | `pretshila-hill-ram-kund-gaya` | Gaya | `105_c35f588b.jpg` | `static/uploads/places/105_c35f588b.jpg` | **NO** | **NO** | **NO** | LOW | NEEDS VERIFIED EXTERNAL SOURCE |
| 106 | Mangla Gauri Temple | `mangla-gauri-temple-gaya` | Gaya | `106_d9a1eee8.jpg` | `static/uploads/places/106_d9a1eee8.jpg` | **NO** | **NO** | **NO** | **HIGH** | NEEDS VERIFIED EXTERNAL SOURCE |
| 108 | Devghat & Falgu River Ghats | `devghat-falgu-river-ghats-gaya` | Gaya | `108_25e5da3a.jpg` | `static/uploads/places/108_25e5da3a.jpg` | **NO** | **NO** | **NO** | LOW | NEEDS VERIFIED EXTERNAL SOURCE |
| 109 | Metta Buddharam Temple | `metta-buddharam-temple-bodh-gaya` | Gaya | `109_6a88cd61.jpg` | `static/uploads/places/109_6a88cd61.jpg` | **NO** | **NO** | **NO** | LOW | NEEDS VERIFIED EXTERNAL SOURCE |
| 110 | Bodh Gaya Archaeological Museum | `bodh-gaya-archaeological-museum` | Gaya | `110_1338d68d.jpg` | `static/uploads/places/110_1338d68d.jpg` | **NO** | **NO** | **NO** | MEDIUM | NEEDS VERIFIED EXTERNAL SOURCE |
| 111 | Brahmayoni Hill | `brahmayoni-hill-gaya` | Gaya | `111_3e0a9753.jpg` | `static/uploads/places/111_3e0a9753.jpg` | **NO** | **NO** | **NO** | LOW | NEEDS VERIFIED EXTERNAL SOURCE |
| 112 | Gehlaur Ghati - Dashrath Manjhi Smarak | `gehlaur-ghati-dashrath-manjhi-smarak-gaya` | Gaya | `112_e5f4ebe2.jpg` | `static/uploads/places/112_e5f4ebe2.jpg` | **NO** | **NO** | **NO** | LOW | NEEDS VERIFIED EXTERNAL SOURCE |

---

## 2. Match Against Existing Project Media

Every directory in `D:\HiddenYatra` was traversed to index all 246 image files across the repository:
- `static/` (root icons and SVG category placeholders): 10 files
- `static/hero/`: 30 files
- `static/uploads/districts/`: 37 files (`district_<id>_<hash>.png`)
- `static/uploads/hero/`: 30 files
- `static/uploads/hosts/listings/`: 42 files (`stay_demo_*`, `bodh_gaya_homestay_cover.jpg`, `simultala_stay_cover.jpg`)
- `static/uploads/places/`: 33 files (covering 24 active places)
- `static/uploads/auth/`: 4 files
- `static/uploads/submissions/`: 6 files
- `docs/evidence/` & `uiux_*`: 54 files (audit verification screenshots)

### Matching Results:
1. **Same-Filename Search:** Zero of the 39 referenced filenames exist in any other folder in the repository.
2. **Same Place ID Search:** The 33 images in `static/uploads/places/` belong to place IDs `1, 2, 3, 5, 6, 8, 9, 10, 13, 16, 20, 21, 22, 30, 44, 57, 58, 59, 60, 61, 62, 63, 66, 67, 68, 69`. None of the 39 missing place IDs have alternate image files on disk.
3. **Photos Table Inspection:** MySQL table `photos` contains 14 rows, all corresponding to places with existing photos (Place IDs 16, 20, 22, 57, 58, 59, 60, 61, 62, 63, 66, 67, 68, 69). No supplemental photos exist for the 39 missing places.
4. **Duplicate / Renamed Media:** The existing host listing and district images cannot safely be repurposed for these monument places without causing domain confusion.

---

## 3. Root Cause Forensic Analysis (Why Each Image Is Missing)

Forensic inspection of historical maintenance scripts uncovered the exact script and mechanism responsible for these filenames: [`scripts/maintenance/sync_authentic_wikipedia_photos.py`](file:///d:/HiddenYatra/scripts/maintenance/sync_authentic_wikipedia_photos.py).

### Forensic Evidence:
1. Lines 18-60 of `sync_authentic_wikipedia_photos.py` define a dictionary `WIKI_PAGES` containing precisely the 39 missing place IDs mapped to Wikipedia article titles (e.g., `7: "Great_Buddha_Statue"`, `12: "Mandar_Hill"`, `14: "Tomb_of_Sher_Shah_Suri"`, `88: "Bihar_Museum"`).
2. Line 126 defines the hash generation formula:
   ```python
   out_filename = f"{place_id}_{hashlib.md5(place_name.encode()).hexdigest()[:8]}{ext}"
   ```
   Testing this formula against the place names yielded identical hashes to the database records:
   - `Great Buddha Statue` -> `07864df2` -> `7_07864df2.jpg`
   - `Mandar Hill` -> `0bd5f87c` -> `12_0bd5f87c.jpg`
   - `Munger Fort` -> `f8e0df37` -> `19_f8e0df37.jpg`
   - `Bihar Museum` -> `8d6a2e08` -> `88_8d6a2e08.jpg`
3. Git history reveals that commits `2b2cf9ed` through `b68d415b` on Aug 20, 2026 added 7 batches of place images to `static/uploads/places/` (covering 24 places). However, the downloads for the remaining 39 places were either interrupted, kept in an untracked local developer directory, or omitted when the repository was pushed.
4. The database was subsequently exported/seeded with these 39 filenames in `cover_image`.

### Classification:
- **All 39 Place Images:** **C. STALE DATABASE REFERENCE** / **D. OLD/HISTORICAL REFERENCE** (Generated locally via maintenance script, updated in DB, but files were never committed to the git repository).

---

## 4. Mock Stay Images Investigation

The prompt specifically requested investigation into:
1. `static/images/stays/stay_rajgir.jpg`
2. `static/images/stays/stay_bodhgaya.jpg`
3. `static/images/stays/stay_valmiki.jpg`

### Findings:
1. **Where Referenced:**
   - A full repository scan across all Python files, Jinja templates, JavaScript scripts, CSS stylesheets, GeoJSON layers, and markdown documentation confirmed that **none of these three filenames are referenced in the active application code**.
   - The directory `static/images/stays/` does not exist on disk.
2. **Current Homestay Media Architecture:**
   - In the production codebase, homestays are modeled in MySQL `host_listings` and GIS dataset `static/data/bihar/homestays.geojson`.
   - Homestay photos are stored in `static/uploads/hosts/listings/` (42 valid JPEG files, including `stay_demo_rajgir_cover.jpg`, `stay_demo_gaya_cover.jpg`, etc.).
   - Template `templates/stays/browse.html` (lines 354-358) correctly links to `uploads/hosts/listings/{{ l.cover_image }}`.
3. **Mock / Demo Data Status:**
   - The entire demo stay catalog is mock seed data created for hackathon demonstration purposes (`scripts/seed/seed_homestays.py`).
4. **Fallback Handling:**
   - `templates/stays/browse.html` contains explicit fallback handling:
     ```jinja
     {% if l.cover_image %}
     <img src="{{ url_for('static', filename='uploads/hosts/listings/' + l.cover_image) }}" alt="{{ l.title }}" class="stay-card-img" loading="lazy">
     {% else %}
     <div class="stay-card-placeholder">🏡</div>
     {% endif %}
     ```
   - In GIS map popups (`static/js/map/map-leaflet.js`), `<img ... onerror="this.style.display='none'">` suppresses broken image icons.

---

## 5. Priority Classification

The 39 missing place images are prioritized based on their public page exposure and UX impact:

### A. CRITICAL (4 Places)
*Visible on the homepage hero / featured places section (`is_featured = 1`). Causes immediate visual degradation for first-time visitors.*
1. **ID 14:** Sher Shah Suri Tomb, Sasaram (Rohtas)
2. **ID 15:** Rohtasgarh Fort (Rohtas)
3. **ID 17:** Valmiki National Park (West Champaran)
4. **ID 18:** Kesariya Stupa (East Champaran)

### B. HIGH (16 Places)
*Major flagship heritage landmarks of Bihar prominently featured on top district destination pages (Patna, Gaya, Bhagalpur, Nalanda, Kaimur).*
1. **ID 4:** Gandhi Maidan Patna
2. **ID 7:** Great Buddha Statue, Bodh Gaya
3. **ID 11:** Vikramshila University Ruins
4. **ID 12:** Mandar Hill
5. **ID 19:** Munger Fort
6. **ID 23:** Battle of Buxar Memorial
7. **ID 24:** Mundeshwari Temple
8. **ID 25:** Janaki Sthan Temple
9. **ID 26:** Darbhanga Raj (Laxmi Vilas Palace)
10. **ID 88:** Bihar Museum
11. **ID 89:** Mahavir Mandir, Patna
12. **ID 90:** Badi Patan Devi Temple
13. **ID 91:** Kumhrar Archaeological Site
14. **ID 93:** Sanjay Gandhi Jaivik Udyan (Patna Zoo)
15. **ID 94:** Buddha Smriti Park
16. **ID 106:** Mangla Gauri Temple

### C. MEDIUM (14 Places)
*Secondary regional heritage, cultural, and nature sites appearing in district sub-listings and thematic circuits.*
1. **ID 27:** Litchi Gardens & Jubba Sahni Park (Muzaffarpur)
2. **ID 28:** Veer Kunwar Singh Fort, Jagdishpur (Bhojpur)
3. **ID 92:** Agam Kuan & Shitala Devi Temple (Patna)
4. **ID 95:** Maner Sharif (Patna)
5. **ID 96:** Patna Planetarium (Patna)
6. **ID 97:** Padri Ki Haveli (Patna)
7. **ID 98:** Sabhyata Dwar (Patna)
8. **ID 99:** Eco Park / Rajdhani Vatika (Patna)
9. **ID 100:** JP Ganga Path / Marine Drive (Patna)
10. **ID 101:** ISKCON Temple Patna
11. **ID 102:** Royal Thai Monastery (Gaya)
12. **ID 103:** Indosan Nipponji (Gaya)
13. **ID 104:** Dungeshwari Cave Temples (Gaya)
14. **ID 110:** Bodh Gaya Archaeological Museum

### D. LOW (5 Places + 3 Mock Stays)
*Niche hill viewpoints, local ghats, and demo stay legacy references.*
1. **ID 105:** Pretshila Hill & Ram Kund (Gaya)
2. **ID 108:** Devghat & Falgu River Ghats (Gaya)
3. **ID 109:** Metta Buddharam Temple (Gaya)
4. **ID 111:** Brahmayoni Hill (Gaya)
5. **ID 112:** Gehlaur Ghati - Dashrath Manjhi Path (Gaya)
6. **STAY-MOCK-1:** `static/images/stays/stay_rajgir.jpg`
7. **STAY-MOCK-2:** `static/images/stays/stay_bodhgaya.jpg`
8. **STAY-MOCK-3:** `static/images/stays/stay_valmiki.jpg`

---

## 6. Safe Restoration Plan

### Strict Analysis-Only Boundary:
In accordance with instructions:
- **No images were downloaded or fabricated.**
- **No database records were updated or deleted.**
- **No files were renamed or copied.**

### Restoration Pathway for Future Phase:
1. **Place Images (All 39 Records):**
   - Marked: **`NEEDS VERIFIED EXTERNAL MEDIA SOURCE`**.
   - **Recommended Execution:** A dedicated, supervised restoration script based on `scripts/maintenance/sync_authentic_wikipedia_photos.py` should be run in an approved future phase. This will fetch verified Creative Commons-licensed images from Wikimedia Commons for each monument, verify dimensions using Pillow, write them to `static/uploads/places/<hash_filename>`, and commit them to Git.
2. **Mock Stay Images:**
   - Already superseded in the active application by `static/uploads/hosts/listings/` and protected by UI fallback handlers. If legacy compatibility is desired, symlinking or copying `stay_demo_rajgir_cover.jpg` and `stay_demo_gaya_cover.jpg` into `static/images/stays/` can be scheduled during a future maintenance phase.

---

## 7. Important Data Safety & Invariance Verification

Verification confirmed that zero modifications occurred during this investigation:
- **Active Places:** `148` (`deleted_at IS NULL`)
- **Maximum Place ID:** `198`
- **Districts:** `38`
- **Batch 9 Status:** **NOT INSERTED**
- **Test Suite Status:** 498 passed, 0 failed, 0 errors, 2 skipped

---

## 8. Summary Metric Counts

| Metric | Count |
| :--- | :---: |
| **TOTAL MISSING PLACE IMAGES** | **39** |
| **PROJECT-LOCAL RESTORATION CANDIDATES** | **0** |
| **STALE REFERENCES** | **39** |
| **NEEDS VERIFIED EXTERNAL SOURCE** | **39** |
| **UNKNOWN** | **0** |
| **MOCK STAY ISSUES** | **3** |
| **CRITICAL** | **4** |
| **HIGH** | **16** |
| **MEDIUM** | **14** |
| **LOW** | **8** *(5 places + 3 mock stays)* |

