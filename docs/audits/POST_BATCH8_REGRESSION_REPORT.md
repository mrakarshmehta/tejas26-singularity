# HiddenYatra — Post-Batch 8 Regression & Live Verification Report

**Execution Timestamp:** 2026-09-15 13:18:45 IST  
**Environment:** Windows / Python 3.13 / MySQL 8.0 (Pool: 5–20 connections) / Flask 3.0.0  
**Phase:** Batch 8 Atomic Insertion & Comprehensive Regression Verification  

---

## 1. Final Status

# ✅ BATCH 8 LIVE & VERIFIED

All 10 approved Batch 8 destination candidates have been atomically committed to the live database in a single transaction (`autocommit = False`). All 10 district mappings were verified against the live `districts` table prior to execution. Zero regressions occurred across the active platform, search engine, itinerary generation, APIs, and automated test suites.

---

## 2. Before / After Inventory Baseline

| Metric | Pre-Batch 8 Baseline | Post-Batch 8 Baseline | Delta | Verification Status |
| :--- | :---: | :---: | :---: | :---: |
| **Total Active Places (`deleted_at IS NULL`)** | **138** | **148** | **+10** | **VERIFIED** |
| **Districts Covered** | **38 / 38** | **38 / 38** | **0** | **VERIFIED (100%)** |
| **Maximum Place ID (`MAX(id)`)** | **188** | **198** | **+10** | **VERIFIED** |
| **Total Places in Table (incl. historical test/soft-deleted)** | 139 | 149 | +10 | VERIFIED |
| **Database Mutations on Pre-existing Places** | 0 | 0 | 0 | **100% INVARIANT** |

---

## 3. Actual Inserted Batch 8 IDs

The 10 records were inserted atomically in ascending sequence:
```
Inserted IDs: [189, 190, 191, 192, 193, 194, 195, 196, 197, 198]
```

---

## 4. Exact Inserted Records (10 / 10)

| ID | Name | District | DB Dist ID | Category | Latitude | Longitude | Canonical Slug |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **189** | Ara House | Bhojpur | **16** | `historical` | 25.5539 | 84.6680 | `ara-house-bhojpur` |
| **190** | Ahilya Sthan, Ahiyari | Darbhanga | **18** | `cultural` | 26.2917 | 85.8015 | `ahilya-sthan-ahiyari-darbhanga` |
| **191** | Baba Garibnath Temple | Muzaffarpur | **7** | `temple` | 26.1205 | 85.3912 | `baba-garibnath-temple-muzaffarpur` |
| **192** | Surya Mandir, Kandaha | Saharsa | **29** | `historical` | 25.8820 | 86.4670 | `surya-mandir-kandaha-saharsa` |
| **193** | Mata Puran Devi Temple | Purnia | **28** | `cultural` | 25.7725 | 87.4580 | `mata-puran-devi-temple-purnia` |
| **194** | Baba Brahmeshwar Nath Temple, Brahmpur | Buxar | **17** | `temple` | 25.5992 | 84.2882 | `baba-brahmeshwar-nath-temple-brahmpur-buxar` |
| **195** | Gunawa Ji (Jain Tirth) | Nawada | **38** | `cultural` | 24.8944 | 85.5312 | `gunawa-ji-jain-tirth-nawada` |
| **196** | Ambika Sthan, Aami | Saran | **31** | `cultural` | 25.6881 | 85.0062 | `ambika-sthan-aami-saran` |
| **197** | Lakri Dargah | Gopalganj | **19** | `cultural` | 26.3150 | 84.4720 | `lakri-dargah-gopalganj` |
| **198** | Baba Tileshwar Nath Mandir, Sukhpur | Supaul | **36** | `temple` | 26.0620 | 86.6080 | `baba-tileshwar-nath-mandir-sukhpur-supaul` |

---

## 5. District Depth Impact

All 10 candidates provided essential depth expansion to underrepresented districts, doubling Supaul's inventory and bringing 7 other districts from 2 to 3 destinations:

| District Name | District DB ID | Pre-Batch 8 Count | Post-Batch 8 Count | Delta | Newly Inserted Destination |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Supaul** | 36 | 1 | **2** | +1 | Baba Tileshwar Nath Mandir, Sukhpur |
| **Bhojpur** | 16 | 2 | **3** | +1 | Ara House |
| **Darbhanga** | 18 | 2 | **3** | +1 | Ahilya Sthan, Ahiyari |
| **Muzaffarpur** | 7 | 2 | **3** | +1 | Baba Garibnath Temple |
| **Saharsa** | 29 | 2 | **3** | +1 | Surya Mandir, Kandaha |
| **Purnia** | 28 | 2 | **3** | +1 | Mata Puran Devi Temple |
| **Nawada** | 38 | 2 | **3** | +1 | Gunawa Ji (Jain Tirth) |
| **Gopalganj** | 19 | 2 | **3** | +1 | Lakri Dargah |
| **Buxar** | 17 | 3 | **4** | +1 | Baba Brahmeshwar Nath Temple, Brahmpur |
| **Saran** | 31 | 3 | **4** | +1 | Ambika Sthan, Aami |

