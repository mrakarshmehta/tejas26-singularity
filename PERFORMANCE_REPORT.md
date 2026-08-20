# HiddenYatra — Performance & Asset Optimization Report

This report documents query performance, static asset minification, and caching controls across the HiddenYatra platform.

---

## 1. Database Query Indexing Coverage

- **Table**: `places` (28 rows)
- **Active Indexes**: 14
  1. `PRIMARY` (`id`)
  2. `uq_places_slug` (`slug` UNIQUE)
  3. `idx_places_district` (`district_id`)
  4. `idx_places_category` (`category`)
  5. `idx_places_state` (`state_id`)
  6. `idx_places_featured` (`is_featured`)
  7. `idx_places_views` (`view_count`)
  8. `idx_places_lat_lng` (`latitude`, `longitude`)
  9. `idx_places_created` (`created_at`)
  10. `idx_places_deleted` (`deleted_at`)
  11. `idx_places_slug_deleted` (`slug`, `deleted_at`)
  12. `idx_places_featured_views` (`is_featured`, `view_count`)
  13. `idx_places_block` (`block_id`)
  14. `ft_places_search` (`FULLTEXT` search index on `name`, `description`, `history`, `local_food`)

---

## 2. Static Asset Minification

All 13 static CSS and JavaScript files have been minified via `scripts/tools/minify_assets.py`:

- `sw.js` (1673 -> 1170 bytes)
- `admin.css` (30379 -> 25023 bytes)
- `animations.css` (5777 -> 4280 bytes)
- `components.css` (42630 -> 35887 bytes)
- `explore-map.css` (16591 -> 13044 bytes)
- `main.css` (39638 -> 33055 bytes)
- `smart-nearby.css` (9067 -> 7021 bytes)
- `admin.js` (2553 -> 1806 bytes)
- `app.js` (7689 -> 6025 bytes)
- `gallery.js` (2616 -> 2084 bytes)
- `map.js` (16874 -> 11593 bytes)
- `particles.js` (1437 -> 1169 bytes)
- `smart-nearby.js` (16197 -> 12065 bytes)

---

## 3. HTTP Caching Headers (Configured in `app.py`)

- **CSS & JS static assets**: `Cache-Control: public, max-age=3600` (1 hour) + query string versioning (`?v=10`)
- **Images & Icons**: `Cache-Control: public, max-age=86400` (1 day)
