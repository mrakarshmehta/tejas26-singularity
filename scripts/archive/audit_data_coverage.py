"""Deep tourism data coverage audit via HTTP API against running Flask app."""
import sys, io, json, re, requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://127.0.0.1:5000"
s = requests.Session()

print("=" * 60)
print("HIDDENYATRA TOURISM DATA COVERAGE AUDIT")
print("=" * 60)

# 1. Get all places from explore map (most reliable source)
r = s.get(f"{BASE}/explore")
match = re.search(r'const ALL_PLACES = (\[.*?\]);', r.text)
if not match:
    print("ERROR: Could not extract ALL_PLACES from explore page")
    sys.exit(1)

places = json.loads(match.group(1))
print(f"\n1. TOTAL ACTIVE PLACES (explore map): {len(places)}")

# 2. District analysis
districts = {}
for p in places:
    d = p.get("district_name", "Unknown")
    if d not in districts:
        districts[d] = {"count": 0, "categories": set(), "gems": 0, "has_image": 0, "has_coords": 0}
    districts[d]["count"] += 1
    districts[d]["categories"].add(p.get("category", "unknown"))
    if p.get("is_hidden_gem"):
        districts[d]["gems"] += 1
    if p.get("cover_image"):
        districts[d]["has_image"] += 1
    if p.get("latitude") and p.get("longitude"):
        districts[d]["has_coords"] += 1

print(f"\n2. DISTRICTS WITH DESTINATIONS: {len(districts)}")
print(f"\n{'District':35s} | Places | Gems | Imgs | Coords | Categories")
print(f"{'-'*35}-+--------+------+------+--------+{'-'*30}")
for d_name in sorted(districts.keys()):
    d = districts[d_name]
    cats_str = ", ".join(sorted(d["categories"]))
    print(f"   {d_name:32s} | {d['count']:6d} | {d['gems']:4d} | {d['has_image']:4d} | {d['has_coords']:6d} | {cats_str}")

# 3. Category breakdown
categories = {}
for p in places:
    c = p.get("category", "unknown")
    if c not in categories:
        categories[c] = {"count": 0, "gems": 0}
    categories[c]["count"] += 1
    if p.get("is_hidden_gem"):
        categories[c]["gems"] += 1

print(f"\n3. CATEGORY BREAKDOWN:")
for c_name in sorted(categories.keys(), key=lambda x: -categories[x]["count"]):
    c = categories[c_name]
    print(f"   {c_name:20s} | {c['count']:3d} places | {c['gems']:2d} gems")

# 4. Hidden gems total
total_gems = sum(1 for p in places if p.get("is_hidden_gem"))
print(f"\n4. TOTAL HIDDEN GEMS: {total_gems}")

# 5. Data quality
with_image = sum(1 for p in places if p.get("cover_image"))
with_coords = sum(1 for p in places if p.get("latitude") and p.get("longitude"))
print(f"\n5. DATA QUALITY:")
print(f"   With cover image:  {with_image}/{len(places)} ({100*with_image//len(places)}%)")
print(f"   With coordinates:  {with_coords}/{len(places)} ({100*with_coords//len(places)}%)")

# 6. Check all 38 Bihar districts
bihar_38_districts = [
    "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur",
    "Bhojpur", "Buxar", "Darbhanga", "East Champaran", "Gaya", "Gopalganj",
    "Jamui", "Jehanabad", "Kaimur", "Katihar", "Khagaria", "Kishanganj",
    "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur",
    "Nalanda", "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa",
    "Samastipur", "Saran", "Sheikhpura", "Sheohar", "Sitamarhi",
    "Siwan", "Supaul", "Vaishali", "West Champaran"
]

db_district_names = set(districts.keys())
# Also check for fuzzy matches (e.g., "Jhanjharpur (Madhubani)" matches "Madhubani")
matched = set()
unmatched_38 = []
for bd in bihar_38_districts:
    found = False
    for dbn in db_district_names:
        if bd.lower() in dbn.lower() or dbn.lower() in bd.lower():
            found = True
            matched.add(bd)
            break
    if not found:
        unmatched_38.append(bd)

print(f"\n6. BIHAR 38-DISTRICT COVERAGE:")
print(f"   Matched: {len(matched)}/38")
print(f"   Missing: {len(unmatched_38)}/38")
if unmatched_38:
    print(f"\n   Missing districts:")
    for d in sorted(unmatched_38):
        print(f"     ✗ {d}")

# 7. Check additional content APIs
print(f"\n7. ADDITIONAL CONTENT APIs:")
apis = [
    ("/api/festivals", "Festivals"),
    ("/api/crafts", "Crafts"),
    ("/api/performing-arts", "Performing Arts"),
    ("/api/archaeology/sites", "Archaeological Sites"),
    ("/api/wildlife/sanctuaries", "Wildlife Sanctuaries"),
    ("/api/treks", "Treks"),
    ("/api/gastronomy/dishes", "Gastronomy Dishes"),
    ("/api/souvenirs", "Souvenirs"),
    ("/api/guides", "Local Guides"),
    ("/api/volunteer/programs", "Volunteer Programs"),
    ("/api/panoramas", "Virtual Panoramas"),
    ("/api/circuits", "Tourism Circuits"),
    ("/api/scholars", "Scholars/Intellectual Heritage"),
]

for path, label in apis:
    try:
        r = s.get(f"{BASE}{path}")
        if r.status_code == 200:
            data = r.json()
            # Try to count items
            count = 0
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                for key in data:
                    val = data[key]
                    if isinstance(val, list):
                        count = max(count, len(val))
            print(f"   {label:30s} | {r.status_code} | ~{count} items")
        else:
            print(f"   {label:30s} | {r.status_code} | error")
    except Exception as e:
        print(f"   {label:30s} | ERROR: {e}")

# 8. Check search index size
r = s.get(f"{BASE}/api/search/instant?q=a")
if r.status_code == 200:
    data = r.json()
    print(f"\n8. SEARCH INDEX:")
    print(f"   Results for 'a': {len(data.get('results', []))}")

# Also check via the /browse page for total count display
r = s.get(f"{BASE}/browse")
count_match = re.search(r'(\d+)\s*(?:destinations|places|results)', r.text)
if count_match:
    print(f"   Browse page count: {count_match.group(0)}")

print("\n" + "=" * 60)
print("AUDIT COMPLETE")
print("=" * 60)
