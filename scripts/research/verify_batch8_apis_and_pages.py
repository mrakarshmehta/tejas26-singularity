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
    print("=" * 80)
    print("LIVE API, SEARCH, AND PAGE VERIFICATION FOR BATCH 8")
    print("=" * 80)

    # 1. Discovery Snapshot
    print("\n1. Testing GET /api/discovery-snapshot:")
    status, data = fetch_json("/api/discovery-snapshot")
    assert status == 200
    p = data['platform']
    print(f"   verified_places: {p['verified_places']} (Expected: 148)")
    print(f"   geo_mapped_places: {p['geo_mapped_places']} (Expected: 148)")
    print(f"   districts_covered: {p['districts_covered']} (Expected: 38)")
    assert p['verified_places'] == 148, f"Expected 148 verified_places, got {p['verified_places']}"
    assert p['geo_mapped_places'] == 148, f"Expected 148 geo_mapped_places, got {p['geo_mapped_places']}"
    assert p['districts_covered'] == 38, f"Expected 38 districts_covered, got {p['districts_covered']}"
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
    print(f"   Total map places: {len(places)} (Expected: 148)")
    assert len(places) == 148, f"Expected 148 places on map, got {len(places)}"
    batch8_ids = {p['id'] for p in places if p['id'] >= 189}
    print(f"   Batch 8 IDs present on map: {sorted(list(batch8_ids))} (Expected 189–198)")
    assert batch8_ids == set(range(189, 199)), f"Batch 8 IDs mismatch: {batch8_ids}"
    print("   [OK] All 10 Batch 8 Destinations Mapped Successfully")

    # 4. Culture Map
    print("\n4. Testing GET /api/culture-map:")
    status, culture_data = fetch_json("/api/culture-map")
    assert status == 200
    print(f"   Culture map status: {culture_data.get('status')}")
    print("   [OK] Culture Map Verified")

    # 5. Instant Search Queries (All requested search queries)
    print("\n5. Testing Instant Search Queries for Batch 8 Keywords:")
    search_terms = [
        ("Ara House", "Ara House"),
        ("Ahilya Sthan", "Ahilya Sthan, Ahiyari"),
        ("Ahiyari", "Ahilya Sthan, Ahiyari"),
        ("Baba Garibnath", "Baba Garibnath Temple"),
        ("Surya Mandir", "Surya Mandir, Kandaha"),
        ("Kandaha", "Surya Mandir, Kandaha"),
        ("Puran Devi", "Mata Puran Devi Temple"),
        ("Brahmeshwar Nath", "Baba Brahmeshwar Nath Temple, Brahmpur"),
        ("Brahmpur", "Baba Brahmeshwar Nath Temple, Brahmpur"),
        ("Gunawa Ji", "Gunawa Ji (Jain Tirth)"),
        ("Jain Tirth", "Gunawa Ji (Jain Tirth)"),
        ("Ambika Sthan", "Ambika Sthan, Aami"),
        ("Aami", "Ambika Sthan, Aami"),
        ("Lakri Dargah", "Lakri Dargah"),
        ("Tileshwar Nath", "Baba Tileshwar Nath Mandir, Sukhpur"),
        ("Sukhpur", "Baba Tileshwar Nath Mandir, Sukhpur")
    ]

    for term, expected_name in search_terms:
        encoded = urllib.parse.quote(term)
        status, res = fetch_json(f"/api/search/instant?q={encoded}")
        assert status == 200
        results = res.get('results', [])
        found = any(expected_name.lower() in r['name'].lower() for r in results)
        top_name = results[0]['name'] if results else 'NONE'
        print(f"   - Query '{term:<22}' -> Found: {found} (Top: '{top_name}')")
        assert found, f"Query '{term}' did not return '{expected_name}'!"
    print("   [OK] All 16 Search Queries Returned Correct Batch 8 Destinations")

    # 6. Smart Nearby
    print("\n6. Testing Smart Nearby Endpoint:")
    status, nearby_res = fetch_json("/api/smart-nearby?lat=25.5539&lng=84.6680&radius=25")
    assert status == 200
    nearby_items = nearby_res.get('results', [])
    print(f"   Nearby to Ara House (25 km): found {len(nearby_items)} attractions")
    assert len(nearby_items) > 0
    print("   [OK] Smart Nearby Verified")

    # 7. Itinerary Search
    print("\n7. Testing Itinerary Search Endpoint:")
    status, itin_res = fetch_json("/api/itinerary/search?district=Bhojpur&days=1")
    if isinstance(itin_res, list):
        print(f"   Itinerary search returned {len(itin_res)} itinerary plans")
    else:
        print(f"   Itinerary search response status: {itin_res.get('status')}")
    print("   [OK] Itinerary Search Endpoint Verified")

    # 8. Verify Place Detail Pages (HTTP 200 & Content check)
    print("\n8. Testing Place Detail Pages (HTTP 200 & DOM Checks):")
    slugs = [
        "ara-house-bhojpur",
        "ahilya-sthan-ahiyari-darbhanga",
        "baba-garibnath-temple-muzaffarpur",
        "surya-mandir-kandaha-saharsa",
        "mata-puran-devi-temple-purnia",
        "baba-brahmeshwar-nath-temple-brahmpur-buxar",
        "gunawa-ji-jain-tirth-nawada",
        "ambika-sthan-aami-saran",
        "lakri-dargah-gopalganj",
        "baba-tileshwar-nath-mandir-sukhpur-supaul"
    ]
    for slug in slugs:
        status, html = fetch_html(f"/place/{slug}")
        assert status == 200, f"Failed for slug {slug}: status {status}"
        assert "<title>" in html
        assert "Nearby Places" in html or "Explore" in html or "About" in html
        print(f"   [OK] /place/{slug:<48} -> 200 OK (Length: {len(html)} bytes)")
    print("   [OK] All 10 Batch 8 Place Detail Pages Verified")

    # 9. Verify District Pages (HTTP 200)
    print("\n9. Testing District Pages for 10 Affected Districts:")
    dist_slugs = [
        "bhojpur",
        "darbhanga",
        "muzaffarpur",
        "saharsa",
        "purnia",
        "buxar",
        "nawada",
        "saran",
        "gopalganj",
        "supaul"
    ]
    for dslug in dist_slugs:
        status, html = fetch_html(f"/state/bihar/{dslug}")
        assert status == 200, f"Failed for district slug {dslug}: status {status}"
        print(f"   [OK] /state/bihar/{dslug:<20} -> 200 OK (Length: {len(html)} bytes)")
    print("   [OK] All 10 Affected District Pages Verified")

    print("\n" + "=" * 80)
    print("LIVE API, SEARCH, AND USER-FACING PAGE REGRESSION PASSED 100%!")
    print("=" * 80)

if __name__ == "__main__":
    main()