---

## 6. Category Diversity Distribution

The Batch 8 insertion expands thematic diversity across the catalog:

| Category | Count Added | Share | Inserted Destinations |
| :--- | :---: | :---: | :--- |
| **cultural** | 5 | 50.0% | Ahilya Sthan, Mata Puran Devi, Gunawa Ji (Jain Tirth), Ambika Sthan, Lakri Dargah |
| **temple** | 3 | 30.0% | Baba Garibnath Temple, Baba Brahmeshwar Nath Temple, Baba Tileshwar Nath Mandir |
| **historical** | 2 | 20.0% | Ara House (1857 Uprising), Surya Mandir Kandaha (14th C. Inscribed Sun Temple) |
| **Total** | **10** | **100.0%** | **10 separate districts** |

---

## 7. Duplicate, Alias & Integrity Checks

Post-insert database integrity assertions executed:
- **Duplicate Names:** **0** (`SELECT name, COUNT(*) FROM places WHERE deleted_at IS NULL GROUP BY name HAVING count > 1` $\rightarrow$ 0 rows)
- **Duplicate Slugs:** **0** (`SELECT slug, COUNT(*) FROM places WHERE deleted_at IS NULL GROUP BY slug HAVING count > 1` $\rightarrow$ 0 rows)
- **Duplicate Coordinates:** **0** (`SELECT latitude, longitude, COUNT(*) FROM places WHERE deleted_at IS NULL GROUP BY latitude, longitude HAVING count > 1` $\rightarrow$ 0 rows)
- **Foreign Key Integrity:** **0 orphans** (`SELECT p.id FROM places p LEFT JOIN districts d ON p.district_id = d.id WHERE d.id IS NULL AND p.deleted_at IS NULL` $\rightarrow$ 0 rows)
- **Category Validity:** All 3 categories (`historical`, `cultural`, `temple`) exist in the validated platform category enum.

---

## 8. Haversine Overlap Audit Against Prior 138 Active Places

Every Batch 8 place was audited against all 138 existing active places:

| ID | Candidate Name | District | Nearest Existing Active Place | Distance | Overlap Status |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **189** | Ara House | Bhojpur | ID 119 Aranya Devi Temple (Bhojpur) | **0.88 km** | SAME SITE / SEVERE OVERLAP (*Special Scrutiny Approved*) |
| **190** | Ahilya Sthan, Ahiyari | Darbhanga | ID 26 Darbhanga Raj Palace (Darbhanga) | **18.21 km** | DISTINCT DESTINATION |
| **191** | Baba Garibnath Temple | Muzaffarpur | ID 27 Litchi Gardens / Jubba Sahni Park (Muzaffarpur) | **2.65 km** | NEARBY BUT DISTINCT (*Special Scrutiny Approved*) |
| **192** | Surya Mandir, Kandaha | Saharsa | ID 130 Shri Ugratara Sthan, Mahishi (Saharsa) | **2.58 km** | NEARBY BUT DISTINCT (*Special Scrutiny Approved*) |
| **193** | Mata Puran Devi Temple | Purnia | ID 174 Kajha Kothi Eco Park (Purnia) | **12.27 km** | DISTINCT DESTINATION |
| **194** | Baba Brahmeshwar Nath | Buxar | ID 28 Veer Kunwar Singh Fort, Jagdishpur (Bhojpur) | **19.58 km** | DISTINCT DESTINATION |
| **195** | Gunawa Ji (Jain Tirth) | Nawada | ID 145 Ghora Katora Lake Eco-Reserve (Nalanda) | **11.98 km** | DISTINCT DESTINATION |
| **196** | Ambika Sthan, Aami | Saran | ID 95 Maner Sharif (Patna) | **12.94 km** | DISTINCT DESTINATION |
| **197** | Lakri Dargah | Gopalganj | ID 121 Thawe Mandir (Gopalganj) | **15.92 km** | DISTINCT DESTINATION |
| **198** | Baba Tileshwar Nath | Supaul | ID 173 Matsyagandha Lake & Raktakali (Saharsa) | **19.98 km** | DISTINCT DESTINATION |

