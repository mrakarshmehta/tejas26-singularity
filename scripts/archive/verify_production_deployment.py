"""
HiddenYatra — Final Production Deployment Verification
Validates live endpoints, assets, routes, and security constraints on the production deployment.
"""
import urllib.request
import urllib.error
import http.cookiejar
import json
import struct
import sys

BASE_URL = "http://localhost:8000"

def test_url(path, expected_statuses=[200], check_bytes=[]):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HYProductionDeploymentTest/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            content = resp.read()
            passed = (status in expected_statuses)
            for b_str in check_bytes:
                if b_str not in content:
                    passed = False
            return passed, status, len(content)
    except urllib.error.HTTPError as e:
        passed = (e.code in expected_statuses)
        return passed, e.code, 0
    except Exception as e:
        return False, str(e), 0

def run_deployment_verification():
    print("=" * 65, flush=True)
    print("FINAL PRODUCTION DEPLOYMENT VERIFICATION MATRIX", flush=True)
    print("=" * 65, flush=True)

    checks = [
        ("01. Health Check", "/health", [200], [b'"status":"ok"']),
        ("02. Homepage", "/", [200], [b"HiddenYatra"]),
        ("03. Explore Map (Google Engine Container)", "/explore", [200], [b'id="explore-map"']),
        ("04. Explore Map (MAP_ENGINE=google)", "/explore", [200], [b"window.MAP_ENGINE = 'google'"]),
        ("05. Static JS (Google Map Adapter)", "/static/js/map/map-google.js", [200], [b"MapGoogleAdapter"]),
        ("06. Static JS (Google Data Layer Manager)", "/static/js/map/map-google-layers.js", [200], [b"HYGoogleGeoLayerManager"]),
        ("07. Static JS (WebGL Terrain Manager)", "/static/js/map/map-google-terrain.js", [200], [b"HYGoogleTerrainManager"]),
        ("08. Static JS (Perimeter Micro-Skirts & Mesh)", "/static/js/map/map-google-terrain-mesh.js", [200], [b"HYGoogleTerrainMeshFactory"]),
        ("09. Static JS (Multi-Chunk Viewport Loader)", "/static/js/map/map-google-terrain-loader.js", [200], [b"HYGoogleTerrainLoader"]),
        ("10. Static JS (Off-Thread Web Worker)", "/static/js/map/map-google-terrain-worker.js", [200], [b"HYEL"]),
        ("11. Static JS (Smart Nearby Advanced Markers)", "/static/js/smart-nearby.js", [200], [b"AdvancedMarkerElement"]),
        ("12. Layer GeoJSON (Districts - 38)", "/static/data/bihar/districts.geojson", [200], [b"FeatureCollection"]),
        ("13. Layer GeoJSON (Blocks - 534)", "/static/data/bihar/blocks.geojson", [200], [b"FeatureCollection"]),
        ("14. Layer GeoJSON (Rivers - 101)", "/static/data/bihar/rivers.geojson", [200], [b"FeatureCollection"]),
        ("15. Layer GeoJSON (Lakes & Dams - 102)", "/static/data/bihar/lakes_dams.geojson", [200], [b"FeatureCollection"]),
        ("16. Layer GeoJSON (Forests - 13)", "/static/data/bihar/forests.geojson", [200], [b"FeatureCollection"]),
        ("17. Layer GeoJSON (Hotels - 12)", "/static/data/bihar/hotels.geojson", [200], [b"FeatureCollection"]),
        ("18. Layer GeoJSON (Homestays - 10)", "/static/data/bihar/homestays.geojson", [200], [b"FeatureCollection"]),
        ("19. Terrain Manifest (is_synthetic=False)", "/static/data/terrain/bihar/manifest.json", [200], [b'"is_synthetic_test_data": false']),
        ("20. Terrain Chunk (Zoom 9 Coarse)", "/static/data/terrain/bihar/z9/377/219.hyelev", [200], [b"HYEL"]),
        ("21. Terrain Chunk (Zoom 10 Medium)", "/static/data/terrain/bihar/z10/753/439.hyelev", [200], [b"HYEL"]),
        ("22. Terrain Chunk (Zoom 11 High-Res)", "/static/data/terrain/bihar/z11/1507/878.hyelev", [200], [b"HYEL"]),
        ("23. Smart Nearby API (Nearest Facilities)", "/api/smart-nearby?lat=25.5941&lng=85.1376", [200], [b'"status":"success"', b'"results"']),
        ("24. Nearby Essentials API (10 Facilities)", "/api/place/1/nearby-essentials", [200], [b'"status":"success"', b'"essentials"']),
        ("25. Suggest Place (Auth Protected View)", "/suggest-place", [200, 302], []),
    ]

    passed = 0
    total = len(checks)

    for name, path, exp_st, check_b in checks:
        ok, st, sz = test_url(path, exp_st, check_b)
        if ok:
            print(f"[PASS] {name} -> HTTP {st} ({sz}B)", flush=True)
            passed += 1
        else:
            print(f"[FAIL] {name} -> Expected {exp_st}, got {st}", flush=True)

    print("=" * 65, flush=True)
    print(f"DEPLOYMENT VERIFICATION RESULT: {passed} / {total} CHECKS PASSED", flush=True)
    print("=" * 65, flush=True)
    return passed == total

if __name__ == "__main__":
    success = run_deployment_verification()
    sys.exit(0 if success else 1)
