import sys
import json
import urllib.request
import urllib.parse
sys.path.insert(0, '.')

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:5000"

def fetch_json(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def fetch_html(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.read().decode('utf-8')

def main():
    print("================================================================================")
    print("LIVE API, SEARCH, AND PAGE VERIFICATION FOR BATCH 6")
    print("================================================================================")

    # 1. Discovery Snapshot
    print("\n1. Testing GET /api/discovery-snapshot:")
    status, data = fetch_json("/api/discovery-snapshot")
    assert status == 200
    p = data['platform']
    print(f"   verified_places: {p['verified_places']} (Expected: 128)")
    print(f"   geo_mapped_places: {p['geo_mapped_places']} (Expected: 128)")
    print(f"   districts_covered: {p['districts_covered']} (Expected: 38)")
    assert p['verified_places'] == 128
    assert p['geo_mapped_places'] == 128
    assert p['districts_covered'] == 38
    print("   [OK] Discovery Snapshot Contract Passed")

    # 2. Search Filters
    print("\n2. Testing GET /api/search/filters:")
    status, filters = fetch_json("/api/search/filters")
    assert status == 200
    districts = filters.get('districts', [])
    categories = filters.get('categories', [])
    print(f"   Districts count: {len(districts)} (Expected: 38)")
    print(f"   Categories: {categories}")
    assert len(districts) == 38
    print("   [OK] Search Filters Verified")

    # 3. Places Map
    print("\n3. Testing GET /api/places/map:")
    status, map_data = fetch_json("/api/places/map")
    assert status == 200
    places = map_data if isinstance(map_data, list) else map_data.get('places', [])
    print(f"   Total map places: {len(places)} (Expected: 128)")
    assert len(places) == 128
    batch6_ids = {p['id'] for p in places if p['id'] >= 169}
    print(f"   Batch 6 IDs present on map: {sorted(list(batch6_ids))} (Expected 169–178)")
    assert batch6_ids == set(range(169, 179))
    print("   [OK] All 10 Batch 6 Destinations Mapped Successfully")

    # 4. Culture Map
    print("\n4. Testing GET /api/culture-map:")
    status, culture_data = fetch_json("/api/culture-map")
    assert status == 200
    print(f"   Culture map status: {culture_data.get('status')}")
    print("   [OK] Culture Map Verified")

    # 5. Instant Search Queries
    print("\n5. Testing Instant Search Queries:")
    search_terms = [
        ("Kahalgaon", "Kahalgaon Rock-Cut Temples"),
        ("Rock-Cut Temples", "Kahalgaon Rock-Cut Temples"),
        ("Vishwa Shanti Stupa", "Vishwa Shanti Stupa & Ratnagiri Ropeway"),
        ("Ratnagiri Ropeway", "Vishwa Shanti Stupa & Ratnagiri Ropeway"),
        ("Shringirishi", "Shringirishi Dham"),
        ("Girihinda", "Girihinda Pahar & Shiv Temple"),
        ("Matsyagandha", "Matsyagandha Lake & Raktakali Temple"),
        ("Kajha Kothi", "Kajha Kothi Eco Park"),
        ("Guru Tegh Bahadur", "Guru Tegh Bahadur Historic Gurdwara, Lakshmipur"),
        ("Lakshmipur", "Guru Tegh Bahadur Historic Gurdwara, Lakshmipur"),
        ("Dighwa Dubauli", "Dighwa Dubauli Archaeological Mounds"),
        ("Champanagar", "Champanagar Ancient Capital & Jain Tirth"),
        ("Jain Tirth", "Champanagar Ancient Capital & Jain Tirth"),
        ("Deokund", "Deokund")
    ]

    for term, expected_name in search_terms:
        encoded = urllib.parse.quote(term)
        status, res = fetch_json(f"/api/search/instant?q={encoded}")
        assert status == 200
        results = res.get('results', [])
        found = any(expected_name.lower() in r['name'].lower() for r in results)
        print(f"   - Query '{term:<20}' -> Top Hit: '{results[0]['name'] if results else 'NONE'}' (Found expected: {found})")
        assert found, f"Query '{term}' did not return '{expected_name}'!"
    print("   [OK] All 14 Instant Search Queries Verified")

    # 6. Smart Nearby
    print("\n6. Testing GET /api/smart-nearby:")
    # Test near Kahalgaon (25.2689, 87.2345)
    status, nearby = fetch_json("/api/smart-nearby?lat=25.2689&lng=87.2345")
    assert status == 200
    print(f"   Smart nearby near Kahalgaon returned {len(nearby.get('nearby_places', []))} places")
    print("   [OK] Smart Nearby Verified")

    # 7. Itinerary Search Autocomplete
    print("\n7. Testing GET /api/itinerary/search:")
    status, itin_res = fetch_json("/api/itinerary/search?q=Vishwa+Shanti")
    assert status == 200
    itin_matches = itin_res if isinstance(itin_res, list) else itin_res.get('results', [])
    assert any("Vishwa Shanti" in r['name'] for r in itin_matches)
    print(f"   Itinerary match found: {[r['name'] for r in itin_matches]}")
    print("   [OK] Itinerary Search Verified")

    # 8. Detail Pages Verification
    print("\n8. Testing Detail Pages for All 10 Destinations:")
    slugs = [
        "kahalgaon-rock-cut-temples-bhagalpur",
        "vishwa-shanti-stupa-and-ratnagiri-ropeway-nalanda",
        "shringirishi-dham-lakhisarai",
        "girihinda-pahar-and-shiv-temple-sheikhpura",
        "matsyagandha-lake-and-raktakali-temple-saharsa",
        "kajha-kothi-eco-park-purnia",
        "guru-tegh-bahadur-historic-gurdwara-lakshmipur-katihar",
        "dighwa-dubauli-archaeological-mounds-gopalganj",
        "champanagar-ancient-capital-and-jain-tirth-bhagalpur",
        "deokund-aurangabad"
    ]

    for slug in slugs:
        status, html = fetch_html(f"/place/{slug}")
        print(f"   - /place/{slug:<55} -> HTTP {status} (Length: {len(html)} bytes)")
        assert status == 200
        assert "<html" in html.lower()
    print("   [OK] All 10 Place Detail Pages Loaded Cleanly (HTTP 200)")

    # 9. District Pages Verification
    print("\n9. Testing District Pages for Affected Districts:")
    district_slugs = [
        ("bhagalpur", ["Kahalgaon", "Champanagar"]),
        ("nalanda", ["Vishwa Shanti"]),
        ("lakhisarai", ["Shringirishi"]),
        ("sheikhpura", ["Girihinda"]),
        ("saharsa", ["Matsyagandha"]),
        ("purnia", ["Kajha Kothi"]),
        ("katihar", ["Guru Tegh Bahadur"]),
        ("gopalganj", ["Dighwa Dubauli"]),
        ("aurangabad", ["Deokund"])
    ]

    for d_slug, expected_places in district_slugs:
        status, html = fetch_html(f"/state/bihar/{d_slug}")
        print(f"   - /state/bihar/{d_slug:<15} -> HTTP {status} (Length: {len(html)} bytes)")
        assert status == 200
        for exp in expected_places:
            assert exp.lower() in html.lower(), f"Expected '{exp}' card on /state/bihar/{d_slug}"
    print("   [OK] All 9 District Pages Render New Cards Correctly")

    print("\n================================================================================")
    print("ALL API, SEARCH, AND PAGE CONTRACTS VERIFIED 100% GREEN!")
    print("================================================================================")

if __name__ == "__main__":
    main()