### Special Scrutiny Audit Summary (< 5 km candidates):
1. **Ara House (0.88 km from Aranya Devi Temple):**
   - *Physical Parcel:* Independent secular fortified bungalow structure inside Maharaja College campus, separated from the ancient market temple by the railway and central urban thoroughfare.
   - *Typology & Mission:* Secular 1857 Indian Mutiny military siege fortress (site of the international Siege of Arrah by Babu Veer Kunwar Singh) vs. ancient riverbank Hindu temple.
2. **Baba Garibnath Temple (2.65 km from Jubba Sahni Park):**
   - *Physical Parcel:* Located in the heart of old Muzaffarpur, 2.65 km away from Club Road municipal park.
   - *Typology & Mission:* Major 300-year-old pilgrimage shrine ("Deoghar of North Bihar") with dedicated BSTDC corridor project vs. municipal children's eco-garden.
3. **Surya Mandir, Kandaha (2.58 km from Shri Ugratara Sthan):**
   - *Physical Parcel:* Distinct village and panchayat (Pastwar Panchayat, Kandaha village) across rural agrarian fields from Mahishi village.
   - *Typology & Mission:* ASI-recognized archaeological monument featuring an authentic 14th-century Oinwar Sanskrit inscription and black granite Surya idol on 7-horse chariot vs. active Tantric Shaktipeeth temple trust.

---

## 9. Previous Record Invariance Audit

Comparison executed between pre-insert snapshot and post-insert state for IDs 1–188:
- **Active places with ID $\le$ 188:** Exactly **138 / 138** (0 deleted, 0 soft-deleted)
- **Names, descriptions, categories, coordinates, and district IDs:** **0 altered**
- **District assignments:** **0 reassigned**

---

## 10. Live API Regression Verification

All live API endpoints tested against the active local server (`http://127.0.0.1:5000`):

| Endpoint | HTTP Status | Response Contract Verification | Result |
| :--- | :---: | :--- | :---: |
| `GET /api/discovery-snapshot` | **200 OK** | `verified_places: 148`, `geo_mapped_places: 148`, `districts_covered: 38` | **PASS** ✅ |
| `GET /api/search/filters` | **200 OK** | `districts: 38`, 9 categories | **PASS** ✅ |
| `GET /api/places/map` | **200 OK** | Total places: 148; all Batch 8 IDs (189–198) present with valid coordinates | **PASS** ✅ |
| `GET /api/culture-map` | **200 OK** | `status: success`, cultural pins rendered | **PASS** ✅ |
| `GET /api/smart-nearby` | **200 OK** | Proximity search (lat: 25.5539, lng: 84.6680, radius: 25km) returned valid nearby places | **PASS** ✅ |
| `GET /api/itinerary/search` | **200 OK** | Deterministic itinerary query for Bhojpur returned 30 multi-stop day plans | **PASS** ✅ |

---

## 11. Search Regression Verification

All 16 mandated instant search queries were verified via `GET /api/search/instant?q=<query>`:

| Query String | Expected Destination | Top Matched Destination Name | Match Found | Result |
| :--- | :--- | :--- | :---: | :---: |
| `Ara House` | Ara House | **Ara House** | **True** | **PASS** ✅ |
| `Ahilya Sthan` | Ahilya Sthan, Ahiyari | **Ahilya Sthan, Ahiyari** | **True** | **PASS** ✅ |
| `Ahiyari` | Ahilya Sthan, Ahiyari | **Ahilya Sthan, Ahiyari** | **True** | **PASS** ✅ |
| `Baba Garibnath` | Baba Garibnath Temple | **Baba Garibnath Temple** | **True** | **PASS** ✅ |
| `Surya Mandir` | Surya Mandir, Kandaha | **Surya Mandir, Kandaha** | **True** | **PASS** ✅ |
| `Kandaha` | Surya Mandir, Kandaha | **Surya Mandir, Kandaha** | **True** | **PASS** ✅ |
| `Puran Devi` | Mata Puran Devi Temple | **Mata Puran Devi Temple** | **True** | **PASS** ✅ |
| `Brahmeshwar Nath` | Baba Brahmeshwar Nath Temple, Brahmpur | **Baba Brahmeshwar Nath Temple, Brahmpur** | **True** | **PASS** ✅ |
| `Brahmpur` | Baba Brahmeshwar Nath Temple, Brahmpur | **Baba Brahmeshwar Nath Temple, Brahmpur** | **True** | **PASS** ✅ |
| `Gunawa Ji` | Gunawa Ji (Jain Tirth) | **Gunawa Ji (Jain Tirth)** | **True** | **PASS** ✅ |
| `Jain Tirth` | Gunawa Ji (Jain Tirth) | Champanagar Ancient Capital & Jain Tirth / Gunawa Ji | **True** | **PASS** ✅ |
| `Ambika Sthan` | Ambika Sthan, Aami | **Ambika Sthan, Aami** | **True** | **PASS** ✅ |
| `Aami` | Ambika Sthan, Aami | **Ambika Sthan, Aami** | **True** | **PASS** ✅ |
| `Lakri Dargah` | Lakri Dargah | **Lakri Dargah** | **True** | **PASS** ✅ |
| `Tileshwar Nath` | Baba Tileshwar Nath Mandir, Sukhpur | **Baba Tileshwar Nath Mandir, Sukhpur** | **True** | **PASS** ✅ |
| `Sukhpur` | Baba Tileshwar Nath Mandir, Sukhpur | **Baba Tileshwar Nath Mandir, Sukhpur** | **True** | **PASS** ✅ |

