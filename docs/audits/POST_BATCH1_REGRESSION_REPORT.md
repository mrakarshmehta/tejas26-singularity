# HIDDENYATRA — POST BATCH-1 REGRESSION & LIVE MAP VERIFICATION REPORT

**Verification Date**: September 14, 2026  
**Target Environment**: Local Production-Equivalent (MySQL 8.0 @ Port 3307, Flask App @ Port 5000)  
**Batch Insertion Verified**: Batch 1 (IDs 114 – 124)  
**Status**: **`✅ BATCH 1 LIVE & VERIFIED`**

---

## 1. EXECUTIVE SUMMARY & INVENTORY METRICS

| Metric | Before Batch 1 | After Batch 1 | Delta / Verification | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Total Active Places** | **63** | **74** | **+11 records** (Authoritative DB check) | **PASS** ✅ |
| **Discovery Snapshot (`verified_places`)** | 63 | 74 | Live DB aggregation verified | **PASS** ✅ |
| **Geo-Mapped Places** | 63 | 74 | 100% valid coordinates within Bihar | **PASS** ✅ |
| **Districts Covered with Places** | 20 | 25 | **+5 districts unlocked** (Araria, Arwal, Banka, Gopalganj, Katihar) | **PASS** ✅ |
| **Inserted Primary Keys** | — | `114` to `124` | Contiguous, zero sequence collision | **PASS** ✅ |
| **Unique Name / Slug Collisions** | 0 | 0 | Zero duplicate names or slugs | **PASS** ✅ |
| **Coordinate Duplicate Collisions** | 0 | 0 | Zero coordinate collisions | **PASS** ✅ |

---

## 2. BATCH 1 INSERTED PLACES REGISTER

Every record in Batch 1 has been verified against the live database, routing table, and frontend views:

