# HiddenYatra — Map/GIS Fix Changelog

This document tracks all code and database modifications made during the P0/P1 GIS Fix Phase.

---

## Safety & Checkpoint Baseline
- **Git Checkpoint Tag:** `checkpoint-pre-map-fixes`
- **Baseline Date:** 2026-09-13
- **Development Server:** Running on `http://127.0.0.1:5000`
- **Database Backup Table:** `_backup_places_pre_map_fix` created containing original unmodified place records prior to any coordinate or duplicate alterations.

---

## 1. P0-4 & P0-5: Geographic Coordinate Correction & Barabar Duplicate Canonicalization

### Issue
- **Barabar Caves ID 5**: Coordinates were pointing to incorrect location (24.6961 N, 84.9911 E) in Bodh Gaya instead of Makhdumpur/Belaganj (25.0061 N, 85.0621 E). Duplicate record ID 107 existed with overlapping content (`barabar-caves-siddheshwar-nath-gaya`).
- **Rohtasgarh Fort ID 15**: Coordinates were shifted north by ~21 km (24.8167 N, 83.8333 E) instead of actual fort plateau (24.6300 N, 83.8900 E).
- **Golghar ID 1**: Coordinates had minor latitude offset (25.6200 N, 85.1448 E) instead of center of Golghar roundabout (25.6120 N, 85.1448 E).

### Files Changed
- `routes/places.py`: Added HTTP 301 permanent redirect handling for duplicate slug `barabar-caves-siddheshwar-nath-gaya` -> `/place/barabar-caves-gaya`.

### Database Rows Changed
Table: `places`

1. **Place ID 5 (Barabar Caves)**:
   - **Old values**:
     - `latitude`: `24.69610000`
     - `longitude`: `84.99110000`
     - `block_id`: `NULL`
     - `name`: `'Barabar Caves'`
     - `is_hidden_gem`: `0`
   - **New values**:
     - `latitude`: `25.00610000`
     - `longitude`: `85.06210000`
     - `block_id`: `17` (Belaganj)
     - `name`: `'Barabar Caves & Siddheshwar Nath'`
     - `is_hidden_gem`: `1`
     - Enriched description, parking tips, and accessibility info merged from ID 107.
   - **Reason**: Correct coordinate location, consolidate metadata, maintain single canonical destination without broken foreign keys.

2. **Place ID 107 (Duplicate Barabar Caves entry)**:
   - **Old values**: `deleted_at`: `NULL`
   - **New values**: `deleted_at`: `2026-09-13 22:58:20` (Soft-deleted)
   - **Reason**: Avoid duplicate map pins; legacy URLs 301-redirect to canonical ID 5 slug.

3. **Place ID 15 (Rohtasgarh Fort)**:
   - **Old values**: `latitude`: `24.81670000`, `longitude`: `83.83330000`
   - **New values**: `latitude`: `24.63000000`, `longitude`: `83.89000000`
   - **Reason**: Fix 21 km geographic positioning error to place fort correctly on Rohtas plateau.

4. **Place ID 1 (Golghar Patna)**:
   - **Old values**: `latitude`: `25.62000000`, `longitude`: `85.14480000`
   - **New values**: `latitude`: `25.61200000`, `longitude`: `85.14480000`
   - **Reason**: Fix ~890 m latitude offset to center directly over Golghar monument.

### Tests Performed
- Executed `tests/test_map_fixes.py` (`test_fixed_coordinates_integrity`, `test_barabar_canonicalization_and_redirect`).
- Verified HTTP 301 redirection from `/place/barabar-caves-siddheshwar-nath-gaya` to `/place/barabar-caves-gaya`.
- Visual browser verification confirmed place page renders with exact coordinates.

---

## 2. P0-1, P0-2 & P1-1: Leaflet Asset Loading Architecture

### Issue
- `app.py` set `skip_base_leaflet = True` globally when `MAP_ENGINE = 'google'`.
- `base.html` omitted Leaflet CSS and JS, causing `L is undefined` on district and itinerary detail pages.

