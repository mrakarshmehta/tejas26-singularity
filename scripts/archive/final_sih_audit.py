"""FINAL SIH SUBMISSION AUDIT — Automated Phase"""
import sys, io, re, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://127.0.0.1:5000"
s = requests.Session()
issues_blocking = []
issues_nonblocking = []

def check(name, url, checks=None, expect=200):
    """Test a page and run content checks."""
    try:
        r = s.get(f"{BASE}{url}", timeout=15)
        ok = r.status_code == expect
        if not ok:
            issues_blocking.append(f"{name}: HTTP {r.status_code} (expected {expect})")
            print(f"  ✗ {name} — HTTP {r.status_code}")
            return None
        
        text = r.text
        # Check for broken images (src="" or src with no value)
        broken_img = len(re.findall(r'<img[^>]+src\s*=\s*["\'][\s]*["\']', text))
        if broken_img:
            issues_nonblocking.append(f"{name}: {broken_img} empty image src attrs")
        
        # Check for placeholder text
        placeholders = []
        for ph in ['Lorem ipsum', 'TODO', 'FIXME', 'placeholder', 'sample text', 'test data']:
            if ph.lower() in text.lower():
                placeholders.append(ph)
        if placeholders:
            issues_nonblocking.append(f"{name}: placeholder text found: {placeholders}")
        
        # Check for visible Python/Jinja errors
        if 'Traceback' in text or 'TemplateSyntaxError' in text or 'Internal Server Error' in text:
            issues_blocking.append(f"{name}: Server error visible in page content")
        
        # Check for ???  
        q_marks = text.count('???')
        if q_marks > 0:
            issues_nonblocking.append(f"{name}: Found {q_marks} '???' occurrences (possible data gap)")
        
        # Custom checks
        if checks:
            for desc, pattern in checks:
                if not re.search(pattern, text, re.IGNORECASE):
                    issues_nonblocking.append(f"{name}: Missing expected content — {desc}")
        
        print(f"  ✓ {name} — {r.status_code} ({len(text)} bytes)")
        return text
    except Exception as e:
        issues_blocking.append(f"{name}: Connection error — {e}")
        print(f"  ✗ {name} — ERROR: {e}")
        return None

print("=" * 70)
print("FINAL SIH SUBMISSION AUDIT — PRODUCT VERIFICATION")
print("=" * 70)

# 1. Homepage
print("\n--- 1. HOMEPAGE ---")
hp = check("Homepage", "/", [
    ("Search bar", r'<input.*search|hero-search'),
    ("Navigation", r'nav-link|nav-links'),
    ("District section", r'district|Districts'),
    ("Footer", r'footer'),
])

# 2. Explore Map  
print("\n--- 2. EXPLORE MAP ---")
em = check("Explore Map", "/explore", [
    ("Google Maps script", r'maps\.googleapis|google.*map'),
    ("Search input", r'map-search|search'),
    ("Category filters", r'filter-chip|category'),
    ("Layer Manager", r'layer-manager|terrain|satellite'),
])

# 3. Search
print("\n--- 3. SEARCH ---")
check("Search Page", "/search?q=Golghar", [
    ("Search results", r'search-result|place|Golghar'),
])
# API search
r = s.get(f"{BASE}/api/itinerary/search?q=temple", timeout=10)
temple_results = r.json() if r.status_code == 200 else []
print(f"  API search 'temple': {len(temple_results)} results — {'✓' if len(temple_results) > 0 else '✗'}")

# 4. Districts  
print("\n--- 4. DISTRICTS ---")
check("State Bihar", "/state/bihar", [
    ("District links", r'district|block'),
])

# 5. Place Detail
print("\n--- 5. PLACE DETAIL ---")
slugs = ['golghar', 'barabar-caves-gaya', 'nalanda-university-ruins', 
         'rajgir-rajagriha', 'vishnupad-temple-gaya', 'simultala-hill-station-jamui']
for slug in slugs:
    check(f"Place: {slug}", f"/place/{slug}", [
        ("Hero image", r'place-hero|hero-image|background-image'),
        ("Description", r'place-desc|description|about'),
        ("Plan Trip CTA", r'Plan Trip|itinerary'),
        ("View on Map CTA", r'View on Map|explore\?place_id'),
    ])

# 6. Smart Nearby
print("\n--- 6. SMART NEARBY ---")
r = s.get(f"{BASE}/api/smart-nearby?lat=25.6&lng=85.1&radius=50", timeout=15)
if r.status_code == 200:
    sn = r.json()
    count = len(sn.get('results', sn)) if isinstance(sn, dict) else len(sn)
    print(f"  ✓ Smart Nearby API — {count} results")
else:
    issues_blocking.append(f"Smart Nearby API: HTTP {r.status_code}")
    print(f"  ✗ Smart Nearby API — {r.status_code}")

# 7. Near Me (requires geolocation — verify code exists)
print("\n--- 7. NEAR ME ---")
if em:
    has_nearme = bool(re.search(r'near.me|nearMe|geolocation|getCurrentPosition', em, re.IGNORECASE))
    print(f"  {'✓' if has_nearme else '✗'} Near Me code present in explore map")
    if not has_nearme:
        issues_nonblocking.append("Near Me: Geolocation code not found in explore map")

