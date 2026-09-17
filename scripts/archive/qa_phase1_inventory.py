"""Phase 1: Database & Route Inventory — gather facts before browser testing."""
import sys, io, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://127.0.0.1:5000"
s = requests.Session()

print("=" * 70)
print("PHASE 1: DATABASE & ROUTE INVENTORY")
print("=" * 70)

# 1. All pages & status codes
routes = [
    "/", "/explore", "/itinerary", "/districts", "/food-culture",
    "/local-stays", "/safety", "/community/suggest",
    "/states", "/about", "/contact",
    "/manifest.json", "/static/sw.js",
]
print("\n--- ROUTE STATUS ---")
for route in routes:
    try:
        r = s.get(f"{BASE}{route}", timeout=10, allow_redirects=False)
        status = r.status_code
        size = len(r.content)
        print(f"  {status}  {route}  ({size} bytes)")
    except Exception as e:
        print(f"  ERR  {route}  ({e})")

# 2. Places data from search API
print("\n--- ALL PLACES (via /api/itinerary/search) ---")
r = s.get(f"{BASE}/api/itinerary/search?q=", timeout=10)
all_places = r.json()
print(f"  Total places returned: {len(all_places)}")

# Group by district
districts = {}
categories = {}
for p in all_places:
    d = p.get('district_name', 'Unknown')
    c = p.get('category', 'unknown')
    districts.setdefault(d, []).append(p['name'])
    categories.setdefault(c, []).append(p['name'])

print(f"\n--- DISTRICTS WITH PLACES ({len(districts)}) ---")
for d in sorted(districts.keys()):
    print(f"  {d}: {len(districts[d])} places")

print(f"\n--- CATEGORIES ({len(categories)}) ---")
for c in sorted(categories.keys()):
    print(f"  {c}: {len(categories[c])} places")

# 3. All place slugs for detail page testing
print(f"\n--- PLACE SLUGS ({len(all_places)}) ---")
for p in all_places:
    print(f"  id={p['id']}  slug={p['slug']}  cat={p['category']}  dist={p.get('district_name','?')}")

# 4. District pages
print("\n--- DISTRICT PAGES ---")
r = s.get(f"{BASE}/districts", timeout=10)
if r.status_code == 200:
    # Count district links
    import re
    district_links = re.findall(r'href="/district/([^"]+)"', r.text)
    print(f"  District links found on /districts: {len(district_links)}")
    for dl in district_links[:5]:
        print(f"    /district/{dl}")
    if len(district_links) > 5:
        print(f"    ... and {len(district_links)-5} more")
else:
    print(f"  /districts returned {r.status_code}")

# 5. State pages
print("\n--- STATE PAGES ---")
r = s.get(f"{BASE}/states", timeout=10)
if r.status_code == 200:
    state_links = re.findall(r'href="/state/([^"]+)"', r.text)
    print(f"  State links found on /states: {len(state_links)}")
    for sl in state_links[:5]:
        print(f"    /state/{sl}")
else:
    print(f"  /states returned {r.status_code}")

# 6. Smart Nearby API
print("\n--- SMART NEARBY API ---")
r = s.get(f"{BASE}/api/smart-nearby?lat=25.6&lng=85.1&radius=50", timeout=10)
print(f"  Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list):
                print(f"  {k}: {len(v)} results")
    elif isinstance(data, list):
        print(f"  Results: {len(data)}")

# 7. Check for hidden gems
print("\n--- HIDDEN GEMS ---")
r = s.get(f"{BASE}/api/itinerary/search?q=", timeout=10)
# We need to check the main places data - try explore page
r2 = s.get(f"{BASE}/explore", timeout=10)
gem_count = r2.text.count('"is_hidden_gem": true') + r2.text.count('"is_hidden_gem":true')
print(f"  Hidden gem flags found in explore page data: {gem_count}")

# 8. Food & stays
print("\n--- FOOD & CULTURE PAGE ---")
r = s.get(f"{BASE}/food-culture", timeout=10)
print(f"  Status: {r.status_code}, Size: {len(r.content)} bytes")

print("\n--- LOCAL STAYS PAGE ---")
r = s.get(f"{BASE}/local-stays", timeout=10)
print(f"  Status: {r.status_code}, Size: {len(r.content)} bytes")

print("\n--- SAFETY PAGE ---")
r = s.get(f"{BASE}/safety", timeout=10)
print(f"  Status: {r.status_code}, Size: {len(r.content)} bytes")

print("\n--- COMMUNITY SUGGEST PAGE ---")
r = s.get(f"{BASE}/community/suggest", timeout=10)
print(f"  Status: {r.status_code}, Size: {len(r.content)} bytes")

print("\n" + "=" * 70)
print("PHASE 1 COMPLETE")
print("=" * 70)
