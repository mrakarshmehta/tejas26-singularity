import sys, os, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from config import GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_MAP_ID, MAP_ENGINE, DB_HOST, DB_NAME
from models.database import get_cursor, get_place_by_slug, get_nearby_places
import requests

BASE = "http://127.0.0.1:5000"
session = requests.Session()

print("=" * 70)
print("FINAL DEMO ENVIRONMENT & SIH FLOW AUDIT")
print("=" * 70)

flow_results = {}

# Step 1: HOME
r_home = session.get(f"{BASE}/", timeout=5)
flow_results['1. HOME'] = r_home.status_code == 200 and 'hero-search' in r_home.text
print(f"1. HOME (GET /) -> HTTP {r_home.status_code} | PASS: {flow_results['1. HOME']}")

# Step 2: SEARCH
r_search = session.get(f"{BASE}/api/itinerary/search?q=Rajgir", timeout=5)
places_found = r_search.json() if r_search.status_code == 200 else []
rajgir = next((p for p in places_found if 'rajgir' in p['slug'].lower() or 'rajgir' in p['name'].lower()), None)
flow_results['2. SEARCH'] = r_search.status_code == 200 and rajgir is not None
print(f"2. SEARCH (/api/itinerary/search?q=Rajgir) -> {len(places_found)} results | Found: {rajgir['name'] if rajgir else 'None'} | PASS: {flow_results['2. SEARCH']}")

# Step 3: PLACE DETAIL
r_place = session.get(f"{BASE}/place/rajgir-rajagriha", timeout=5)
has_view_map_cta = '/explore?place_id=' in r_place.text
has_plan_cta = '/itinerary?place_id=' in r_place.text
has_directions = 'google.com/maps' in r_place.text
flow_results['3. PLACE DETAIL'] = r_place.status_code == 200 and has_view_map_cta and has_plan_cta
print(f"3. PLACE DETAIL (/place/rajgir-rajagriha) -> HTTP {r_place.status_code} | CTAs: View on Map={has_view_map_cta}, Plan Trip={has_plan_cta} | PASS: {flow_results['3. PLACE DETAIL']}")

# Step 4: VIEW ON MAP & MAP ENGINE
r_map = session.get(f"{BASE}/explore?place_id=9", timeout=5)
has_gmaps_script = 'maps.googleapis.com' in r_map.text
has_map_id = (GOOGLE_MAPS_MAP_ID in r_map.text) if GOOGLE_MAPS_MAP_ID else False
has_url_param_handler = 'qPlaceId' in r_map.text or 'urlParams.get' in r_map.text
flow_results['4. VIEW ON MAP'] = r_map.status_code == 200 and has_gmaps_script and has_url_param_handler
print(f"4. VIEW ON MAP (/explore?place_id=9) -> HTTP {r_map.status_code} | Google Maps={has_gmaps_script}, Map ID={has_map_id}, Auto-select handler={has_url_param_handler} | PASS: {flow_results['4. VIEW ON MAP']}")

# Step 5: DISTANCE & SMART NEARBY
r_nearby = session.get(f"{BASE}/api/smart-nearby?lat=25.01&lng=85.42&radius=50", timeout=5)
nearby_data = r_nearby.json() if r_nearby.status_code == 200 else []
flow_results['5. DISTANCE & SMART NEARBY'] = r_nearby.status_code == 200 and len(nearby_data) > 0
print(f"5. DISTANCE & SMART NEARBY (/api/smart-nearby) -> HTTP {r_nearby.status_code} | {len(nearby_data)} nearby spots with distance | PASS: {flow_results['5. DISTANCE & SMART NEARBY']}")

# Step 6: PLAN TRIP & URL PREFILL
r_itin = session.get(f"{BASE}/itinerary?place_id=9", timeout=5)
has_prefill_script = 'initFromUrlParams' in r_itin.text or 'params.get(\'place_id\')' in r_itin.text
has_budget_input = 'trip-budget-amount' in r_itin.text or 'budget' in r_itin.text
has_days_input = 'trip-days' in r_itin.text
flow_results['6. PLAN TRIP FORM'] = r_itin.status_code == 200 and has_prefill_script and has_days_input
print(f"6. PLAN TRIP FORM (/itinerary?place_id=9) -> HTTP {r_itin.status_code} | Prefill handler={has_prefill_script}, Days/Budget inputs={has_days_input} | PASS: {flow_results['6. PLAN TRIP FORM']}")

# Step 7: PRINT / PDF EXPORT
has_print_script = 'window.print()' in r_itin.text
has_export_btn = 'Export PDF' in r_itin.text or 'btn-print' in r_itin.text
flow_results['7. PRINT / PDF EXPORT'] = has_print_script and has_export_btn
print(f"7. PRINT / PDF EXPORT -> window.print()={has_print_script}, Export Button={has_export_btn} | PASS: {flow_results['7. PRINT / PDF EXPORT']}")

# System Health Summary
print("\n" + "=" * 70)
print("SYSTEM & CREDENTIALS CHECK")
print("=" * 70)
has_key = bool(GOOGLE_MAPS_API_KEY and len(GOOGLE_MAPS_API_KEY) > 10)
print(f"  Google Maps API Key: {'PASS' if has_key else 'FAIL'} (length={len(GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY else 0})")
print(f"  Google Maps Map ID:  {'PASS' if GOOGLE_MAPS_MAP_ID else 'FAIL'} ({GOOGLE_MAPS_MAP_ID})")
print(f"  Map Engine:          {MAP_ENGINE}")

with get_cursor() as cur:
    cur.execute("SELECT COUNT(*) AS total_places FROM places WHERE deleted_at IS NULL")
    places_count = cur.fetchone()['total_places']
    cur.execute("SELECT COUNT(*) AS total_districts FROM districts WHERE state_id = 1")
    districts_count = cur.fetchone()['total_districts']

db_pass = places_count == 64 and districts_count == 38
print(f"  Database Status:     {'PASS' if db_pass else 'FAIL'} ({places_count} places, {districts_count} districts)")

all_flow_pass = all(flow_results.values())
print(f"\nDemo Flow Overall:     {'PASS' if all_flow_pass else 'FAIL'}")
print("=" * 70)
