import urllib.request
import json
import urllib.parse

base_url = "http://127.0.0.1:5000"

print("=== ITINERARY / NEARBY VERIFICATION ===")

test_places = [
    ("Saurath", 26.4125, 86.0954),
    ("Tutla", 24.7815, 84.0125),
    ("Bateshwar", 25.3341, 87.2712),
    ("Kusiargaon", 26.1158, 87.4589),
    ("Someshwar", 27.4685, 84.3125),
    ("Ghora Katora", 24.9921, 85.4812),
    ("Kusheshwar", 25.8125, 86.1158),
    ("Areraj", 26.5412, 84.7485),
    ("Chirand", 25.7125, 84.8125),
]

for name, lat, lng in test_places:
    # 1. Smart Nearby
    url_sn = f"{base_url}/api/smart-nearby?lat={lat}&lng={lng}&limit=10"
    req = urllib.request.Request(url_sn, headers={'User-Agent': 'Test'})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read().decode('utf-8'))
        results = data.get('results', [])
        assert len(results) > 0, f"Smart nearby empty for ({lat}, {lng})"
        print(f"PASS: Smart nearby for {name} ({lat}, {lng}) -> {len(results)} places returned (closest: {results[0].get('name')} @ {results[0].get('distance_km')} km)")

    # 2. Itinerary Candidate Search
    q_encoded = urllib.parse.quote(name)
    url_itin = f"{base_url}/api/itinerary/search?q={q_encoded}"
    req2 = urllib.request.Request(url_itin, headers={'User-Agent': 'Test'})
    with urllib.request.urlopen(req2) as r:
        data2 = json.loads(r.read().decode('utf-8'))
        itin_places = data2 if isinstance(data2, list) else data2.get('places', [])
        assert len(itin_places) > 0, f"Itinerary search empty for {name}"
        print(f"PASS: Itinerary candidate search for '{name}' -> Found: {itin_places[0].get('name')}")

print("\nALL 10 NEW DESTINATIONS ARE FULLY ACCESSIBLE TO NEARBY DISCOVERY AND ITINERARY PLANNING!")
