import requests
import html

BASE_URL = "http://127.0.0.1:5000"

def test_api_checks():
    print("=== 1. DISCOVERY & API CHECKS ===")
    
    # 1. /api/discovery-snapshot
    res = requests.get(f"{BASE_URL}/api/discovery-snapshot")
    assert res.status_code == 200, f"/api/discovery-snapshot status {res.status_code}"
    snap = res.json()
    plat = snap.get('platform', {})
    print(f"Snapshot platform: verified_places={plat.get('verified_places')}, geo_mapped_places={plat.get('geo_mapped_places')}, districts_covered={plat.get('districts_covered')}")
    assert plat.get('verified_places') == 108, f"Expected 108 verified_places, got {plat.get('verified_places')}"
    assert plat.get('geo_mapped_places') == 108, f"Expected 108 geo_mapped_places, got {plat.get('geo_mapped_places')}"
    assert plat.get('districts_covered') == 38, f"Expected 38 districts_covered, got {plat.get('districts_covered')}"
    print("  -> /api/discovery-snapshot [OK]")

    # 2. /api/search/filters
    res = requests.get(f"{BASE_URL}/api/search/filters")
    assert res.status_code == 200
    filters = res.json()
    assert 'districts' in filters and len(filters['districts']) == 38
    print(f"  -> /api/search/filters [OK] (Districts: {len(filters['districts'])}, Categories: {len(filters['categories'])})")

    # 3. /api/places/map
    res = requests.get(f"{BASE_URL}/api/places/map")
    assert res.status_code == 200
    map_places = res.json()
    print(f"  -> /api/places/map [OK] (Count: {len(map_places)})")
    assert len(map_places) == 108, f"Expected 108 map places, got {len(map_places)}"

    # 4. /api/culture-map
    res = requests.get(f"{BASE_URL}/api/culture-map")
    assert res.status_code == 200
    culture_map = res.json()
    print(f"  -> /api/culture-map [OK]")

    # 5. /explore page map embedding
    res = requests.get(f"{BASE_URL}/explore")
    assert res.status_code == 200
    print("  -> /explore page [OK]")

def test_search_queries():
    print("\n=== 2. INSTANT SEARCH CHECKS ===")
    search_queries = [
        ("Rampurva", "Rampurva Ashokan Pillars"),
        ("Renu", "Phanishwar Nath Renu Smarak & Birthplace"),
        ("Shergarh", "Shergarh Fort"),
        ("Daud Khan", "Daud Khan Fort"),
        ("Lauriya", "Lauriya Nandangarh"),
        ("Rajnagar Palace", "Rajnagar Palace Complex"),
        ("Kaimur Wildlife", "Kaimur Wildlife Sanctuary & Adhaura Hills"),
        ("Simaria", "Simaria Ghat & Dinkar Memorial"),
        ("Jal Mandir", "Jal Mandir, Pawapuri"),
        ("Gupta Dham", "Gupta Dham (Gupteshwar Mahadev Cave)")
    ]

    for query, expected_title in search_queries:
        res = requests.get(f"{BASE_URL}/api/search/instant?q={query}")
        assert res.status_code == 200, f"Search failed for {query}"
        data = res.json()
        results = data.get('results', [])
        found = any(expected_title.lower() in (r.get('name') or r.get('title') or '').lower() for r in results)
        first_title = (results[0].get('name') or results[0].get('title')) if results else "None"
        print(f"  Search '{query:16}' -> Found: {found} (Top hit: {first_title})")
        assert found, f"Expected to find '{expected_title}' for query '{query}', but results were: {results}"
    print("  -> All 10 instant search queries resolved [OK]")

def test_place_detail_pages():
    print("\n=== 3. PLACE DETAIL PAGES CHECKS ===")
    batch4_slugs = [
        ("rampurva-ashokan-pillars-west-champaran", "Rampurva Ashokan Pillars", 27.2685, 84.5012),
        ("phanishwar-nath-renu-smarak-and-birthplace-araria", "Phanishwar Nath Renu Smarak & Birthplace", 26.2486, 87.2842),
        ("shergarh-fort-rohtas", "Shergarh Fort", 24.8415, 83.7812),
        ("daud-khan-fort-aurangabad", "Daud Khan Fort", 25.0315, 84.4024),
        ("lauriya-nandangarh-west-champaran", "Lauriya Nandangarh", 26.9954, 84.4124),
        ("rajnagar-palace-complex-madhubani", "Rajnagar Palace Complex", 26.3912, 86.1485),
        ("kaimur-wildlife-sanctuary-and-adhaura-hills-kaimur", "Kaimur Wildlife Sanctuary & Adhaura Hills", 24.8125, 83.6125),
        ("simaria-ghat-and-dinkar-memorial-begusarai", "Simaria Ghat & Dinkar Memorial", 25.4382, 85.9921),
        ("jal-mandir-pawapuri-nalanda", "Jal Mandir, Pawapuri", 25.0925, 85.5385),
        ("gupta-dham-gupteshwar-mahadev-cave-rohtas", "Gupta Dham (Gupteshwar Mahadev Cave)", 24.7512, 83.7912)
    ]

    for slug, expected_title, lat, lng in batch4_slugs:
        url = f"{BASE_URL}/place/{slug}"
        res = requests.get(url)
        assert res.status_code == 200, f"Detail page failed for {url} with code {res.status_code}"
        content = html.unescape(res.text)
        assert expected_title in content, f"Expected title '{expected_title}' not found in {url}"
        assert f"{lat:.4f}" in content or f"{lat:.2f}" in content, f"Latitude {lat} not found in {url}"
        assert f"{lng:.4f}" in content or f"{lng:.2f}" in content, f"Longitude {lng} not found in {url}"
        print(f"  Detail: {expected_title:42} -> HTTP 200 [OK]")
    print("  -> All 10 detail pages verified [OK]")

