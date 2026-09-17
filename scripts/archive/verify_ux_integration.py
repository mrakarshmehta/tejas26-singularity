"""Comprehensive UX & Route Verification Script for HiddenYatra."""
import sys, io, re, requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = "http://127.0.0.1:5000"
s = requests.Session()

print("=" * 60)
print("HIDDENYATRA FINAL UX INTEGRATION VERIFICATION")
print("=" * 60)

# 1. Explore Map Page
r_explore = s.get(f"{BASE}/explore")
print(f"\n1. Explore Map Page: status {r_explore.status_code}")
assert r_explore.status_code == 200, "Explore map failed"
assert 'Showing <strong id="map-results-count"' in r_explore.text
assert 'across 20 districts' in r_explore.text
assert 'preview-plan-btn' in r_explore.text
assert 'preview-directions-btn' in r_explore.text
assert 'preview-gmaps-btn' in r_explore.text
assert 'preview-save-btn' in r_explore.text
assert 'URLSearchParams' in r_explore.text
print("   [PASS] Explore map contains all required controls, actions, and URL param handler")

# 2. Place Detail Page
r_place = s.get(f"{BASE}/place/golghar")
print(f"\n2. Place Detail Page (Golghar): status {r_place.status_code}")
assert r_place.status_code == 200, "Place detail failed"
assert '🧳 Plan Trip' in r_place.text
assert '🗺️ View on Map' in r_place.text
assert '/itinerary?place_id=' in r_place.text
assert '/explore?place_id=' in r_place.text
assert '🗺️ Explore Map' in r_place.text
assert '🧳 Plan a Trip Here →' in r_place.text
print("   [PASS] Place detail contains Hero actions & Sidebar Map Widget CTA links")

# 3. Itinerary Planner Page
r_itin = s.get(f"{BASE}/itinerary")
print(f"\n3. Itinerary Planner Page: status {r_itin.status_code}")
assert r_itin.status_code == 200, "Itinerary page failed"
assert 'initFromUrlParams' in r_itin.text
assert 'URLSearchParams' in r_itin.text
assert 'renderSelectedPlaceChips' in r_itin.text
print("   [PASS] Itinerary planner contains auto-prefill from URL parameters")

# 4. Itinerary Search API
r_search = s.get(f"{BASE}/api/itinerary/search?q=Mahabodhi")
print(f"\n4. Itinerary Search API: status {r_search.status_code}")
assert r_search.status_code == 200
data = r_search.json()
assert len(data) > 0
print(f"   [PASS] Found destination: {data[0].get('name')} (id: {data[0].get('id')})")

# 5. CSS Styling Verification
r_css = s.get(f"{BASE}/static/css/explore-map.css")
print(f"\n5. Explore Map CSS: status {r_css.status_code}")
assert r_css.status_code == 200
assert '[data-theme="light"] .gm-style .gm-style-iw-c' in r_css.text
assert '.hy-marker-selected' in r_css.text
assert '.map-place-preview' in r_css.text
assert '@media (max-width: 768px)' in r_css.text
print("   [PASS] CSS contains light mode InfoWindow rules, selected marker glow, and mobile bottom sheet")

# 6. Run regression test
print("\n6. Running 25-Point Automated Regression Suite...")
import subprocess
res = subprocess.run(["python", "scratch/test_map_regression.py"], capture_output=True, text=True)
print(res.stdout)
assert "OVERALL STATUS: ALL PASSED" in res.stdout, "Regression test suite had failures"

print("=" * 60)
print("ALL UX VERIFICATION CHECKS PASSED WITH ZERO REGRESSIONS")
print("=" * 60)
