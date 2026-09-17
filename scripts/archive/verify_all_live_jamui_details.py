"""
Reconcile every offline defined change with live Render data.
"""
import json
import urllib.request

# Load live scraped data
with open('scratch/live_district_data.json', 'r', encoding='utf-8') as f:
    live_data = json.load(f)

jamui_live = live_data.get('jamui', {})
live_places = jamui_live.get('places_from_map_attr', [])
live_places_dict = {p['slug']: p for p in live_places}

print(f"Total places returned on live Jamui page: {len(live_places)}")
print("=" * 80)
print(f"{'SLUG':40s} | {'NAME':32s} | {'CATEGORY':12s} | {'COORDS':18s} | {'BLOCK'}")
print("-" * 120)
for p in sorted(live_places, key=lambda x: x['name']):
    coords = f"{p.get('latitude')},{p.get('longitude')}"
    print(f"{p.get('slug'):40s} | {p.get('name'):32s} | {p.get('category'):12s} | {coords:18s} | {p.get('block_name')}")

# Also verify Nearby Essentials API for Jamui
url_nearby = "https://hiddenyatra.onrender.com/api/smart-nearby?lat=24.9198&lng=86.2235"
req = urllib.request.Request(url_nearby, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        nearby_data = json.loads(resp.read().decode('utf-8'))
        print("\n" + "=" * 80)
        print(f"Live Smart Nearby Essentials for Jamui Center (24.9198, 86.2235): {len(nearby_data.get('essentials', []))} items")
        for item in nearby_data.get('essentials', [])[:10]:
            print(f"  - [{item.get('category')}] {item.get('name')} ({item.get('distance_formatted')})")
except Exception as e:
    print("Error fetching smart-nearby:", e)
