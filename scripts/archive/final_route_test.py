"""Final comprehensive route test — all major pages and APIs."""
import sys, io, requests, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://127.0.0.1:5000"
s = requests.Session()

results = []

def test(name, url, expect=200):
    try:
        r = s.get(f"{BASE}{url}", timeout=15)
        status = "PASS" if r.status_code == expect else "FAIL"
        results.append((name, url, r.status_code, expect, status))
        print(f"  {status}  {r.status_code}  {name}")
    except Exception as e:
        results.append((name, url, "ERR", expect, "FAIL"))
        print(f"  FAIL  ERR  {name} ({e})")

print("=" * 70)
print("FINAL COMPREHENSIVE ROUTE TEST")
print("=" * 70)

# Core pages
test("Homepage", "/")
test("Explore Map", "/explore")
test("Trip Planner", "/itinerary")
test("Food & Culture", "/food-culture")
test("Safety", "/safety")
test("Stays Page 1", "/stays")
test("Stays Page 2", "/stays?page=2")
test("Stays Page 3", "/stays?page=3")
test("Search Page", "/search?q=Golghar")
test("Browse", "/browse")
test("Circuits", "/circuits")
test("Festivals", "/festivals")
test("Crafts", "/crafts")
test("Eco Pledge", "/eco-pledge")
test("Transport", "/transport")
test("Virtual Tours", "/virtual-tours")
test("Gastronomy", "/gastronomy")
test("Wildlife", "/wildlife")
test("Volunteer", "/volunteer")
test("Archaeology", "/archaeology")
test("Numismatics", "/numismatics")
test("Weather", "/weather")
test("Performing Arts", "/performing-arts")
test("Guides", "/guides")
test("Treks", "/treks")
test("Souvenirs", "/souvenirs")
test("Intellectual Heritage", "/intellectual-heritage")
test("Budget Planner", "/budget-planner")
test("Quiz", "/quiz")
test("Offline", "/offline")
test("Community Suggest", "/suggest")

# Place details
test("Place: Golghar", "/place/golghar")
test("Place: Barabar Caves", "/place/barabar-caves-gaya")
test("Place: Nalanda", "/place/nalanda-university-ruins")
test("Place: Rajgir", "/place/rajgir-rajagriha")
test("Place: Vishnupad", "/place/vishnupad-temple-gaya")
test("Place: Mahabodhi Museum", "/place/bodh-gaya-archaeological-museum")

# State/District pages
test("State: Bihar", "/state/bihar")

# APIs
test("API: Itinerary Search", "/api/itinerary/search?q=temple")
test("API: Smart Nearby", "/api/smart-nearby?lat=25.6&lng=85.1&radius=50")
test("API: Nearby", "/api/nearby?lat=25.6&lng=85.1&radius=10")

# API POST: Itinerary generate
print("\n--- API POST Tests ---")
try:
    r = s.post(f"{BASE}/api/itinerary/generate", json={
        "place_ids": [1, 5],
        "days": 2,
        "budget": "medium",
        "companion": "couple"
    }, timeout=15)
    status = "PASS" if r.status_code == 200 else "FAIL"
    results.append(("API: Generate Itinerary", "POST /api/itinerary/generate", r.status_code, 200, status))
    print(f"  {status}  {r.status_code}  Generate Itinerary POST")
except Exception as e:
    results.append(("API: Generate Itinerary", "POST", "ERR", 200, "FAIL"))
    print(f"  FAIL  ERR  Generate Itinerary POST ({e})")

# Static assets
test("SW.js", "/static/sw.js")
test("Manifest", "/static/manifest.json")
test("Main CSS", "/static/css/main.css")
test("App JS", "/static/js/app.js")

# Summary
print("\n" + "=" * 70)
passed = sum(1 for r in results if r[4] == "PASS")
failed = sum(1 for r in results if r[4] == "FAIL")
print(f"TOTAL: {len(results)} tests | PASS: {passed} | FAIL: {failed}")
print("=" * 70)

if failed > 0:
    print("\nFAILED TESTS:")
    for name, url, code, expect, status in results:
        if status == "FAIL":
            print(f"  ✗ {name} ({url}) → {code} (expected {expect})")