def test_district_pages():
    print("\n=== 4. AFFECTED DISTRICT PAGES CHECKS ===")
    district_slugs = [
        ("west-champaran", ["Rampurva Ashokan Pillars", "Lauriya Nandangarh"]),
        ("araria", ["Phanishwar Nath Renu Smarak & Birthplace"]),
        ("rohtas", ["Shergarh Fort", "Gupta Dham (Gupteshwar Mahadev Cave)"]),
        ("aurangabad", ["Daud Khan Fort"]),
        ("jhanjharpur-madhubani", ["Rajnagar Palace Complex"]),
        ("kaimur", ["Kaimur Wildlife Sanctuary & Adhaura Hills"]),
        ("begusarai", ["Simaria Ghat & Dinkar Memorial"]),
        ("nalanda", ["Jal Mandir, Pawapuri"])
    ]

    for dist_slug, expected_places in district_slugs:
        url = f"{BASE_URL}/state/bihar/{dist_slug}"
        res = requests.get(url)
        assert res.status_code == 200, f"District page failed for {url} with code {res.status_code}"
        content = html.unescape(res.text)
        for place in expected_places:
            assert place in content, f"Place '{place}' not found on district page {url}"
            print(f"  District {dist_slug:22} contains '{place}' [OK]")
    print("  -> All affected district pages verified [OK]")

def test_smart_nearby_and_itinerary():
    print("\n=== 5. SMART NEARBY & ITINERARY CHECKS ===")
    batch4_test_items = [
        ("Rampurva Ashokan Pillars", 27.2685, 84.5012, "Rampurva"),
        ("Phanishwar Nath Renu Smarak & Birthplace", 26.2486, 87.2842, "Renu"),
        ("Shergarh Fort", 24.8415, 83.7812, "Shergarh"),
        ("Daud Khan Fort", 25.0315, 84.4024, "Daud"),
        ("Lauriya Nandangarh", 26.9954, 84.4124, "Lauriya"),
        ("Rajnagar Palace Complex", 26.3912, 86.1485, "Rajnagar"),
        ("Kaimur Wildlife Sanctuary & Adhaura Hills", 24.8125, 83.6125, "Kaimur"),
        ("Simaria Ghat & Dinkar Memorial", 25.4382, 85.9921, "Simaria"),
        ("Jal Mandir, Pawapuri", 25.0925, 85.5385, "Pawapuri"),
        ("Gupta Dham (Gupteshwar Mahadev Cave)", 24.7512, 83.7912, "Gupta Dham")
    ]

    for name, lat, lng, keyword in batch4_test_items:
        # Smart nearby around this location
        res = requests.get(f"{BASE_URL}/api/smart-nearby?lat={lat}&lng={lng}&limit=10")
        assert res.status_code == 200, f"Smart nearby failed for {name}"
        data = res.json()
        assert 'results' in data or 'places' in data or isinstance(data, list)
        
        # Itinerary search for waypoint selection
        res2 = requests.get(f"{BASE_URL}/api/itinerary/search?q={keyword}")
        assert res2.status_code == 200, f"Itinerary search failed for {keyword}"
        itin_results = res2.json()
        assert any(keyword.lower() in p.get('name', '').lower() for p in itin_results), f"Keyword '{keyword}' not found in itinerary results: {itin_results}"
        print(f"  Nearby & Itinerary: {name:42} [OK]")

    print("  -> Smart nearby & Itinerary search verified for all 10 [OK]")

if __name__ == "__main__":
    test_api_checks()
    test_search_queries()
    test_place_detail_pages()
    test_district_pages()
    test_smart_nearby_and_itinerary()
    print("\nALL LIVE API, SEARCH, DETAIL, DISTRICT, AND ITINERARY CHECKS PASSED [OK]!")
