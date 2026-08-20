"""
Tests for HiddenYatra Advanced Custom Map (HYMap) System.
Verifies template integration, asset presence, GeoJSON integrity, and security.
"""
import os
import json
import unittest
from app import create_app


class TestHYMapSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def test_explore_route_renders_hymap_assets(self):
        """Verify /explore endpoint serves all HYMap scripts and stylesheets in default Google mode."""
        response = self.client.get('/explore')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Check CSS
        self.assertIn('layer-manager.css', html)
        self.assertIn('controls.css', html)
        self.assertIn('mode-dock.css', html)

        # Check JS modules for Google mode (system default)
        expected_modules = [
            'map-state.js',
            'map-layers.js',
            'map-markers.js',
            'map-google.js',
            'map-google-layers.js',
            'map-google-terrain.js',
            'map-google-terrain-mesh.js',
            'map-google-terrain-loader.js',
            'map-controls.js',
            'map-modes.js',
            'map-core.js',
        ]
        for mod in expected_modules:
            self.assertIn(mod, html, f"Missing JS module in /explore: {mod}")

        # Check Google Maps engine global
        self.assertIn("MAP_ENGINE = 'google'", html)

    def test_leaflet_compatibility_mode_renders_leaflet_assets(self):
        """Verify /explore endpoint serves Leaflet assets when MAP_ENGINE=leaflet is explicitly requested."""
        os.environ['MAP_ENGINE'] = 'leaflet'
        import importlib
        import config as cfg_mod
        importlib.reload(cfg_mod)
        app_leaflet = create_app()
        client_leaflet = app_leaflet.test_client()

        response = client_leaflet.get('/explore')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Check Leaflet JS modules
        self.assertIn('map-leaflet.js', html)
        self.assertIn('leaflet@1.9.4/dist/leaflet.js', html)
        self.assertIn('new HYMap(map,', html)
        self.assertIn('hyMap.init();', html)

        # Clean up
        os.environ.pop('MAP_ENGINE', None)
        importlib.reload(cfg_mod)

    def test_districts_geojson_validity(self):
        """Verify Bihar districts GeoJSON has exactly 38 valid polygon features."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'districts.geojson')
        self.assertTrue(os.path.exists(geojson_path), "districts.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        features = data.get('features', [])
        self.assertEqual(len(features), 38, f"Expected 38 districts, found {len(features)}")

        district_names = set()
        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('name', props)
            district_names.add(props['name'])
            geom = feature.get('geometry', {})
            self.assertEqual(geom.get('type'), 'Polygon')
            self.assertGreaterEqual(len(geom.get('coordinates', [[]])[0]), 4)

        self.assertEqual(len(district_names), 38, "Duplicate district names in GeoJSON")

    def test_all_hymap_asset_files_exist(self):
        """Verify all JS and CSS map assets exist on filesystem."""
        expected_files = [
            os.path.join('static', 'js', 'map', 'map-state.js'),
            os.path.join('static', 'js', 'map', 'map-layers.js'),
            os.path.join('static', 'js', 'map', 'map-markers.js'),
            os.path.join('static', 'js', 'map', 'map-leaflet.js'),
            os.path.join('static', 'js', 'map', 'map-maplibre.js'),
            os.path.join('static', 'js', 'map', 'map-transition.js'),
            os.path.join('static', 'js', 'map', 'map-controls.js'),
            os.path.join('static', 'js', 'map', 'map-modes.js'),
            os.path.join('static', 'js', 'map', 'map-core.js'),
            os.path.join('static', 'css', 'map', 'controls.css'),
            os.path.join('static', 'css', 'map', 'layer-manager.css'),
            os.path.join('static', 'css', 'map', 'mode-dock.css'),
            os.path.join('static', 'data', 'bihar', 'districts.geojson'),
        ]
        for rel_path in expected_files:
            full_path = os.path.join(self.base_dir, rel_path)
            self.assertTrue(os.path.exists(full_path), f"HYMap asset missing: {rel_path}")
            self.assertGreater(os.path.getsize(full_path), 0, f"Asset empty: {rel_path}")

    def test_map_modes_definitions(self):
        """Verify map-modes.js contains all 6 required modes (Normal, Dark, Terrain, 3D, Satellite, Hybrid)."""
        modes_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-modes.js')
        with open(modes_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for mode_key in ['normal', 'dark', 'terrain', 'terrain3d', 'satellite', 'hybrid']:
            self.assertIn(f"id: '{mode_key}'", content, f"Missing mode definition for: {mode_key}")

    def test_hybrid_tile_source_defined(self):
        """Verify carto_labels tile source exists in map-layers.js for Hybrid mode."""
        layers_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-layers.js')
        with open(layers_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('carto_labels', content)
        self.assertIn('light_only_labels', content)

    def test_layer_manager_seven_groups_defined(self):
        """Verify all 7 required UI sections exist in HY_LAYER_GROUPS."""
        layers_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-layers.js')
        with open(layers_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        expected_groups = [
            'terrain',
            'natural_geography',
            'boundaries',
            'tourism',
            'roads_transport',
            'routes',
            'analytics',
        ]
        for group in expected_groups:
            self.assertIn(f"id: '{group}'", content, f"Missing layer group definition: {group}")

    def test_layer_definitions_hierarchy_and_keys(self):
        """Verify layer definitions contain required fields and hierarchical parent/child associations."""
        layers_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-layers.js')
        with open(layers_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check key layers across all 7 categories
        expected_layer_ids = [
            # Terrain
            'terrain_relief', 'hillshade', '3d_terrain',
            # Natural Geography
            'natural_geography', 'rivers', 'lakes_dams', 'forests', 'waterfalls_geo', 'hills_mountains',
            # Boundaries
            'boundaries', 'state_boundary', 'district_boundaries', 'block_boundaries',
            # Tourism
            'tourist_places', 'temple', 'fort', 'waterfall', 'historical', 'religious',
            'nature', 'hidden_gem', 'viewpoint', 'hotels', 'homestays', 'restaurants', 'local_food', 'user_submitted',
            # Roads & Transport
            'roads_transport', 'highways', 'major_roads', 'local_roads', 'railway',
            # Routes
            'routes', 'my_location', 'active_routes', 'distance_measurement',
            # Analytics
            'analytics', 'heatmap', 'density',
        ]
        for layer_id in expected_layer_ids:
            self.assertIn(f"id: '{layer_id}'", content, f"Missing layer ID: {layer_id}")

        # Check export names
        self.assertIn('root.HY_LAYERS =', content)
        self.assertIn('root.HY_LAYER_GROUPS =', content)
        self.assertIn('root.HYLayerRegistry =', content)

    def test_map_state_hierarchical_methods(self):
        """Verify MapState contains hierarchical propagation, opacity, and bulk layer control methods."""
        state_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-state.js')
        with open(state_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        expected_methods = [
            'setLayerVisible',
            'isLayerVisible',
            'isLayerEnabled',
            'setLayerOpacity',
            'getLayerOpacity',
            'resetLayers',
            'hideAllLayers',
            'showAllLayers',
            'getActiveLayerCount',
        ]
        for method in expected_methods:
            self.assertIn(method, content, f"Missing MapState method: {method}")

    def test_layer_manager_controls_and_accessibility(self):
        """Verify MapControls provides search, quick action toolbar, accessibility, and backdrop."""
        controls_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-controls.js')
        with open(controls_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('hy-lm-backdrop', content)
        self.assertIn('hy-lm-search', content)
        self.assertIn('hy-lm-btn-reset', content)
        self.assertIn('hy-lm-btn-show-all', content)
        self.assertIn('hy-lm-btn-hide-all', content)
        self.assertIn("setAttribute('role', 'dialog')", content)
        self.assertIn('role="switch"', content)
        self.assertIn('aria-checked', content)

    def test_rivers_geojson_validity(self):
        """Verify Bihar rivers GeoJSON has valid LineString/MultiLineString features with genuine OSM metadata."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'rivers.geojson')
        self.assertTrue(os.path.exists(geojson_path), "rivers.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        self.assertEqual(data.get('metadata', {}).get('source'), 'OpenStreetMap')
        features = data.get('features', [])
        self.assertGreaterEqual(len(features), 10, f"Expected >=10 rivers, found {len(features)}")

        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('name', props)
            self.assertIn('source', props)
            self.assertEqual(props['source'], 'OpenStreetMap')
            self.assertIn('osm_primary_id', props)
            geom = feature.get('geometry', {})
            self.assertIn(geom.get('type'), ['LineString', 'MultiLineString'])
            coords = geom.get('coordinates', [])
            self.assertGreaterEqual(len(coords), 1)
            all_pts = coords if geom.get('type') == 'LineString' else [pt for seg in coords for pt in seg]
            for pt in all_pts:
                lng, lat = pt[0], pt[1]
                self.assertTrue(83.0 <= lng <= 88.5, f"Lng {lng} out of Bihar bounds in {props.get('name')}")
                self.assertTrue(24.0 <= lat <= 27.8, f"Lat {lat} out of Bihar bounds in {props.get('name')}")

    def test_lakes_dams_geojson_validity(self):
        """Verify Bihar lakes & dams GeoJSON has valid closed Polygon features with genuine OSM metadata."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'lakes_dams.geojson')
        self.assertTrue(os.path.exists(geojson_path), "lakes_dams.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        self.assertEqual(data.get('metadata', {}).get('source'), 'OpenStreetMap')
        features = data.get('features', [])
        self.assertGreaterEqual(len(features), 10, f"Expected >=10 lakes/dams, found {len(features)}")

        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('name', props)
            self.assertIn('source', props)
            self.assertEqual(props['source'], 'OpenStreetMap')
            self.assertIn('osm_id', props)
            geom = feature.get('geometry', {})
            self.assertIn(geom.get('type'), ['Polygon', 'MultiPolygon'])
            coords = geom.get('coordinates', [])
            self.assertGreaterEqual(len(coords), 1)
            ring = coords[0]
            self.assertEqual(ring[0], ring[-1], f"Polygon not closed in {props.get('name')}")
            for pt in ring:
                lng, lat = pt[0], pt[1]
                self.assertTrue(83.0 <= lng <= 88.5, f"Lng {lng} out of Bihar bounds in {props.get('name')}")
                self.assertTrue(24.0 <= lat <= 27.8, f"Lat {lat} out of Bihar bounds in {props.get('name')}")

    def test_rivers_and_lakes_layer_registry_sources(self):
        """Verify rivers, lakes_dams, forests, and waterfalls layers in map-layers.js point to valid GeoJSON endpoints."""
        layers_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-layers.js')
        with open(layers_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("source: '/static/data/bihar/rivers.geojson'", content)
        self.assertIn("source: '/static/data/bihar/lakes_dams.geojson'", content)
        self.assertIn("source: '/static/data/bihar/forests.geojson'", content)
        self.assertIn("source: '/static/data/bihar/waterfalls.geojson'", content)

    def test_forests_geojson_validity(self):
        """Verify Bihar forests GeoJSON has valid closed Polygon features with genuine OSM metadata."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'forests.geojson')
        self.assertTrue(os.path.exists(geojson_path), "forests.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        self.assertEqual(data.get('metadata', {}).get('source'), 'OpenStreetMap')
        features = data.get('features', [])
        self.assertGreaterEqual(len(features), 5, f"Expected >=5 forests, found {len(features)}")

        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('name', props)
            self.assertIn('source', props)
            self.assertEqual(props['source'], 'OpenStreetMap')
            self.assertIn('osm_id', props)
            geom = feature.get('geometry', {})
            self.assertIn(geom.get('type'), ['Polygon', 'MultiPolygon'])
            coords = geom.get('coordinates', [])
            self.assertGreaterEqual(len(coords), 1)
            ring = coords[0]
            self.assertEqual(ring[0], ring[-1], f"Polygon not closed in {props.get('name')}")
            for pt in ring:
                lng, lat = pt[0], pt[1]
                self.assertTrue(83.0 <= lng <= 88.5, f"Lng {lng} out of Bihar bounds in {props.get('name')}")
                self.assertTrue(24.0 <= lat <= 27.8, f"Lat {lat} out of Bihar bounds in {props.get('name')}")

    def test_waterfalls_geojson_validity(self):
        """Verify Bihar waterfalls GeoJSON has valid Point features with genuine OSM metadata."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'waterfalls.geojson')
        self.assertTrue(os.path.exists(geojson_path), "waterfalls.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        self.assertEqual(data.get('metadata', {}).get('source'), 'OpenStreetMap')
        features = data.get('features', [])
        self.assertGreaterEqual(len(features), 1, f"Expected >=1 waterfalls, found {len(features)}")

        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('name', props)
            self.assertIn('source', props)
            self.assertEqual(props['source'], 'OpenStreetMap')
            self.assertIn('osm_id', props)
            geom = feature.get('geometry', {})
            self.assertEqual(geom.get('type'), 'Point')
            coords = geom.get('coordinates', [])
            self.assertEqual(len(coords), 2)
            lng, lat = coords[0], coords[1]
            self.assertTrue(83.0 <= lng <= 88.5, f"Lng {lng} out of Bihar bounds in {props.get('name')}")
            self.assertTrue(24.0 <= lat <= 27.8, f"Lat {lat} out of Bihar bounds in {props.get('name')}")


    def test_block_boundaries_layer_registry_source(self):
        """Verify block_boundaries layer in map-layers.js points to /static/data/bihar/blocks.geojson."""
        layers_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-layers.js')
        with open(layers_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("source: '/static/data/bihar/blocks.geojson'", content)
        self.assertIn("id: 'block_boundaries'", content)

    def test_blocks_geojson_validity(self):
        """Verify Bihar blocks GeoJSON has exactly 534 valid closed polygon features across all 38 districts with authentic Census/LGD metadata."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'blocks.geojson')
        self.assertTrue(os.path.exists(geojson_path), "blocks.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        meta = data.get('metadata', {})
        self.assertIn('Census of India', meta.get('source', ''))
        self.assertEqual(meta.get('total_features'), 534)
        self.assertEqual(meta.get('total_districts'), 38)

        features = data.get('features', [])
        self.assertEqual(len(features), 534, f"Expected exactly 534 blocks, got {len(features)}")

        districts_seen = set()
        seeded_matched = 0

        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('name', props)
            self.assertIn('district_id', props)
            self.assertIn('district_name', props)
            self.assertIn('district_slug', props)
            self.assertIn('census_code', props)
            self.assertIn('source', props)

            districts_seen.add(props['district_id'])
            if props.get('block_id'):
                seeded_matched += 1
                self.assertIsNotNone(props.get('slug'))

            geom = feature.get('geometry', {})
            self.assertIn(geom.get('type'), ['Polygon', 'MultiPolygon'])
            coords = geom.get('coordinates', [])
            self.assertGreaterEqual(len(coords), 1)

            polys = coords if geom.get('type') == 'MultiPolygon' else [coords]
            for poly in polys:
                ring = poly[0]
                self.assertEqual(ring[0], ring[-1], f"Polygon not closed in {props.get('name')}")
                for pt in ring:
                    lng, lat = pt[0], pt[1]
                    self.assertTrue(83.0 <= lng <= 88.5, f"Lng {lng} out of Bihar bounds in {props.get('name')}")
                    self.assertTrue(24.0 <= lat <= 27.8, f"Lat {lat} out of Bihar bounds in {props.get('name')}")

        self.assertEqual(len(districts_seen), 38, f"Expected 38 districts, found {len(districts_seen)}")
        self.assertGreaterEqual(seeded_matched, 90, f"Expected >=90 matched seeded blocks, got {seeded_matched}")

    def test_hotels_and_homestays_layer_registry_sources(self):
        """Verify hotels and homestays layers in map-layers.js point to static GeoJSON endpoints."""
        layers_js_path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-layers.js')
        with open(layers_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("source: '/static/data/bihar/hotels.geojson'", content)
        self.assertIn("source: '/static/data/bihar/homestays.geojson'", content)

    def test_hotels_geojson_validity(self):
        """Verify Bihar hotels GeoJSON has exactly 12 valid Point features with zero private host data."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'hotels.geojson')
        self.assertTrue(os.path.exists(geojson_path), "hotels.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        features = data.get('features', [])
        self.assertEqual(len(features), 12, f"Expected exactly 12 hotel features, got {len(features)}")

        private_keys = {'host_phone', 'host_email', 'id_number_hash', 'address_full', 'password', 'emergency_phone', 'emergency_name'}

        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('name', props)
            self.assertIn('district_id', props)
            self.assertIn('district_name', props)
            self.assertIn('district_slug', props)
            self.assertIn('source', props)

            # Strict Privacy Check
            for pk in private_keys:
                self.assertNotIn(pk, props, f"Private key '{pk}' leaked in hotel properties: {props}")

            geom = feature.get('geometry', {})
            self.assertEqual(geom.get('type'), 'Point')
            coords = geom.get('coordinates', [])
            self.assertEqual(len(coords), 2)
            lng, lat = coords[0], coords[1]
            self.assertTrue(83.0 <= lng <= 88.5, f"Lng {lng} out of Bihar bounds in {props.get('name')}")
            self.assertTrue(24.0 <= lat <= 27.8, f"Lat {lat} out of Bihar bounds in {props.get('name')}")

    def test_homestays_geojson_validity(self):
        """Verify Bihar homestays GeoJSON has exactly 10 valid published Point features with public stay links and zero private host data."""
        geojson_path = os.path.join(self.base_dir, 'static', 'data', 'bihar', 'homestays.geojson')
        self.assertTrue(os.path.exists(geojson_path), "homestays.geojson not found")

        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('type'), 'FeatureCollection')
        features = data.get('features', [])
        self.assertEqual(len(features), 10, f"Expected exactly 10 homestay features, got {len(features)}")

        private_keys = {'host_phone', 'host_email', 'id_number_hash', 'address_full', 'password', 'emergency_phone', 'emergency_name', 'host_id', 'rejection_reason'}

        for feature in features:
            self.assertEqual(feature.get('type'), 'Feature')
            props = feature.get('properties', {})
            self.assertIn('title', props)
            self.assertIn('slug', props)
            self.assertIn('district_name', props)
            self.assertIn('listing_type', props)
            self.assertIn('price_per_night', props)
            self.assertIn('cover_image', props)
            self.assertIn('detail_url', props)
            self.assertTrue(props['detail_url'].startswith('/stays/'), f"Invalid stay URL: {props['detail_url']}")
            self.assertIn('source', props)

            # Strict Privacy Check
            for pk in private_keys:
                self.assertNotIn(pk, props, f"Private key '{pk}' leaked in homestay properties: {props}")

            geom = feature.get('geometry', {})
            self.assertEqual(geom.get('type'), 'Point')
            coords = geom.get('coordinates', [])
            self.assertEqual(len(coords), 2)
            lng, lat = coords[0], coords[1]
            self.assertTrue(83.0 <= lng <= 88.5, f"Lng {lng} out of Bihar bounds in {props.get('title')}")
            self.assertTrue(24.0 <= lat <= 27.8, f"Lat {lat} out of Bihar bounds in {props.get('title')}")


class TestGoogleMapsEngine(unittest.TestCase):
    """Tests for Google Maps engine integration (Phase G1)."""

    @classmethod
    def setUpClass(cls):
        os.environ['MAP_ENGINE'] = 'google'
        os.environ['GOOGLE_MAPS_API_KEY'] = 'test-key-for-unit-tests'
        os.environ['GOOGLE_MAPS_MAP_ID'] = 'test-map-id'
        # Force config module to reload with new env vars
        import importlib
        import config as cfg_mod
        importlib.reload(cfg_mod)
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    @classmethod
    def tearDownClass(cls):
        os.environ.pop('MAP_ENGINE', None)
        os.environ.pop('GOOGLE_MAPS_API_KEY', None)
        os.environ.pop('GOOGLE_MAPS_MAP_ID', None)
        # Reload config to restore defaults for any subsequent tests
        import importlib
        import config as cfg_mod
        importlib.reload(cfg_mod)

    def test_google_engine_loads_google_scripts(self):
        """When MAP_ENGINE=google, template should load Google Maps API and map-google.js."""
        response = self.client.get('/explore')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('maps.googleapis.com', html)
        self.assertIn('map-google.js', html)

    def test_google_engine_excludes_leaflet_scripts(self):
        """When MAP_ENGINE=google, Leaflet CDN scripts must not be present."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertNotIn('leaflet@1.9.4/dist/leaflet.js', html)
        self.assertNotIn('leaflet.markercluster@1.5.3', html)

    def test_google_engine_excludes_leaflet_css(self):
        """When MAP_ENGINE=google, Leaflet CSS must not be loaded."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertNotIn('leaflet@1.9.4/dist/leaflet.css', html)
        self.assertNotIn('MarkerCluster.css', html)

    def test_google_engine_passes_map_id(self):
        """Template must include the Map ID for Vector map initialization."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertIn('test-map-id', html)

    def test_google_engine_passes_api_key(self):
        """Template must include the API key in the Google Maps script URL."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertIn('key=test-key-for-unit-tests', html)

    def test_google_engine_sets_map_engine_global(self):
        """Template must set window.MAP_ENGINE = 'google'."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertIn("MAP_ENGINE = 'google'", html)

    def test_google_engine_has_init_callback(self):
        """Template must define _hyInitGoogleMap callback."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertIn('_hyInitGoogleMap', html)

    def test_google_engine_loads_shared_hymap_scripts(self):
        """Engine-agnostic HYMap scripts must still be loaded in Google mode."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        for mod in ['map-state.js', 'map-layers.js', 'map-markers.js',
                     'map-controls.js', 'map-modes.js', 'map-core.js']:
            self.assertIn(mod, html, f"Missing shared HYMap module: {mod}")

    def test_google_engine_excludes_leaflet_adapter(self):
        """map-leaflet.js, map-maplibre.js, map-transition.js must NOT load in Google mode."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertNotIn('map-leaflet.js', html)
        self.assertNotIn('map-maplibre.js', html)
        self.assertNotIn('map-transition.js', html)

    def test_map_google_js_exists(self):
        """The map-google.js adapter file must exist on disk."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google.js')
        self.assertTrue(os.path.exists(path), f"map-google.js not found at {path}")

    def test_map_core_js_bumped_version(self):
        """map-core.js should be loaded at v1.2 (bumped for Google support)."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertIn('map-core.js?v=1.2', html)

    def test_csp_allows_google_maps(self):
        """CSP headers must whitelist Google Maps domains."""
        response = self.client.get('/explore')
        csp = response.headers.get('Content-Security-Policy', '')
        self.assertIn('maps.googleapis.com', csp)
        self.assertIn('*.googleapis.com', csp)
        self.assertIn('*.gstatic.com', csp)

    def test_hy_google_marker_factory_defined_in_map_markers_js(self):
        """Verify HYGoogleMarkerFactory is defined and exported in map-markers.js."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-markers.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('root.HYGoogleMarkerFactory = GoogleMarkerFactory', content)
        self.assertIn('createPlaceMarkerDOM', content)
        self.assertIn('createPointMarkerDOM', content)
        self.assertIn('createMarker', content)
        self.assertIn('buildPlacePopupHTML', content)
        self.assertIn('buildHotelPopupHTML', content)
        self.assertIn('buildHomestayPopupHTML', content)
        self.assertIn('buildWaterfallPopupHTML', content)

    def test_google_marker_dom_and_aria_attributes(self):
        """Verify Google Advanced Marker DOM includes proper ARIA accessibility and classes."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-markers.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('hy-gmp-marker', content)
        self.assertIn('hy-gmp-pin', content)
        self.assertIn('hy-gmp-emoji', content)
        self.assertIn('role', content)
        self.assertIn('button', content)
        self.assertIn('aria-label', content)
        self.assertIn('tabindex', content)
        self.assertIn('pulse-gold', content)
        self.assertIn('pulse-pink', content)

    def test_google_adapter_has_marker_lifecycle_methods(self):
        """Verify MapGoogleAdapter implements places and point layer marker management."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('_placesMarkers', content)
        self.assertIn('_pointLayersMarkers', content)
        self.assertIn('_infoWindow', content)
        self.assertIn('renderPlacesMarkers', content)
        self.assertIn('handlePlaceMarkerClick', content)
        self.assertIn('filterPlacesMarkers', content)
        self.assertIn('selectPlaceById', content)
        self.assertIn('addPointMarkerLayer', content)
        self.assertIn('handlePointMarkerClick', content)

    def test_explore_template_google_mode_wires_all_place_markers_and_filters(self):
        """Verify /explore template in Google mode binds renderPlacesMarkers and UI event handlers."""
        response = self.client.get('/explore')
        html = response.data.decode('utf-8')

        self.assertIn('renderPlacesMarkers', html)
        self.assertIn('filterPlacesMarkers', html)
        self.assertIn('selectPlace', html)
        self.assertIn('applyFilters', html)
        self.assertIn('resetAllFilters', html)
        self.assertIn('libraries=marker', html)

    def test_map_google_layers_js_exists_and_loaded(self):
        """Verify map-google-layers.js exists on disk and is included in Google mode."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-layers.js')
        self.assertTrue(os.path.exists(path), f"map-google-layers.js not found at {path}")

        response = self.client.get('/explore')
        html = response.data.decode('utf-8')
        self.assertIn('map-google-layers.js', html)

    def test_hy_google_geo_layer_manager_exports_and_methods(self):
        """Verify HYGoogleGeoLayerManager is defined and contains core layer lifecycle methods."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-layers.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('root.HYGoogleGeoLayerManager = GoogleGeoLayerManager', content)
        self.assertIn('fetchGeoJson', content)
        self.assertIn('loadLayer', content)
        self.assertIn('toggleLayer', content)
        self.assertIn('setLayerOpacity', content)
        self.assertIn('_applyZoomGating', content)
        self.assertIn('buildFeaturePopupHTML', content)
        self.assertIn('destroy', content)

    def test_google_geo_layer_manager_six_g3_layers_supported(self):
        """Verify all 6 Phase G3 vector layers are defined in LAYER_STYLES."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-layers.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        for layer_id in ['state_boundary', 'district_boundaries', 'block_boundaries',
                         'rivers', 'lakes_dams', 'forests']:
            self.assertIn(layer_id, content, f"Missing G3 layer definition: {layer_id}")

    def test_block_boundaries_google_min_zoom_10_gating(self):
        """Verify block_boundaries layer enforces minZoom: 10 in Google Geo Layer Manager."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-layers.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('minZoom: 10', content)
        self.assertIn('_applyZoomGating', content)

    def test_waterfalls_not_duplicated_into_g3(self):
        """Verify waterfalls are NOT re-rendered as polygon layers in map-google-layers.js."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-layers.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Waterfalls must be exclusively in G2 marker system
        self.assertNotIn('waterfalls_geo:', content)
        self.assertNotIn('waterfalls:', content)

    def test_google_geo_layer_popups_privacy_safe(self):
        """Verify popup builders in map-google-layers.js are XSS-escaped and privacy-safe."""
        path = os.path.join(self.base_dir, 'static', 'js', 'map', 'map-google-layers.js')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('escHtml', content)
        self.assertIn('_buildDistrictPopup', content)
        self.assertIn('_buildBlockPopup', content)
        self.assertIn('_buildRiverPopup', content)
        self.assertIn('_buildLakeDamPopup', content)
        self.assertIn('_buildForestPopup', content)

        for pk in ['host_phone', 'host_email', 'emergency_contact', 'aadhar_no', 'owner_private_phone']:
            self.assertNotIn(pk, content)


if __name__ == '__main__':
    unittest.main()
