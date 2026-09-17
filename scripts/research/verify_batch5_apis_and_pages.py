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
    assert plat.get('verified_places') == 118, f"Expected 118 verified_places, got {plat.get('verified_places')}"
    assert plat.get('geo_mapped_places') == 118, f"Expected 118 geo_mapped_places, got {plat.get('geo_mapped_places')}"
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
    assert len(map_places) == 118, f"Expected 118 map places, got {len(map_places)}"

    # 4. /api/culture-map
    res = requests.get(f"{BASE_URL}/api/culture-map")
    assert res.status_code == 200
    culture_map = res.json()
    print(f"  -> /api/culture-map [OK]")

    # 5. /explore page map embedding
    res = requests.get(f"{BASE_URL}/explore")
    assert res.status_code == 200
    assert "places-data" in res.text
    print("  -> /explore page [OK]")

def test_search_queries():
    print("\n=== 2. INSTANT SEARCH CHECKS ===")
    search_queries = [
        ("Umga", "Umga Sun Temple & Rock Complex"),
        ("Ashokan Pillar", "Ashokan Pillar & Ananda Stupa, Kolhua"),
        ("Punaura", "Punaura Dham"),
        ("Udaipur Wildlife", "Udaipur Wildlife Sanctuary"),
        ("Chandan Dam", "Chandan Dam"),
        ("Baraila", "Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary"),
        ("George Orwell", "George Orwell Birthplace & Memorial"),
        ("Kharagpur Lake", "Kharagpur Lake (Haveli Kharagpur)"),
        ("Sarvodaya Ashram", "Sarvodaya Ashram, Shekhodeora"),
        ("Sujani", "Sujani Embroidery Craft Cluster")
    ]

    for query, expected_title in search_queries:
        res = requests.get(f"{BASE_URL}/api/search/instant?q={query}")
        assert res.status_code == 200, f"Search failed for {query}"
        data = res.json()
        results = data.get('results', [])
        found = any(expected_title.lower() in (r.get('name') or r.get('title') or '').lower() for r in results)
        first_title = (results[0].get('name') or results[0].get('title')) if results else "None"
        print(f"  Search '{query:18}' -> Found: {found} (Top hit: {first_title})")
        assert found, f"Expected to find '{expected_title}' for query '{query}', but results were: {results}"
    print("  -> All 10 instant search queries resolved [OK]")

def test_place_detail_pages():
    print("\n=== 3. PLACE DETAIL PAGES CHECKS ===")
    batch5_slugs = [
        ("umga-sun-temple-and-rock-complex-aurangabad", "Umga Sun Temple & Rock Complex", 24.6312, 84.5518),
        ("ashokan-pillar-and-ananda-stupa-kolhua-vaishali", "Ashokan Pillar & Ananda Stupa, Kolhua", 26.0125, 85.1124),
        ("punaura-dham-sitamarhi", "Punaura Dham", 26.6125, 85.4512),
        ("udaipur-wildlife-sanctuary-west-champaran", "Udaipur Wildlife Sanctuary", 26.8512, 84.4812),
        ("chandan-dam-banka", "Chandan Dam", 24.7812, 86.8125),
        ("baraila-lake-salim-ali-bird-sanctuary-vaishali", "Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary", 25.7512, 85.4512),
        ("george-orwell-birthplace-and-memorial-east-champaran", "George Orwell Birthplace & Memorial", 26.6452, 84.9085),
        ("kharagpur-lake-haveli-kharagpur-munger", "Kharagpur Lake (Haveli Kharagpur)", 25.1215, 86.5124),
        ("sarvodaya-ashram-shekhodeora-nawada", "Sarvodaya Ashram, Shekhodeora", 24.8125, 85.8412),
        ("sujani-embroidery-craft-cluster-muzaffarpur", "Sujani Embroidery Craft Cluster", 26.1512, 85.4812)
    ]

    for slug, expected_title, lat, lng in batch5_slugs:
        url = f"{BASE_URL}/place/{slug}"
        res = requests.get(url)
        assert res.status_code == 200, f"Detail page failed for {url} with code {res.status_code}"
        content = html.unescape(res.text)
        assert expected_title in content, f"Expected title '{expected_title}' not found in {url}"
        assert f"{lat:.4f}" in content or f"{lat:.2f}" in content, f"Latitude {lat} not found in {url}"
        assert f"{lng:.4f}" in content or f"{lng:.2f}" in content, f"Longitude {lng} not found in {url}"
        print(f"  Detail: {expected_title:48} -> HTTP 200 [OK]")
    print("  -> All 10 detail pages verified [OK]")

def test_district_pages():
    print("\n=== 4. AFFECTED DISTRICT PAGES CHECKS ===")
    district_slugs = [
        ("aurangabad", ["Umga Sun Temple & Rock Complex"]),
        ("vaishali", ["Ashokan Pillar & Ananda Stupa, Kolhua", "Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary"]),
        ("sitamarhi", ["Punaura Dham"]),
        ("west-champaran", ["Udaipur Wildlife Sanctuary"]),
        ("banka", ["Chandan Dam"]),
        ("east-champaran", ["George Orwell Birthplace & Memorial"]),
        ("munger", ["Kharagpur Lake (Haveli Kharagpur)"]),
        ("nawada", ["Sarvodaya Ashram, Shekhodeora"]),
        ("muzaffarpur", ["Sujani Embroidery Craft Cluster"])
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
    batch5_test_items = [
        ("Umga Sun Temple & Rock Complex", 24.6312, 84.5518, "Umga"),
        ("Ashokan Pillar & Ananda Stupa, Kolhua", 26.0125, 85.1124, "Kolhua"),
        ("Punaura Dham", 26.6125, 85.4512, "Punaura"),
        ("Udaipur Wildlife Sanctuary", 26.8512, 84.4812, "Udaipur"),
        ("Chandan Dam", 24.7812, 86.8125, "Chandan"),
        ("Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary", 25.7512, 85.4512, "Baraila"),
        ("George Orwell Birthplace & Memorial", 26.6452, 84.9085, "Orwell"),
        ("Kharagpur Lake (Haveli Kharagpur)", 25.1215, 86.5124, "Kharagpur"),
        ("Sarvodaya Ashram, Shekhodeora", 24.8125, 85.8412, "Sarvodaya"),
        ("Sujani Embroidery Craft Cluster", 26.1512, 85.4812, "Sujani")
    ]

    for name, lat, lng, keyword in batch5_test_items:
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
        print(f"  Nearby & Itinerary: {name:48} [OK]")

    print("  -> Smart nearby & Itinerary search verified for all 10 [OK]")

if __name__ == "__main__":
    test_api_checks()
    test_search_queries()
    test_place_detail_pages()
    test_district_pages()
    test_smart_nearby_and_itinerary()
    print("\nALL LIVE API, SEARCH, DETAIL, DISTRICT, AND ITINERARY CHECKS PASSED [OK]!")