---

## 12. Map Verification

- **Endpoint:** `GET /explore`
- **Total Mapped Markers:** **148**
- **Batch 8 Pin Placement:** Verified on map at precise coordinates (e.g., Ara House at 25.5539, 84.6680; Baba Tileshwar Nath at 26.0620, 86.6080).
- **Interactions:** Popups display title, district, category badge, and detail link. Zero Leaflet or browser console errors.
- *Notice:* All geographic distances rely strictly on deterministic spherical Haversine calculations without claiming live road routing or real-time traffic.

---

## 13. Detail Pages Verification

All 10 canonical destination routes were fetched and verified:

| Canonical Slug | HTTP Status | Response Size | DOM & Content Checks |
| :--- | :---: | :---: | :--- |
| `/place/ara-house-bhojpur` | **200 OK** | 95,267 B | Verified title, description, 1857 Uprising history, maps link |
| `/place/ahilya-sthan-ahiyari-darbhanga` | **200 OK** | 95,639 B | Verified title, Ramayana Circuit context, Kamtaul connectivity |
| `/place/baba-garibnath-temple-muzaffarpur` | **200 OK** | 95,645 B | Verified title, Deoghar of North Bihar, Shravani Mela context |
| `/place/surya-mandir-kandaha-saharsa` | **200 OK** | 95,427 B | Verified title, 14th C. Oinwar epigraph, ASI protected status |
| `/place/mata-puran-devi-temple-purnia` | **200 OK** | 95,163 B | Verified title, district eponym origin, Navratri rituals |
| `/place/baba-brahmeshwar-nath-temple-brahmpur-buxar` | **200 OK** | 95,664 B | Verified title, Mini Kashi lore, Brahmpur cattle fair |
| `/place/gunawa-ji-jain-tirth-nawada` | **200 OK** | 95,439 B | Verified title, Gautama Swami Kevala Jnana, Jal Mandir |
| `/place/ambika-sthan-aami-saran` | **200 OK** | 95,380 B | Verified title, Daksha Yajna Shaktipeeth, Ganga cliff mound |
| `/place/lakri-dargah-gopalganj` | **200 OK** | 95,357 B | Verified title, Shah Arzan tomb, Aurangzeb royal endowment |
| `/place/baba-tileshwar-nath-mandir-sukhpur-supaul` | **200 OK** | 95,605 B | Verified title, Swayambhu Shivalinga, Sukhpur Kosi basin |

---

## 14. District Pages Verification

All 10 affected district portal pages were tested and confirmed:

| District Slug | HTTP Status | Response Size | Destination Count & Card Verification |
| :--- | :---: | :---: | :--- |
| `/state/bihar/bhojpur` | **200 OK** | 54,101 B | 3 places rendered (incl. Ara House) |
| `/state/bihar/darbhanga` | **200 OK** | 55,917 B | 3 places rendered (incl. Ahilya Sthan) |
| `/state/bihar/muzaffarpur` | **200 OK** | 57,022 B | 3 places rendered (incl. Baba Garibnath Temple) |
| `/state/bihar/saharsa` | **200 OK** | 55,067 B | 3 places rendered (incl. Surya Mandir Kandaha) |
| `/state/bihar/purnia` | **200 OK** | 54,800 B | 3 places rendered (incl. Mata Puran Devi Temple) |
| `/state/bihar/buxar` | **200 OK** | 59,272 B | 4 places rendered (incl. Baba Brahmeshwar Nath) |
| `/state/bihar/nawada` | **200 OK** | 54,377 B | 3 places rendered (incl. Gunawa Ji Jain Tirth) |
| `/state/bihar/saran` | **200 OK** | 59,608 B | 4 places rendered (incl. Ambika Sthan, Aami) |
| `/state/bihar/gopalganj` | **200 OK** | 55,195 B | 3 places rendered (incl. Lakri Dargah) |
| `/state/bihar/supaul` | **200 OK** | 50,239 B | **2 places rendered** (Kosi Barrage + Baba Tileshwar Nath) |

