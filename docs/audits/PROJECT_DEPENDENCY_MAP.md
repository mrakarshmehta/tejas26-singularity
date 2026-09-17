# HiddenYatra — Architectural Dependency Map

## 1. Blueprint to Route & Template Mapping

```
app.py (Flask Application Factory)
│
├── routes/main.py (main_bp)
│   ├── / -> index.html (Main landing page, hero search, trending places)
│   ├── /browse -> browse.html (Categorical catalog)
│   ├── /explore -> explore_map.html (Interactive Leaflet/MapLibre GIS explorer)
│   ├── /state -> state.html (State-level overview)
│   ├── /crafts -> crafts.html / craft_detail.html
│   ├── /festivals -> festivals.html / festival_detail.html
│   ├── /gastronomy -> gastronomy.html / dish_detail.html
│   ├── /wildlife -> wildlife.html / wildlife_detail.html
│   ├── /treks -> treks.html / trek_detail.html
│   └── /safety -> safety.html (Women & tourist emergency safety network)
│
├── routes/places.py (places_bp)
│   ├── /places/<slug> -> place.html (Rich canonical place details)
│   └── /districts/<slug> -> district.html (District tourism portal)
│
├── routes/api.py (api_bp)
│   ├── /api/places -> JSON place inventory (geojson, bounds, filters)
│   ├── /api/instant-search -> models/search_engine.py
│   ├── /api/places/<id>/nearby -> Haversine smart nearby recommendations
│   ├── /api/districts -> GeoJSON polygon boundary layer
│   └── /api/blocks -> Sub-district block spatial geometries
│
├── routes/auth.py (auth_bp)
│   ├── /auth/login -> auth/login.html
│   ├── /auth/signup -> auth/signup.html
│   └── /auth/logout -> Redirect
│
├── routes/admin.py (admin_bp)
│   ├── /admin -> admin/dashboard.html
│   ├── /admin/places -> admin/places.html
│   └── /admin/analytics -> admin/analytics.html
│
├── routes/itinerary.py (itinerary_bp)
│   ├── /itinerary -> itinerary.html (AI smart trip planner)
│   └── /itinerary/generate -> models/itineraries.py (Algorithmic circuit generator)
│
└── routes/stays.py (stays_bp)
    ├── /stays -> stays/index.html
    └── /stays/<id> -> stays/detail.html
```

---

## 2. GIS & Mapping Data Pipeline

```
Client Browser (explore_map.html)
│
├── static/css/explore-map.css
├── static/css/map/advanced-map.css
│
├── static/js/map/map-core.js (Map initialization, state manager)
│   ├── Leaflet.js / MapLibre GL JS engine
│   └── static/js/map/map-modes.js (2D, 3D Terrain, Satellite toggles)
│
├── static/js/map/map-layers.js (Spatial Vector Layer Manager)
│   ├── fetch('/static/data/bihar/districts.geojson') -> District Boundaries
│   ├── fetch('/static/data/bihar/blocks.geojson') -> Sub-District Polygons
│   ├── fetch('/static/data/bihar/rivers.geojson') -> Gangetic River Network
│   ├── fetch('/static/data/bihar/forests.geojson') -> Protected Forest Reserves
│   └── fetch('/static/data/bihar/lakes_dams.geojson') -> Waterbodies
│
└── static/js/map/map-google-terrain.js (3D Terrain Mesh Subsystem)
    ├── static/js/map/map-google-terrain-loader.js
    │   └── fetch('/static/data/terrain/bihar/manifest.json')
    └── static/js/map/map-google-terrain-worker.js
        └── fetch('/static/data/terrain/bihar/z{z}/{x}_{y}.bin') -> Elevation Grid
```

---

## 3. Search Engine Pipeline

```
User Input Query ("Bodh Gaya" or "waterfall")
│
▼
static/js/search.js (Client Debounced Auto-Complete)
│
▼ (HTTP GET /api/instant-search?q=...)
routes/api.py: instant_search()
│
▼
models/search_engine.py: search_places(query)
│
├── In-Memory Inverted Index (Trie Prefix Matching)
├── Fuzzy Levenshtein Distance Matcher
├── Synonym & Category Normalization
└── BM25 Weighted Scoring (Title > Category > District > Description)
│
▼
JSON Response [{id, name, slug, category, district, rating, image}]
│
▼
Rendered in Client Autocomplete Modal / Search Results Page
```

---

## 4. Database Connection & Model Dependencies

```
models/connection.py (Connection Pool & Transaction Manager)
│
├── models/database.py (Schema initialization & core lookups)
│   └── places, districts, categories tables
│
├── models/places.py
│   └── places, place_photos, place_reviews, place_amenities
│
├── models/search_engine.py
│   └── queries places + districts to populate in-memory search index
│
├── models/admin_db.py
│   └── administrative statistics, audit logs, place verification
│
├── models/stays.py & stay_requests.py
│   └── stays, hosts, booking_requests
│
└── models/auth.py
    └── users, sessions, roles, permissions
```
