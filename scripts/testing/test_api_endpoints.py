import urllib.request
import json
import re

base_url = "http://127.0.0.1:5000"

def get_json(endpoint):
    url = f"{base_url}{endpoint}"
    req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Test'})
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def get_html(endpoint):
    url = f"{base_url}{endpoint}"
    req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Test'})
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode('utf-8')

print("=== LIVE API VERIFICATION ===")

# 1. /api/discovery-snapshot
status, snap = get_json("/api/discovery-snapshot")
print(f"GET /api/discovery-snapshot -> Status {status}")
plat = snap.get('platform', {})
verified_places = plat.get('verified_places')
geo_mapped_places = plat.get('geo_mapped_places')
districts_covered = plat.get('districts_covered')
print(f"  verified_places: {verified_places} (Expected: 98)")
print(f"  geo_mapped_places: {geo_mapped_places} (Expected: 98)")
print(f"  districts_covered: {districts_covered} (Expected: 38)")
assert verified_places == 98, f"Mismatch: {verified_places}"
assert geo_mapped_places == 98, f"Mismatch: {geo_mapped_places}"
assert districts_covered == 38, f"Mismatch: {districts_covered}"

# 2. /api/search/filters
status, filters = get_json("/api/search/filters")
print(f"\nGET /api/search/filters -> Status {status}")
print(f"  categories count: {len(filters.get('categories', []))}")
print(f"  districts count: {len(filters.get('districts', []))}")
assert len(filters.get('districts', [])) == 38

# 3. /api/search/instant
status, instant = get_json("/api/search/instant?q=Saurath")
print(f"\nGET /api/search/instant?q=Saurath -> Status {status}")
print(f"  results: {len(instant.get('results', []))}")
assert len(instant.get('results', [])) >= 1
print(f"  first match: {instant['results'][0].get('name')} | District: {instant['results'][0].get('district')}")

# 4. /api/culture-map
status, culture = get_json("/api/culture-map")
print(f"\nGET /api/culture-map -> Status {status}")
features = culture.get('features', [])
print(f"  GeoJSON features count: {len(features)}")
assert status == 200

# 5. /api/places/nearby-radius
status, nearby = get_json("/api/places/nearby-radius?lat=26.4125&lng=86.0954&radius=50")
print(f"\nGET /api/places/nearby-radius?lat=26.4125&lng=86.0954&radius=50 -> Status {status}")
print(f"  places within 50km of Saurath: {len(nearby.get('places', []))}")
assert status == 200

# 6. /api/smart-nearby
status, smart = get_json("/api/smart-nearby?lat=26.4125&lng=86.0954")
print(f"\nGET /api/smart-nearby?lat=26.4125&lng=86.0954 -> Status {status}")
print(f"  smart nearby count: {len(smart.get('results', []))}")
assert status == 200

# 7. /explore map place count and Batch 3 presence
status, html = get_html("/explore")
print(f"\nGET /explore -> Status {status}")
# Match places JSON array in HTML
match = re.search(r'const\s+PLACES\s*=\s*(\[.*?\]);', html, re.DOTALL)
if not match:
    match = re.search(r'data-places=[\'"](.*?)[\'"]', html)
if match:
    places_data = json.loads(match.group(1))
    print(f"  Embedded places on Explore map: {len(places_data)} (Expected: 98)")
    b3_map = [p for p in places_data if p.get('id') in range(139, 149)]
    print(f"  Batch 3 places embedded on map: {len(b3_map)} / 10")
    assert len(places_data) == 98
else:
    # Alternative check: count latitude fields in HTML
    lat_count = len(re.findall(r'"latitude"\s*:\s*\d+\.\d+', html))
    print(f"  Count of latitude entries on explore map: {lat_count}")
    assert lat_count == 98

print("\nALL API CHECKS PASSED SUCCESSFULLY!")