---

## 15. Smart Nearby & Itinerary Engine Verification

- **Smart Nearby (`GET /api/smart-nearby`):**
  - Confirmed discoverable using deterministic Haversine distance.
  - Proximity clustering correctly groups Batch 8 destinations with neighboring regional clusters (e.g., Ara House with Aranya Devi and Jagdishpur Fort; Baba Brahmeshwar Nath with Buxar and Ara).
- **Deterministic Itinerary Search (`GET /api/itinerary/search`):**
  - All 10 places participate in deterministic nearest-neighbor trip sequencing.
  - No changes made to itinerary generation rules (strict hop limits, daily time budgets, and backtracking reduction preserved).

---

## 16. Automated Test Suite Results

The comprehensive test suite was executed in full:

| Test Suite File | Tests Run | Result | Execution Notes |
| :--- | :---: | :---: | :--- |
| `tests/test_map_fixes.py` | 14 | **PASS** | Map fix contracts and coordinate integrity verified |
| `tests/test_discovery_contract.py` | 4 | **PASS** | Platform snapshot counts (148 places, 38 districts) validated |
| `tests/test_search_engine.py` | 65 | **PASS** | Search algorithms, typo tolerance, synonyms, and performance validated |
| `tests/test_smart_nearby.py` | 12 | **PASS** | Smart nearby discovery verified |
| `tests/test_routes.py` | 48 | **PASS** | Flask blueprints and HTTP route handling verified |
| `tests/test_database.py` & `tests/test_itinerary.py` | 35 | **PASS** (2 skipped) | Database queries, constraints, and itinerary generation verified |
| `tests/test_browser_api.py` | 18 | **PASS** | Search API latency and stress tests verified (185 QPS) |
| **Full Suite (`python -m unittest discover tests/`)** | **496** | **PASS** (2 skipped) | **494 passed, 0 failures, 0 errors, 2 skipped** (22.29s) |

---

## 17. Visual & Mobile Evidence Artifacts

Visual evidence captured via automated headless browser sessions:

### 1. Explore Map — Bhojpur Filter (Batch 8 Marker)
![Explore Map Bhojpur Filter](file:///C:/Users/AKARSH%20RAJ/.gemini/antigravity-ide/brain/135efbcd-8f42-408e-abf7-f6b2a19445bb/batch8_explore_bhojpur_filter.png)

### 2. Desktop Detail Page — Ara House (Bhojpur)
![Ara House Desktop Detail](file:///C:/Users/AKARSH%20RAJ/.gemini/antigravity-ide/brain/135efbcd-8f42-408e-abf7-f6b2a19445bb/batch8_ara_house_detail_desktop.png)

### 3. Desktop District Portal Page — Bhojpur
![Bhojpur District Page](file:///C:/Users/AKARSH%20RAJ/.gemini/antigravity-ide/brain/135efbcd-8f42-408e-abf7-f6b2a19445bb/batch8_district_bhojpur_desktop.png)

### 4. Desktop District Portal Page — Supaul (Inventory Doubled)
![Supaul District Page](file:///C:/Users/AKARSH%20RAJ/.gemini/antigravity-ide/brain/135efbcd-8f42-408e-abf7-f6b2a19445bb/batch8_district_supaul_desktop.png)

### 5. Mobile Detail Page — Baba Garibnath Temple (Muzaffarpur)
![Baba Garibnath Temple Mobile](file:///C:/Users/AKARSH%20RAJ/.gemini/antigravity-ide/brain/135efbcd-8f42-408e-abf7-f6b2a19445bb/batch8_mobile_garibnath.png)

### 6. Mobile Detail Page — Surya Mandir, Kandaha (Saharsa)
![Surya Mandir Kandaha Mobile](file:///C:/Users/AKARSH%20RAJ/.gemini/antigravity-ide/brain/135efbcd-8f42-408e-abf7-f6b2a19445bb/batch8_mobile_kandaha.png)

---

## 18. Warnings, Issues & Observations

- **Zero Regression Violations:** No foreign key violations, orphan records, duplicate slugs, or broken pages were detected.
- **Strict Stop Condition:** Batch 8 is complete. Database is invariant with 148 active destinations across all 38 districts.
