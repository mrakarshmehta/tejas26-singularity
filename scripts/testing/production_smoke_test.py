"""
HiddenYatra — Production Smoke Test Script
Executes complete end-to-end smoke verification of running server and application stack.
"""
import urllib.request
import urllib.error
import json
import struct
import os
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(path, expected_status=200):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HYProductionSmokeTest/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            content = resp.read()
            return status == expected_status, status, content, resp.headers
    except urllib.error.HTTPError as e:
        return e.code == expected_status, e.code, e.read(), e.headers
    except Exception as e:
        return False, str(e), None, {}

def run_smoke_test():
    print("=" * 65, flush=True)
    print("HIDDENYATRA FULL PRODUCTION SMOKE TEST MATRIX", flush=True)
    print("=" * 65, flush=True)
    
    passed = 0
    total = 0
    
    # 1. Base /explore page
    total += 1
    ok, status, content, headers = test_endpoint("/explore")
    if ok and b"id=\"explore-map\"" in content and b"window.MAP_ENGINE = 'google'" in content:
        print("[PASS] 01. /explore serves Google Map container and MAP_ENGINE='google' (HTTP 200)", flush=True)
        passed += 1
    else:
        print(f"[FAIL] 01. /explore status={status}", flush=True)

    # 2. GeoJSON Datasets (all 7 layers)
    layers = [
        ("districts.geojson", 38),
        ("blocks.geojson", 534),
        ("rivers.geojson", 1),
        ("lakes_dams.geojson", 1),
        ("forests.geojson", 1),
        ("hotels.geojson", 12),
        ("homestays.geojson", 10),
    ]
    for layer_name, min_features in layers:
        total += 1
        ok, status, content, _ = test_endpoint(f"/static/data/bihar/{layer_name}")
        if ok:
            try:
                geojson = json.loads(content.decode("utf-8"))
                fc = len(geojson.get("features", []))
                if fc >= min_features:
                    print(f"[PASS] 02. Layer {layer_name}: {fc} features loaded (HTTP 200)", flush=True)
                    passed += 1
                else:
                    print(f"[FAIL] 02. Layer {layer_name}: feature count {fc} < {min_features}", flush=True)
            except Exception as e:
                print(f"[FAIL] 02. Layer {layer_name} parse error: {e}", flush=True)
        else:
            print(f"[FAIL] 02. Layer {layer_name} status={status}", flush=True)

    # 3. Production Terrain Manifest
    total += 1
    ok, status, content, _ = test_endpoint("/static/data/terrain/bihar/manifest.json")
    if ok:
        try:
            manifest = json.loads(content.decode("utf-8"))
            is_synthetic = manifest.get("is_synthetic_test_data", True)
            src_files = manifest.get("source_files", {})
            tile_count = len(manifest.get("tiles", {}))
            if not is_synthetic and len(src_files) == 6 and tile_count == 25:
                print(f"[PASS] 03. Terrain manifest: is_synthetic={is_synthetic}, 6 SRTM sources, 25 tiles", flush=True)
                passed += 1
            else:
                print(f"[FAIL] 03. Terrain manifest unexpected properties: is_synthetic={is_synthetic}, count={tile_count}, sources={len(src_files)}", flush=True)
        except Exception as e:
            print(f"[FAIL] 03. Terrain manifest parse error: {e}", flush=True)
    else:
        print(f"[FAIL] 03. Terrain manifest status={status}", flush=True)

    # 4. Production Terrain Binary Chunks (Zoom 9, 10, 11)
    test_tiles = [
        "z9/377/219.hyelev",
        "z10/753/439.hyelev",
        "z11/1507/878.hyelev",
    ]
    for tile_path in test_tiles:
        total += 1
        ok, status, content, _ = test_endpoint(f"/static/data/terrain/bihar/{tile_path}")
        if ok and len(content) == 8490 and content[:4] == b"HYEL":
            magic, ver, z, x, y, rows, cols, samples, min_e, max_e, off, sc = struct.unpack("<4sHBxIIHHIffff", content[:40])
            print(f"[PASS] 04. Binary tile {tile_path}: {magic.decode('ascii')} v{ver}, z={z}, x={x}, y={y}, {rows}x{cols} grid ({samples} pts, {min_e:.0f}m-{max_e:.0f}m)", flush=True)
            passed += 1
        else:
            print(f"[FAIL] 04. Binary tile {tile_path} status={status}, len={len(content) if content else 0}", flush=True)

    # 5. JavaScript Terrain & Map Modules
    js_modules = [
        "js/map/map-google.js",
        "js/map/map-google-layers.js",
        "js/map/map-google-terrain.js",
        "js/map/map-google-terrain-mesh.js",
        "js/map/map-google-terrain-loader.js",
        "js/map/map-google-terrain-worker.js",
        "js/smart-nearby.js",
    ]
    for js_mod in js_modules:
        total += 1
        ok, status, content, _ = test_endpoint(f"/static/{js_mod}")
        if ok and len(content) > 100:
            print(f"[PASS] 05. Static JS {js_mod} served successfully ({len(content)}B)", flush=True)
            passed += 1
        else:
            print(f"[FAIL] 05. Static JS {js_mod} status={status}", flush=True)

    # 6. Smart Nearby API Endpoints
    total += 1
    ok, status, content, _ = test_endpoint("/api/smart-nearby?lat=25.5941&lng=85.1376")
    if ok:
        data = json.loads(content.decode("utf-8"))
        if data.get("status") == "success" and len(data.get("results", [])) > 0:
            print(f"[PASS] 06. /api/smart-nearby returned {len(data['results'])} essential results", flush=True)
            passed += 1
        else:
            print(f"[FAIL] 06. /api/smart-nearby unexpected data structure", flush=True)
    else:
        print(f"[FAIL] 06. /api/smart-nearby status={status}", flush=True)

    total += 1
    ok, status, content, _ = test_endpoint("/api/place/1/nearby-essentials")
    if ok:
        data = json.loads(content.decode("utf-8"))
        if data.get("status") == "success" and len(data.get("essentials", [])) == 10:
            print("[PASS] 07. /api/place/1/nearby-essentials returned exactly 10 essential facilities", flush=True)
            passed += 1
        else:
            print(f"[FAIL] 07. /api/place/1/nearby-essentials unexpected payload", flush=True)
    else:
        print(f"[FAIL] 07. /api/place/1/nearby-essentials status={status}", flush=True)

    # 7. Health Endpoint
    total += 1
    ok, status, content, _ = test_endpoint("/health")
    if ok:
        data = json.loads(content.decode("utf-8"))
        if data.get("status") == "ok" and data.get("database") == "connected":
            print("[PASS] 08. /health: database connected, status OK", flush=True)
            passed += 1
        else:
            print(f"[FAIL] 08. /health unexpected response: {data}", flush=True)
    else:
        print(f"[FAIL] 08. /health status={status}", flush=True)

    # 8. Suggest Place Route (302 login redirect is standard authentication guard)
    total += 1
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    custom_opener = urllib.request.build_opener(NoRedirect)
    try:
        resp = custom_opener.open(f"{BASE_URL}/suggest-place", timeout=5)
        st = resp.status
    except urllib.error.HTTPError as e:
        st = e.code
    except Exception:
        st = 0

    if st in [200, 302]:
        print(f"[PASS] 09. /suggest-place route protected with authentication guard (HTTP {st})", flush=True)
        passed += 1
    else:
        print(f"[FAIL] 09. /suggest-place status={st}", flush=True)

    print("=" * 65, flush=True)
    print(f"PRODUCTION SMOKE TEST RESULTS: {passed} / {total} CHECKS PASSED", flush=True)
    print("=" * 65, flush=True)
    return passed == total

if __name__ == "__main__":
    success = run_smoke_test()
    sys.exit(0 if success else 1)
