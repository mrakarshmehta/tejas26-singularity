"""Verify exact place counts from the database."""
import sys, io, requests, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://127.0.0.1:5000"
s = requests.Session()

# Get explore page and extract places data
r = s.get(f"{BASE}/explore", timeout=15)
text = r.text

# Search for all JSON-like data with lat/lng
# The explore page injects places via Jinja2 - look for the script block
patterns = [
    r'(?:places|allPlaces|markers|allMarkers)\s*=\s*(\[[\s\S]*?\]);',
    r'JSON\.parse\(\'(\[.*?\])\'\)',
    r'const\s+\w+\s*=\s*(\[\{[^;]+\}\])\s*;',
]

for pat in patterns:
    matches = re.findall(pat, text)
    for m in matches:
        try:
            data = json.loads(m)
            if isinstance(data, list) and len(data) > 5:
                print(f"Found data array with {len(data)} items")
                if data[0].get('latitude') or data[0].get('lat'):
                    print(f"  ✓ This is places data")
                    districts = set()
                    categories = set()
                    hidden = 0
                    for p in data:
                        if p.get('district_name'):
                            districts.add(p['district_name'])
                        if p.get('category'):
                            categories.add(p['category'])
                        if p.get('is_hidden_gem'):
                            hidden += 1
                    print(f"  Places: {len(data)}")
                    print(f"  Districts: {len(districts)}")
                    print(f"  Hidden gems: {hidden}")
                    print(f"  Categories: {len(categories)}")
        except:
            pass

# Direct count from page - count latitude occurrences
lat_count = len(re.findall(r'"latitude":\s*[\d.]+', text))
print(f"\nLatitude field count in explore page: {lat_count}")

# Also try the API
r = s.get(f"{BASE}/api/itinerary/search?q=", timeout=10)
api_places = r.json()
print(f"API search (empty query) count: {len(api_places)}")

# Try getting all places from smart-nearby with large radius
r = s.get(f"{BASE}/api/smart-nearby?lat=25.5&lng=85.0&radius=500", timeout=15)
sn = r.json()
if isinstance(sn, dict) and 'results' in sn:
    print(f"Smart Nearby (500km radius) count: {len(sn['results'])}")
elif isinstance(sn, list):
    print(f"Smart Nearby (500km radius) count: {len(sn)}")

# Check total from stats endpoint
r = s.get(f"{BASE}/", timeout=10)
stats_match = re.findall(r'stat-number[^>]*>([^<]+)', r.text)
print(f"\nHomepage stat numbers: {stats_match}")