| ID | Place Name | District | Category | Coordinates | Slug / Route |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **114** | **Raniganj Vriksh Vatika** | Araria (11) | `eco_tourism` | `26.0712, 87.2415` | [`/place/raniganj-vriksh-vatika-araria`](file:///d:/HiddenYatra/place/raniganj-vriksh-vatika-araria) |
| **115** | **Makhdum Shah Baba Dargah** | Arwal (12) | `religious` | `25.2443, 84.6711` | [`/place/makhdum-shah-baba-dargah-arwal`](file:///d:/HiddenYatra/place/makhdum-shah-baba-dargah-arwal) |
| **116** | **Odhni Dam Eco-Tourism Complex** | Banka (14) | `eco_tourism` | `24.8986, 86.9172` | [`/place/odhni-dam-eco-tourism-complex-banka`](file:///d:/HiddenYatra/place/odhni-dam-eco-tourism-complex-banka) |
| **117** | **Sultanganj Ajgaibinath Temple** | Bhagalpur (5) | `religious` | `25.2458, 86.7389` | [`/place/sultanganj-ajgaibinath-temple-bhagalpur`](file:///d:/HiddenYatra/place/sultanganj-ajgaibinath-temple-bhagalpur) |
| **118** | **Vikramshila Gangetic Dolphin Sanctuary** | Bhagalpur (5) | `wildlife` | `25.3117, 87.0211` | [`/place/vikramshila-gangetic-dolphin-sanctuary-bhagalpur`](file:///d:/HiddenYatra/place/vikramshila-gangetic-dolphin-sanctuary-bhagalpur) |
| **119** | **Aranya Devi Temple** | Bhojpur (16) | `religious` | `25.5614, 84.6728` | [`/place/aranya-devi-temple-bhojpur`](file:///d:/HiddenYatra/place/aranya-devi-temple-bhojpur) |
| **120** | **Chausa Battlefield & Monument** | Buxar (17) | `historical` | `25.5186, 83.8967` | [`/place/chausa-battlefield-monument-buxar`](file:///d:/HiddenYatra/place/chausa-battlefield-monument-buxar) |
| **121** | **Thawe Mandir** | Gopalganj (19) | `religious` | `26.4172, 84.4447` | [`/place/thawe-mandir-gopalganj`](file:///d:/HiddenYatra/place/thawe-mandir-gopalganj) |
| **122** | **Karkatgarh Waterfall & Eco Park** | Kaimur (22) | `waterfall` | `25.0456, 83.5861` | [`/place/karkatgarh-waterfall-eco-park-kaimur`](file:///d:/HiddenYatra/place/karkatgarh-waterfall-eco-park-kaimur) |
| **123** | **Telhar Kund Waterfall** | Kaimur (22) | `waterfall` | `24.9758, 83.6042` | [`/place/telhar-kund-waterfall-kaimur`](file:///d:/HiddenYatra/place/telhar-kund-waterfall-kaimur) |
| **124** | **Gogabil Lake Bird Sanctuary** | Katihar (23) | `wildlife` | `25.3667, 87.6833` | [`/place/gogabil-lake-bird-sanctuary-katihar`](file:///d:/HiddenYatra/place/gogabil-lake-bird-sanctuary-katihar) |

---

## 3. DATABASE INTEGRITY VERIFICATION

Automated test script: `scratch/db_regression.py` executed against live MySQL database (`hiddenyatra` @ 3307):

1. **Active Record Count**: Exactly **74** active places (`deleted_at IS NULL`). Assertion PASSED.
2. **Key Check**: IDs 114 to 124 exist, non-null, unbroken sequence. Assertion PASSED.
3. **Foreign Key Integrity (`district_id` & `state_id`)**:
   - ID 114: `district_id=11` (Araria), `state_id=1` (Bihar) — **PASS**
   - ID 115: `district_id=12` (Arwal), `state_id=1` (Bihar) — **PASS**
   - ID 116: `district_id=14` (Banka), `state_id=1` (Bihar) — **PASS**
   - ID 117: `district_id=5` (Bhagalpur), `state_id=1` (Bihar) — **PASS**
   - ID 118: `district_id=5` (Bhagalpur), `state_id=1` (Bihar) — **PASS**
   - ID 119: `district_id=16` (Bhojpur), `state_id=1` (Bihar) — **PASS**
   - ID 120: `district_id=17` (Buxar), `state_id=1` (Bihar) — **PASS**
   - ID 121: `district_id=19` (Gopalganj), `state_id=1` (Bihar) — **PASS**
   - ID 122: `district_id=22` (Kaimur), `state_id=1` (Bihar) — **PASS**
   - ID 123: `district_id=22` (Kaimur), `state_id=1` (Bihar) — **PASS**
   - ID 124: `district_id=23` (Katihar), `state_id=1` (Bihar) — **PASS**
4. **Coordinate Boundary Sanity**:
   - All 11 coordinates strictly within Bihar bounds (`Lat: 24.0 – 27.5 N`, `Lng: 83.0 – 88.5 E`).
   - Zero coordinate duplicates across all 74 places.
5. **Content Completeness**:
   - All 11 records have rich descriptions (`> 150` characters).
   - Valid standard categories: `eco_tourism`, `religious`, `wildlife`, `historical`, `waterfall`.

---

## 4. REST API & ENDPOINT VERIFICATION

All core discovery, search, and geospatial endpoints tested via automated HTTP regression script:

| Endpoint | HTTP Status | Payload Verification | Status |
| :--- | :---: | :--- | :---: |
| `GET /api/discovery-snapshot` | **200 OK** | `verified_places: 74`, `geo_mapped_places: 74`, `districts_covered: 25`, `hidden_gems: 22` | **PASS** ✅ |
| `GET /api/search/filters` | **200 OK** | All 38 districts returned; newly unlocked districts (Araria, Arwal, Banka, Gopalganj, Katihar) verified | **PASS** ✅ |
| `GET /api/search/instant` | **200 OK** | Sub-millisecond response (`~0.2ms`), index rebuilt with 304 entries; 11/11 new places resolved | **PASS** ✅ |
| `GET /api/nearby` | **200 OK** | Haversine query from Bhagalpur (`lat=25.2458, lng=86.7389, r=50km`) returned 6 places | **PASS** ✅ |
| `GET /api/places/nearby-radius` | **200 OK** | 100km radius returned 15 places including new Batch 1 records | **PASS** ✅ |
| `GET /api/culture-map` | **200 OK** | GeoJSON cultural layer features loaded with valid properties | **PASS** ✅ |
| `GET /api/itinerary/search?q=Thawe` | **200 OK** | Returns Thawe Mandir as an itinerary place candidate | **PASS** ✅ |
| `GET /api/smart-nearby` | **200 OK** | Kaimur coordinates (`25.0450, 83.5850`) returns Telhar Kund & Karkatgarh in nearby results | **PASS** ✅ |
| `GET /explore` | **200 OK** | Server-side rendered HTML includes all 11 new places in embedded map payload | **PASS** ✅ |

---

## 5. EXPLORE INTERACTIVE MAP AUDIT

1. **Marker Rendering**:
   - Live Explore page (`http://127.0.0.1:5000/explore`) renders all **74** place markers.
   - Newly inserted Batch 1 places verified on map canvas with appropriate SVG category icons (`waterfall`, `wildlife`, `religious`, `eco_tourism`, `historical`).
2. **Marker Coordinates & Popups**:
   - Verified popup click interaction on newly added markers (e.g. Karkatgarh Waterfall, Thawe Mandir, Gogabil Lake).
   - Popups display verified place thumbnail, title, category pill, district name, and clickable deep-link to place detail page.
3. **Filter Interactivity**:
   - Category filtering (`waterfall`, `wildlife`, `religious`, `eco_tourism`, `historical`) correctly shows/hides markers.
   - District dropdown selection for all 5 newly unlocked districts centers map to district centroid and filters markers to the selected district.
4. **Console & Network Health**:
   - Zero uncaught JavaScript errors in browser DevTools console.
   - Zero 4xx/5xx network request failures.

---

## 6. DISTRICT PAGES VERIFICATION

Tested all 9 host districts via HTTP and browser subagents:

| District Route | HTTP Status | Batch 1 Place Confirmed in Layout | District View Status |
| :--- | :---: | :--- | :---: |
| `/state/bihar/araria` | **200 OK** | **Raniganj Vriksh Vatika** displayed in place grid | **PASS** ✅ |
| `/state/bihar/arwal` | **200 OK** | **Makhdum Shah Baba Dargah** displayed in place grid | **PASS** ✅ |
| `/state/bihar/banka` | **200 OK** | **Odhni Dam Eco-Tourism Complex** displayed in place grid | **PASS** ✅ |
| `/state/bihar/bhagalpur` | **200 OK** | **Sultanganj Ajgaibinath Temple** & **Vikramshila Dolphin Sanctuary** | **PASS** ✅ |
| `/state/bihar/bhojpur` | **200 OK** | **Aranya Devi Temple** displayed in place grid | **PASS** ✅ |
| `/state/bihar/buxar` | **200 OK** | **Chausa Battlefield & Monument** displayed in place grid | **PASS** ✅ |
| `/state/bihar/gopalganj` | **200 OK** | **Thawe Mandir** displayed in place grid | **PASS** ✅ |
| `/state/bihar/kaimur` | **200 OK** | **Karkatgarh Waterfall** & **Telhar Kund Waterfall** | **PASS** ✅ |
| `/state/bihar/katihar` | **200 OK** | **Gogabil Lake Bird Sanctuary** displayed in place grid | **PASS** ✅ |

---

## 7. PLACE DETAIL PAGES VERIFICATION

All 11 place detail routes accessed, parsed, and visually audited:

- **Titles & Slugs**: 100% matched canonical entity titles and slugs.
- **District Breadcrumbs**: Correct hierarchy (`Home > Bihar > [District] > [Place Name]`).
- **Category Badges & Metadata**: Correct tags (`Waterfall`, `Temple / Religious`, `Eco Tourism`, `Wildlife Sanctuary`, `Historical`).
- **Logistics & Practical Info**: Best time to visit, entry fees, nearest railway stations, and bus stands rendered in essential info cards.
- **Images & Fallbacks**: Graceful category-specific SVG placeholder fallback active when custom user uploads are not yet present; zero broken image icons (`img onerror` handlers operational).
- **Navigation & Share**: `Share Place`, `Plan Trip`, `Save / Wishlist`, and `Mark Visited` interactive buttons functioning.

---

## 8. INSTANT SEARCH AUDIT (11/11 RANK #1)

Executed search query test across all 11 new places against live search engine (`models/search_engine.py`):

| Query Term | Target Place | Live Search Rank | Match Score & Type | Result |
| :--- | :--- | :---: | :---: | :---: |
| `Raniganj` | Raniganj Vriksh Vatika | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Makhdum` | Makhdum Shah Baba Dargah | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Odhni` | Odhni Dam Eco-Tourism Complex | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Ajgaibinath` | Sultanganj Ajgaibinath Temple | **#1** | 78 (Word Start) | **PASS** ✅ |
| `Dolphin` | Vikramshila Gangetic Dolphin Sanctuary | **#1** | 78 (Word Start) | **PASS** ✅ |
| `Aranya` | Aranya Devi Temple | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Chausa` | Chausa Battlefield & Monument | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Thawe` | Thawe Mandir | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Karkatgarh` | Karkatgarh Waterfall & Eco Park | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Telhar` | Telhar Kund Waterfall | **#1** | 93 (Prefix) | **PASS** ✅ |
| `Gogabil` | Gogabil Lake Bird Sanctuary | **#1** | 93 (Prefix) | **PASS** ✅ |

---

## 9. ITINERARY & NEARBY ENGINE INTEGRATION

1. **Nearby Discovery Participation**:
   - Tested `/api/smart-nearby?lat=25.0450&lng=83.5850&category=nature`: returns Karkatgarh and Telhar Kund as nearby destinations with calculated distances and travel metrics.
2. **Itinerary Candidate Selection**:
   - Tested `/api/itinerary/search?q=[name]`: all 11 destinations are returned in itinerary candidate auto-suggest lists, allowing users to add them to custom itineraries.
3. **Route Mapping**:
   - New destination coordinates participate in waypoint calculation without geodesic distortions.

---

## 10. MOBILE VIEWPORT VERIFICATION (390 × 844)

Conducted browser inspection on mobile viewport (iPhone 12/13/14 format):

1. **Karkatgarh Waterfall & Eco Park (`/place/karkatgarh-waterfall-eco-park-kaimur`)**:
   - Verified responsive header, sticky action pills, breadcrumb truncation, and hero image contrast.
   - Essential info 2-column mobile grid renders cleanly without horizontal scroll overflow.
   - Accordion FAQs and nearby essentials cards stack properly.
2. **Thawe Mandir (`/place/thawe-mandir-gopalganj`)**:
   - Religious place badges, Navratri festival tags, and transport direction links format properly on small screens.
3. **Artifact Recordings & Screenshots**:
   - Mobile verification recording: `batch1_mobile_verify_1789396681519.webp`
   - Screenshots captured: `karkatgarh_hero_mobile_*.png`, `karkatgarh_essential_info_mobile_*.png`, `thawe_mandir_mobile_*.png`.

---

## 11. AUTOMATED TEST SUITE EXECUTION

Executed automated map fix test suite (`tests/test_map_fixes.py`):

```bash
$ python -m unittest tests/test_map_fixes.py
2026-09-14 20:06:35,144 [INFO] models.connection: MySQL connection pool created (size=5, max=20)
2026-09-14 20:06:35,154 [INFO] models.search_engine: Building search index...
2026-09-14 20:06:35,191 [INFO] models.search_engine: Search index built: 304 entries (25 categories, 38 districts)
..............
----------------------------------------------------------------------
Ran 14 tests in 0.936s

OK
```

- **Map Fix Suite (`tests/test_map_fixes.py`)**: **14 / 14 PASSED (100%)**
- **Wider Regression (`pytest`)**: **90 PASSED**

---

## 12. OPERATIONAL NOTES & RECTIFICATIONS PERFORMED

During post-insertion validation:
1. **Search Index Rebuild**:
   - As designed in `models/search_engine.py`, the in-memory singleton `SearchIndex` was built at Flask startup.
   - After Batch 1 MySQL records were inserted, the Flask server process was restarted cleanly. The index rebuilt with **304 entries** (including all 74 places, 38 districts, and cross-domain entities).
   - Stale background worker processes were terminated to guarantee that all HTTP traffic on port 5000 routes exclusively through the fresh server process.
2. **Database Protection**:
   - Zero schema changes were made.
   - Zero unrelated records were modified.
   - No places beyond IDs 114–124 were added.

---

## 13. FINAL VERDICT & NEXT STEPS

```
================================================================================
                    FINAL REGRESSION AUDIT VERDICT:
                    ✅ BATCH 1 LIVE & VERIFIED
================================================================================
```

- **Current Active Inventory**: **74 Verified Destinations** across **25 Districts** of Bihar.
- **Batch 1 Status**: Live, indexed, geolocated, and verified across desktop and mobile.
- **Batch 2 Status**: **HELD ON FREEZE**. Awaiting explicit human approval before any further preparation or insertion.
