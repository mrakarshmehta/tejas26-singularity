import sys, os, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
import requests

BASE = "http://127.0.0.1:5000"
session = requests.Session()

print("=" * 70)
print("PLACE DETAIL MAP VERIFICATION")
print("=" * 70)

# 1. Place Detail: Golghar
r_gol = session.get(f"{BASE}/place/golghar", timeout=5)
print(f"\n1. GET /place/golghar -> HTTP {r_gol.status_code}")
assert r_gol.status_code == 200

has_gmaps = 'maps.googleapis.com' in r_gol.text
has_carto = 'cartocdn.com' in r_gol.text
has_map_div = 'id="place-map"' in r_gol.text
has_map_id = 'data-map-id=' in r_gol.text
has_callback = '_hyInitPlaceDetailMap' in r_gol.text

print(f"  Google Maps Script Loaded: {'✓ YES' if has_gmaps else '✗ NO'}")
print(f"  Google Maps Callback:      {'✓ YES' if has_callback else '✗ NO'}")
print(f"  Map ID Attribute:          {'✓ YES' if has_map_id else '✗ NO'}")
print(f"  CARTO Watermark Script/URL:{'✗ STILL PRESENT' if has_carto else '✓ ZERO CARTO (GONE)'}")

# 2. Place Detail: Rajgir
r_raj = session.get(f"{BASE}/place/rajgir-rajagriha", timeout=5)
print(f"\n2. GET /place/rajgir-rajagriha -> HTTP {r_raj.status_code}")
assert r_raj.status_code == 200
has_gmaps_raj = 'maps.googleapis.com' in r_raj.text
has_carto_raj = 'cartocdn.com' in r_raj.text
print(f"  Google Maps Script Loaded: {'✓ YES' if has_gmaps_raj else '✗ NO'}")
print(f"  CARTO Watermark Script/URL:{'✗ STILL PRESENT' if has_carto_raj else '✓ ZERO CARTO (GONE)'}")

# 3. Explore Map Regression Check
r_exp = session.get(f"{BASE}/explore", timeout=5)
print(f"\n3. GET /explore -> HTTP {r_exp.status_code}")
assert r_exp.status_code == 200
has_exp_gmaps = 'maps.googleapis.com' in r_exp.text
print(f"  Explore Map Google Script: {'✓ YES' if has_exp_gmaps else '✗ NO'}")

# 4. Check for any remaining cartocdn references across all static js
broken_carto_files = []
for root, _, files in os.walk('static'):
    for file in files:
        if file.endswith('.js'):
            p = os.path.join(root, file)
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'basemaps.cartocdn.com' in content:
                    # Ignore layer-manager layer definitions (static/js/map/map-layers.js) which are part of frozen map layer registry
                    if 'static\\js\\map' not in p and 'static/js/map' not in p:
                        broken_carto_files.append(p)

print(f"\n4. Active CARTO usages in general widgets: {len(broken_carto_files)} -> {broken_carto_files}")

print("\n" + "=" * 70)
print("PLACE DETAIL MAP VERIFICATION COMPLETE")
print("=" * 70)