# 8. Trip Planner
print("\n--- 8. TRIP PLANNER ---")
check("Trip Planner", "/itinerary", [
    ("Destination input", r'destination|search|place'),
    ("Days input", r'trip-days|duration|days'),
    ("Budget input", r'budget'),
    ("Companion selector", r'companion|travel-mode|solo|couple|family'),
    ("Generate button", r'Generate|Plan|Create'),
])

# 9. Itinerary Generation (API test with data)
print("\n--- 9. ITINERARY GENERATION ---")
# Can't POST without CSRF, but verify the form and script exist
if em:
    pass  # Already checked in Trip Planner
r = s.get(f"{BASE}/api/itinerary/search?q=", timeout=10)
all_places = r.json() if r.status_code == 200 else []
print(f"  All searchable places: {len(all_places)}")
if len(all_places) < 10:
    issues_nonblocking.append(f"Only {len(all_places)} places searchable for itinerary")

# 10. Budget
print("\n--- 10. BUDGET ---")
check("Budget Planner", "/budget-planner", [
    ("Budget calculator", r'budget|cost|expense'),
])

# 11. Print/PDF  
print("\n--- 11. PRINT/PDF EXPORT ---")
# Check itinerary page for window.print()
itin = check("Itinerary (print check)", "/itinerary")
if itin:
    has_print = 'window.print()' in itin
    has_print_btn = 'Export PDF' in itin or 'btn-print' in itin
    print(f"  window.print(): {'✓' if has_print else '✗'}")
    print(f"  Export PDF button: {'✓' if has_print_btn else '✗'}")
    if not has_print:
        issues_nonblocking.append("Print/PDF: window.print() not found in itinerary page")

# 12. Stays Pagination
print("\n--- 12. STAYS PAGINATION ---")
for p in [1, 2, 3]:
    check(f"Stays Page {p}", f"/stays?page={p}")

# 13. Food & Culture
print("\n--- 13. FOOD & CULTURE ---")
check("Food & Culture", "/food-culture", [
    ("Food content", r'food|cuisine|dish'),
])

# 14. Safety
print("\n--- 14. SAFETY ---")
check("Safety Hub", "/safety", [
    ("Emergency numbers", r'emergency|helpline|police|ambulance|100|112'),
    ("Print button", r'window\.print|print'),
])

# 15. Mobile Responsiveness (code check)
print("\n--- 15. MOBILE RESPONSIVENESS ---")
r = s.get(f"{BASE}/static/css/main.css", timeout=10)
if r.status_code == 200:
    media_queries = len(re.findall(r'@media', r.text))
    has_mobile_nav = 'mobile-bottom-nav' in r.text
    has_hamburger = 'nav-mobile-toggle' in r.text
    print(f"  Media queries in main.css: {media_queries}")
    print(f"  Mobile bottom nav: {'✓' if has_mobile_nav else '✗'}")
    print(f"  Hamburger menu: {'✓' if has_hamburger else '✗'}")

# === DATA VERIFICATION ===
print("\n" + "=" * 70)
print("DATA VERIFICATION")
print("=" * 70)

r = s.get(f"{BASE}/api/itinerary/search?q=", timeout=10)
all_places = r.json() if r.status_code == 200 else []

# Count from explore page for full data
r2 = s.get(f"{BASE}/explore", timeout=10)
explore_text = r2.text if r2.status_code == 200 else ''
# Extract placesData JSON
places_match = re.search(r'const placesData\s*=\s*(\[.*?\]);', explore_text, re.DOTALL)
if places_match:
    try:
        explore_places = json.loads(places_match.group(1))
        total_places = len(explore_places)
        districts_set = set(p.get('district_name', '') for p in explore_places)
        categories_set = set(p.get('category', '') for p in explore_places)
        hidden_gems = sum(1 for p in explore_places if p.get('is_hidden_gem'))
        
        places_with_images = sum(1 for p in explore_places if p.get('image_url'))
        places_with_coords = sum(1 for p in explore_places if p.get('latitude') and p.get('longitude'))
        
        print(f"  Total places on map: {total_places}")
        print(f"  Districts covered: {len(districts_set)} — {sorted(districts_set)}")
        print(f"  Categories: {len(categories_set)} — {sorted(categories_set)}")
        print(f"  Hidden gems: {hidden_gems}")
        print(f"  Places with images: {places_with_images}/{total_places}")
        print(f"  Places with coordinates: {places_with_coords}/{total_places}")
        
        # Validate against claimed data
        if total_places < 60:
            issues_nonblocking.append(f"Claimed 64 places but map shows {total_places}")
        if hidden_gems < 10:
            issues_nonblocking.append(f"Claimed 14 hidden gems but found {hidden_gems}")
    except:
        print("  ✗ Could not parse placesData from explore page")
else:
    print("  ✗ placesData not found in explore page")
    # Fallback to search API count
    print(f"  Search API places: {len(all_places)}")

# === SUMMARY ===
print("\n" + "=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)
print(f"\nBLOCKING ISSUES ({len(issues_blocking)}):")
if issues_blocking:
    for i in issues_blocking:
        print(f"  🚫 {i}")
else:
    print("  None")

print(f"\nNON-BLOCKING ISSUES ({len(issues_nonblocking)}):")
if issues_nonblocking:
    for i in issues_nonblocking:
        print(f"  ⚠️  {i}")
else:
    print("  None")

print(f"\nVERDICT: {'GO' if len(issues_blocking) == 0 else 'NOT GO'}")
