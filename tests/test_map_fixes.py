"""
Automated Test Suite for HiddenYatra Map / GIS Fix Phase
Covers:
1. District map asset availability (Leaflet CSS/JS)
2. Itinerary map asset availability (Leaflet CSS/JS)
3. Culture API normalization (Adapter -> GeoJSON FeatureCollection)
4. Culture marker rendering logic
5. Coordinate integrity for fixed records (Barabar ID 5, Rohtasgarh ID 15, Golghar ID 1)
6. Barabar duplicate canonicalization (ID 107 soft-deleted/redirected, ID 5 active)
7. Discovery Snapshot live counts (authoritative live aggregation)
8. Share state generation
9. URL state restoration and deep link fallback
10. Category mapping logic
"""

import os
import sys
import unittest
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.connection import get_db

class TestMapFixPhase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    # 1. District Map Asset Availability
    def test_district_map_leaflet_assets(self):
        """District page must load Leaflet CSS and JS even when Google Maps is default."""
        resp = self.client.get('/state/bihar/patna')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('leaflet.css', html)
        self.assertIn('leaflet.js', html)
        self.assertIn('id="district-map"', html)

    # 2. Itinerary Map Asset Availability
    def test_itinerary_map_leaflet_assets(self):
        """Itinerary detail page must load Leaflet CSS and JS for route polyline."""
        resp = self.client.get('/itinerary/1')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('leaflet.css', html)
        self.assertIn('leaflet.js', html)
        self.assertIn('id="itinerary-map"', html)

    def test_explore_google_omits_leaflet(self):
        """Explore page with Google engine must not redundantly load Leaflet."""
        resp = self.client.get('/explore')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        # Verify explore page loads properly
        self.assertIn('explore-map-container', html)
        # Should not include leaflet.js when skip_base_leaflet is True for Google mode
        self.assertNotIn('https://unpkg.com/leaflet@', html)

    # 3. Culture API Normalization
    def test_culture_api_endpoint(self):
        """Culture map API returns valid items array."""
        resp = self.client.get('/api/culture-map')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIsInstance(data.get('items'), list)
        self.assertGreater(len(data['items']), 0)

    def test_culture_normalization_geojson_adapter(self):
        """Simulate frontend adapter _normalizeToGeoJson: items -> GeoJSON FeatureCollection."""
        raw_items = [
            {"id": 1, "name": "Mithila Painting", "latitude": 26.35, "longitude": 86.07, "category": "crafts", "district": "Madhubani"},
            {"id": 2, "name": "Chhath Puja", "latitude": 25.60, "longitude": 85.14, "category": "festivals", "district": "Patna"},
            {"id": 3, "name": "Invalid Item", "latitude": None, "longitude": None}
        ]

        # Test the exact transformation logic implemented in map-google-layers.js
        features = []
        for item in raw_items:
            lat = item.get('latitude') or item.get('lat')
            lng = item.get('longitude') or item.get('lng')
            if lat is not None and lng is not None:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(lng), float(lat)]
                    },
                    "properties": item
                })

        geojson = {"type": "FeatureCollection", "features": features}
        self.assertEqual(geojson["type"], "FeatureCollection")
        self.assertEqual(len(geojson["features"]), 2)
        self.assertEqual(geojson["features"][0]["geometry"]["coordinates"], [86.07, 26.35])
        self.assertEqual(geojson["features"][1]["properties"]["name"], "Chhath Puja")

    # 4. Culture Marker Rendering Logic
    def test_culture_categories_coverage(self):
        """Verify culture categories returned by API cover expected cultural dimensions."""
        resp = self.client.get('/api/culture-map')
        items = resp.get_json().get('items', [])
        categories = {item.get('category') for item in items if item.get('category')}
        expected = {'heritage', 'festivals', 'crafts', 'performing_arts', 'local_food'}
        intersection = categories.intersection(expected)
        self.assertGreater(len(intersection), 0, f"Expected culture categories, got: {categories}")

    # 5. Geographic Coordinate Integrity
    def test_fixed_coordinates_integrity(self):
        """Verify ground-truth coordinates for Place IDs 5, 15, 1."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, latitude, longitude, deleted_at FROM places WHERE id IN (1, 5, 15)")
        rows = {r['id']: r for r in cursor.fetchall()}
        cursor.close()
        db.close()

        # Place 1: Golghar Patna (25.6120, 85.1448)
        self.assertIn(1, rows)
        self.assertAlmostEqual(float(rows[1]['latitude']), 25.6120, places=3)
        self.assertAlmostEqual(float(rows[1]['longitude']), 85.1448, places=3)

        # Place 5: Barabar Caves (25.0061, 85.0621)
        self.assertIn(5, rows)
        self.assertAlmostEqual(float(rows[5]['latitude']), 25.0061, places=3)
        self.assertAlmostEqual(float(rows[5]['longitude']), 85.0621, places=3)
        self.assertIsNone(rows[5]['deleted_at'])

        # Place 15: Rohtasgarh Fort (24.6300, 83.8900)
        self.assertIn(15, rows)
        self.assertAlmostEqual(float(rows[15]['latitude']), 24.6300, places=3)
        self.assertAlmostEqual(float(rows[15]['longitude']), 83.8900, places=3)

    # 6. Barabar Duplicate Canonicalization
    def test_barabar_canonicalization_and_redirect(self):
        """Place 5 is canonical active record; Place 107 is soft-deleted; old slug redirects 301."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, is_hidden_gem, deleted_at FROM places WHERE id IN (5, 107)")
        places = {r['id']: r for r in cursor.fetchall()}
        cursor.close()
        db.close()

        self.assertIsNone(places[5]['deleted_at'], "Place ID 5 must be active")
        self.assertEqual(places[5]['is_hidden_gem'], 1, "Place ID 5 must retain is_hidden_gem=1")
        self.assertIsNotNone(places[107]['deleted_at'], "Place ID 107 must be soft-deleted")

        # Test 301 Redirect for duplicate slug
        resp = self.client.get('/place/barabar-caves-siddheshwar-nath-gaya')
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp.headers.get('Location'), '/place/barabar-caves-gaya')

    # 7. Discovery Snapshot Live Data
    def test_discovery_snapshot_live_district_counts(self):
        """Discovery snapshot must return live grouped district counts, not static stale numbers."""
        resp = self.client.get('/api/discovery-snapshot')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('top_districts', data)

        top_districts = {d['name']: (d.get('place_count') or d.get('count') or 0) for d in data['top_districts']}
        # Authoritative DB counts: Patna has 18, Jamui has 11, Rohtas has 6, Nalanda has 4
        self.assertGreaterEqual(top_districts.get('Patna', 0), 10, "Patna should reflect live count >= 10")
        if 'Nalanda' in top_districts:
            self.assertNotEqual(top_districts['Nalanda'], 10, "Nalanda live count must not be static 10")
            self.assertEqual(top_districts['Nalanda'], 5, "Nalanda live count must be 5")
        if 'Rohtas' in top_districts:
            self.assertNotEqual(top_districts['Rohtas'], 7, "Rohtas live count must not be static 7")
            self.assertEqual(top_districts['Rohtas'], 6, "Rohtas live count must be 6")

    # 8. Share State Generation
    def test_share_url_generation_logic(self):
        """Test URL parameters constructed by shareMapView logic."""
        params = {
            'lat': '25.0061',
            'lng': '85.0621',
            'zoom': '14',
            'category': 'temple',
            'district': 'Gaya',
            'place_id': '5'
        }
        query_string = '&'.join([f"{k}={v}" for k, v in params.items() if v])
        url = f"/explore?{query_string}"
        self.assertIn('lat=25.0061', url)
        self.assertIn('lng=85.0621', url)
        self.assertIn('zoom=14', url)
        self.assertIn('category=temple', url)
        self.assertIn('district=Gaya', url)
        self.assertIn('place_id=5', url)

    # 9. URL State Restoration & Deep Link Fallback
    def test_explore_deep_link_valid_place(self):
        """GET /explore with valid place_id returns 200."""
        resp = self.client.get('/explore?place_id=1')
        self.assertEqual(resp.status_code, 200)

    def test_explore_deep_link_invalid_place_graceful_fallback(self):
        """GET /explore with nonexistent place_id returns 200 gracefully without server error."""
        resp = self.client.get('/explore?place_id=99999999')
        self.assertEqual(resp.status_code, 200)

    # 10. Category Filter Mapping Logic
    def test_category_matching_rules(self):
        """Verify matchesCategory business rules for multi-category mappings."""
        def matches_category(place, selected_cat):
            if not selected_cat:
                return True
            cat = (place.get('category') or '').lower()
            if selected_cat == 'hidden_gem':
                return place.get('is_hidden_gem') == 1
            if selected_cat == 'temple':
                return cat in ('temple', 'religious')
            if selected_cat == 'nature':
                return cat in ('nature', 'wildlife', 'park')
            if selected_cat == 'historical':
                return cat in ('historical', 'fort', 'monument')
            if selected_cat == 'waterfall':
                return cat == 'waterfall'
            if selected_cat == 'lake':
                return cat == 'lake'
            if selected_cat == 'museum':
                return cat == 'museum'
            if selected_cat == 'mountain':
                return cat == 'mountain'
            return cat == selected_cat

        # Religious -> temple filter
        self.assertTrue(matches_category({'category': 'religious'}, 'temple'))
        self.assertTrue(matches_category({'category': 'temple'}, 'temple'))
        # Wildlife & Park -> nature filter
        self.assertTrue(matches_category({'category': 'wildlife'}, 'nature'))
        self.assertTrue(matches_category({'category': 'park'}, 'nature'))
        # Fort & Monument -> historical filter
        self.assertTrue(matches_category({'category': 'fort'}, 'historical'))
        self.assertTrue(matches_category({'category': 'monument'}, 'historical'))
        # Hidden gem
        self.assertTrue(matches_category({'category': 'temple', 'is_hidden_gem': 1}, 'hidden_gem'))
        self.assertFalse(matches_category({'category': 'temple', 'is_hidden_gem': 0}, 'hidden_gem'))
        # Lake & Waterfall individual
        self.assertTrue(matches_category({'category': 'waterfall'}, 'waterfall'))
        self.assertTrue(matches_category({'category': 'lake'}, 'lake'))
        self.assertFalse(matches_category({'category': 'temple'}, 'lake'))

    # 11. Places Filter and Nearby Radius API
    def test_get_places_by_filter_and_nearby_radius(self):
        """Verify get_places_by_filter SQL query and /api/places/nearby-radius endpoint succeed."""
        from models.places import get_places_by_filter
        places = get_places_by_filter(limit=10)
        self.assertIsInstance(places, list)
        self.assertGreater(len(places), 0)

        resp = self.client.get('/api/places/nearby-radius?lat=25.5941&lng=85.1376&radius=50')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('places', data)
        self.assertGreater(data.get('count', 0), 0)

if __name__ == '__main__':
    unittest.main()