### Files Changed
- `app.py`: Changed global `skip_base_leaflet` in template context processor from `(config.MAP_ENGINE == 'google')` to `False` (allowing page-level opt-in or context override).
- `templates/base.html`: Updated conditional asset inclusion logic to `{% if not skip_base_leaflet or needs_leaflet %}` for both Leaflet CSS and JS.
- `templates/district.html`: Added `{% set needs_leaflet = true %}` at top of template.
- `templates/itinerary_detail.html`: Added `{% set needs_leaflet = true %}` at top of template.

### Database Rows Changed
- Populated `saved_itineraries` row ID 1 with sample Bihar route coordinates (Patna -> Nalanda -> Rajgir) for functional itinerary map testing.

### Reason
- Keep Google Maps as primary engine on `/explore` without loading redundant Leaflet scripts, while cleanly providing Leaflet to pages requiring Leaflet maps.

### Tests Performed
- Automated test `test_district_map_leaflet_assets` verified `/state/bihar/patna` loads `leaflet.css`, `leaflet.js`, and `#district-map`.
- Automated test `test_itinerary_map_leaflet_assets` verified `/itinerary/1` loads Leaflet assets and renders `#itinerary-map`.
- Automated test `test_explore_google_omits_leaflet` verified `/explore` omits Leaflet JS when in Google Maps mode.
- Browser test captured screenshots of rendered interactive Leaflet maps on `/state/bihar/patna` and `/itinerary/1`.

---

## 3. P0-3: Google Maps Culture Map Layer Ingestion

### Issue
- `/api/culture-map` returned JSON `{ status: "success", items: [...] }` while Google Maps `map.data.addGeoJson()` required a GeoJSON `FeatureCollection`.

### Files Changed
- `static/js/map/map-google-layers.js`:
  - Added `_normalizeToGeoJson(data)` adapter method converting `{ items: [...] }` or `{ results: [...] }` into standard GeoJSON `FeatureCollection` with `Point` geometry.
  - Implemented `_applyLayerStyle()` to support `google.maps.SymbolPath.CIRCLE` for Point layers using layer-specific colors.
  - Added `_buildCulturePopup(props)` to render rich metadata popups (name, icon, category, district, description, link) on click.
- `static/js/map/map-google.js`:
  - Updated `addPointMarkerLayer()` to support `{ items: [...] }` and `{ results: [...] }` data formats.
  - Added `restaurants` to point layer handling.

### Reason
- Retain existing stable backend API response format while ensuring seamless frontend ingestion across both Google Maps and Leaflet engines.

### Tests Performed
- Automated tests `test_culture_api_endpoint`, `test_culture_normalization_geojson_adapter`, and `test_culture_categories_coverage`.
- Browser subagent toggled Culture & Heritage layer on `/explore`, confirming markers render on Google Maps canvas.

---

## 4. P0-6: Discovery Snapshot Authoritative Live Data

### Issue
- Discovery Snapshot modal in `/explore` showed stale, hardcoded district numbers (Nalanda = 10, Rohtas = 7, West Champaran = 5), omitting top districts (Patna = 18, Gaya = 13, Jamui = 11).

### Files Changed
- `routes/api.py`: Updated `api_discovery_snapshot()` endpoint to execute live SQL aggregation:
  `SELECT d.name, COUNT(p.id) as place_count FROM districts d JOIN places p ON p.district_id = d.id WHERE p.deleted_at IS NULL GROUP BY d.id, d.name ORDER BY place_count DESC LIMIT 8`.
- `templates/explore_map.html`: Updated `renderSnapshotModal()` JavaScript function to dynamically construct the top districts table from `data.top_districts` array rather than static HTML strings.

### Reason
- Data integrity; ensure platform statistics always match authoritative database records.

### Tests Performed
- Automated test `test_discovery_snapshot_live_district_counts`.
- Browser test opened Snapshot modal on `/explore`; screenshot confirmed Patna: 18, Gaya: 13, Jamui: 11, Nalanda: 2, Rohtas: 2.

---

## 5. P1-2 & P1-3: Share View & URL State Restoration

### Issue
- `shareMapView()` was scoped only inside Google Maps initialization and unavailable in Leaflet mode.
- Leaflet map initialization did not restore `lat`, `lng`, `zoom` query parameters.

