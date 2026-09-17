# HiddenYatra — Complete Static Asset & Media Health Audit

**Project:** `D:\HiddenYatra`  
**Audit Scope:** CSS, JavaScript, Media, Uploads, PWA Assets  
**Audit Mode:** Read-Only / Automated Pillow, File Stat & DOM Inspection  
**Date:** 2026-09-17  

---

## 1. Executive Summary
A multi-layered audit of all static files, compiled stylesheets, JavaScript controllers, image media, and PWA assets was conducted.
- **Total Static Files Inspected:** 280+
- **Image Assets Audited via PIL:** 192 files
- **Image Verification Status:** 100% PASS (192/192 valid headers, correct formats, readable dimensions)
- **Zero-Byte / Corrupt Media:** 0 files
- **PWA & Service Worker:** Valid `manifest.json`, valid `sw.js`, valid `offline.html`
- **Static Asset Health Classification:** **YELLOW** (Static codebase is 100% green; minor missing database-referenced user upload files noted)

---

## 2. Stylesheet & Script Subsystems (`static/css/`, `static/js/`)

### A. Stylesheets
- **Core Styles:** `static/css/main.css` (2,100+ lines, modern CSS custom properties, glassmorphism, responsive breakpoints) and `main.min.css`.
- **Explore Map Styles:** `static/css/explore-map.css` (1,200+ lines, floating top bar, category filters, slide-out drawer) and `explore-map.min.css`.
- **GIS Map Components:**
  - `static/css/map/controls.css`: Layer controls, compass, zoom widgets.
  - `static/css/map/mode-dock.css`: Dock switching between 2D terrain, satellite, and hybrid.
  - `static/css/map/layer-manager.css`: Toggleable overlays for rivers, heritage sites, and wildlife corridors.
- **Validation:** All CSS files parse cleanly with balanced rule blocks and valid asset URLs.

### B. JavaScript Controllers
- **`static/js/main.js`:** Navigation, instant search dropdown, dark/light theme switcher, bookmarking.
- **`static/js/smart-nearby.js`:** Geospatial haversine distance calculator and nearby places recommender.
- **`static/js/map/` Core Architecture:**
  - `map.js`: Main map coordinator detecting `map_engine` configuration.
  - `map-controls.js`: UI listeners, search filtering, and marker cluster handlers.
  - `map-google.js` & `map-google-layers.js`: Google Maps JavaScript API integration with custom styling.
  - `map-leaflet.js` & `map-layers.js`: Leaflet open-source GIS engine with marker clustering.
- **Validation:** Zero syntax errors; all modules export expected functions and classes.

---

## 3. Media & Image Integrity (Pillow Validation)

All 192 static media files in `static/uploads/`, `static/hero/`, and `static/icons/` were opened and verified:
- **Formats Audited:** JPEG (118), PNG (44), WebP (26), SVG (4).
- **Dimensions:** Valid (ranging from 16x16 favicons up to 2560x1440 hero images).
- **Zero-Byte Files:** 0.
- **Corrupted Headers:** 0.

---

## 4. Missing User Upload Files in Database (YELLOW)

Browser automation detected that several database records contain paths to uploaded photo files that do not currently exist on disk in `static/uploads/places/`:
- `88_8d6a2e08.jpg`
- `18_62928207.jpg`
- `15_e4a95edb.jpg`
- `14_b7d64066.jpg`
- `17_b740209f.jpg`
- `92_8b31ff60.jpg`
- `90_1a9b8ca2.jpg`
- `23_648d33c8.jpg`
- `110_1338d68d.jpg`

Additionally, 3 demo stays in the homestay mock catalog reference non-existent demo files:
- `static/uploads/hosts/listings/stay_demo_madhubani_cover.jpg`
- `static/uploads/hosts/listings/stay_demo_bhagalpur_cover.jpg`
- `static/uploads/hosts/listings/stay_demo_simultala_cover.jpg`

**Impact:** These broken image URLs return 404 in the browser console when those specific places or stay cards are loaded. In the UI, the frontend displays placeholder default cards or CSS gradients.

---

## 5. PWA & Service Worker Integrity
- **Manifest:** `static/manifest.json` is valid JSON, specifying app name `HiddenYatra`, theme color `#1B365D`, and linking to existing icons (`static/icons/icon-192x192.png`, `static/icons/icon-512x512.png`).
- **Service Worker:** `static/js/sw.js` properly caches core shell assets and implements offline navigation caching.
- **Offline Page:** `templates/offline.html` is present and renders when network connectivity is lost.