### Files Changed
- `templates/explore_map.html`:
  - Elevated `shareMapView()` and `showShareToast()` to shared global window scope.
  - Detects active map engine (`googleMap` vs Leaflet `map`), extracts center coordinates, zoom level, and active filters.
  - Added URL parameter parsing to Leaflet initialization block: restores `lat`, `lng`, `zoom` using `map.setView([lat, lng], zoom)`.

### Tests Performed
- Automated test `test_share_url_generation_logic`.
- Browser test clicked Share button; verified toast notification and URL copy generation.

---

## 6. P1-4: Outer Bihar State Boundary Layer

### Issue
- State Boundary layer previously fell back to internal district boundaries or lacked source.

### Files Changed
- `static/data/bihar/state_boundary.geojson`: Added authoritative Survey of India / Census 2011 outer boundary GeoJSON.
- `static/js/map/map-layers.js`: Configured `source: '/static/data/bihar/state_boundary.geojson'`, enabled for `['google', 'leaflet', 'maplibre']`.
- `static/js/map/map-google-layers.js`: Removed legacy fallback to `districts.geojson`.

### Tests Performed
- Verified HTTP 200 retrieval of `/static/data/bihar/state_boundary.geojson`.
- Verified single outer boundary polygon rendering.

---

## 7. P1-5: Layer Manager Inactive Toggles Resolution

### Issue
- Several layers in Layer Manager (`highways`, `railway`, `hills_mountains`, `heatmap`, `density`, etc.) had no backing data sources but displayed active toggle switches.

### Files Changed
- `static/js/map/map-layers.js`: Explicitly marked unimplemented layers with `disabled: true`.
- `static/js/map/map-controls.js`:
  - Updated layer toggle rendering: disabled layers display a distinct, styled `"Planned"` badge instead of an active toggle switch.
  - Guarded `_onLayerToggle()` to reject events for disabled layers.
  - Connected `restaurants` layer to `/api/nearby?category=restaurant` across Google Maps, Leaflet, and MapLibre adapters.

### Tests Performed
- Visual browser verification confirmed "Planned" badges for unimplemented layers; no dead toggles.

---

## 8. P1-6: Category Filter Coverage & Consistency

### Issue
- Database categories such as `religious`, `wildlife`, `park`, `fort`, `monument` were not matched by frontend filter chips (`temple`, `nature`, `historical`).

### Files Changed
- `templates/explore_map.html`:
  - Added `matchesCategory(place, selectedCat)` supporting:
    - `hidden_gem`: `p.is_hidden_gem === 1`
    - `temple`: `temple` + `religious`
    - `nature`: `nature` + `wildlife` + `park`
    - `historical`: `historical` + `fort` + `monument`
    - `waterfall`: `waterfall`
    - `lake`: `lake`
    - `museum`: `museum`
    - `mountain`: `mountain`
  - Integrated into both Leaflet and Google Maps `applyFilters()` pipelines.

### Tests Performed
- Automated test `test_category_matching_rules`.

---

## 9. P1-7: Search Radius Function

### Issue
- `window.HY_setSearchRadius()` was dead code referencing nonexistent `HY_MAP_INSTANCE` and `HY_RADIUS_CIRCLE`.

### Files Changed
- `static/js/smart-nearby.js`: Added `SNS.setRadius(radiusKm)` updating `currentRadius`, UI buttons/pills, map circle, and calling `SNS.fetchNearby()`.
- `static/js/map.js`: Updated `window.HY_setSearchRadius` to delegate to `window.SNS.setRadius(radiusKm)`.

### Tests Performed
- Verified invocation of `window.HY_setSearchRadius(10)` updates radius pills and triggers nearby search.

---

## 10. P1-8: Deep-Link Fallback Handling

### Issue
- Deep linking with an invalid or deleted `place_id` produced no user feedback.

### Files Changed
- `templates/explore_map.html`: Added user-visible toast fallback when a queried `place_id` cannot be found on the map.

### Tests Performed
- Automated tests `test_explore_deep_link_valid_place` and `test_explore_deep_link_invalid_place_graceful_fallback`.
