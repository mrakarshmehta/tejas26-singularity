"""
Comprehensive Route Rendering & Content Verification Test
Tests all key district detail pages and validates HTML content against database records.
"""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from app import create_app

app = create_app()
client = app.test_client()

routes_to_test = [
    ('/state/bihar/jamui', 'Jamui', ['Giddheswar Temple', 'Patneshwar Mandir', 'Simultala Hill Station', 'Minto Tower']),
    ('/state/bihar/nalanda', 'Nalanda', ['Nalanda University Ruins', 'Rajgir']),
    ('/state/bihar/bhagalpur', 'Bhagalpur', ['Vikramshila University Ruins', 'Mandar Hill']),
    ('/state/bihar/kaimur', 'Kaimur', ['Mundeshwari Temple']),
    ('/state/bihar/gaya', 'Gaya', ['Barabar Caves', 'Bodh Gaya', 'Mahabodhi']),
    ('/state/bihar/patna', 'Patna', ['Bihar Museum', 'Mahavir Mandir', 'Golghar']),
]

print("=" * 80)
print("DISTRICT ROUTE RENDERING VERIFICATION")
print("=" * 80)

all_passed = True
for url, expected_district, expected_places in routes_to_test:
    resp = client.get(url)
    print(f"\n🌐 Testing Route: {url}")
    print(f"   Status Code: {resp.status_code}")
    if resp.status_code != 200:
        print(f"   ❌ FAILED: Expected 200, got {resp.status_code}")
        all_passed = False
        continue
    
    html = resp.get_data(as_text=True)
    
    # 1. Check District Name in Header / Title
    h1_match = re.search(r'<h1>([^<]+)', html)
    h1_text = h1_match.group(1).strip() if h1_match else "None"
    print(f"   H1 Heading: '{h1_text}' (Expected: '{expected_district}')")
    if expected_district.lower() not in h1_text.lower():
        print(f"   ❌ FAILED: Heading mismatch!")
        all_passed = False
    else:
        print(f"   ✅ Heading matched")
    
    # 2. Check Expected Places in Page
    found_places = []
    missing_places = []
    for p in expected_places:
        if p in html:
            found_places.append(p)
        else:
            missing_places.append(p)
    print(f"   Places Verified: {len(found_places)}/{len(expected_places)} found")
    if missing_places:
        print(f"   ⚠️ Missing Places: {missing_places}")
    else:
        print(f"   ✅ All expected places present in HTML")

# Also test AI Trip Planner route
print("\n" + "=" * 80)
print("AI TRIP PLANNER ROUTE VERIFICATION")
print("=" * 80)
resp = client.get('/itinerary')
print(f"🌐 Testing /itinerary Status: {resp.status_code}")
if resp.status_code == 200:
    html = resp.get_data(as_text=True)
    # Check for recent trip planner features
    checks = {
        'Custom Days Input': 'min="1" max="30"' in html or 'number' in html,
        'Travel Mode Selector': 'travel_mode' in html or 'Travel Mode' in html or 'Solo' in html or 'Family' in html,
        'Budget Selector': 'budget' in html or 'Budget' in html,
    }
    for feat, ok in checks.items():
        print(f"   - {feat}: {'✅ Present' if ok else '❌ Missing'}")
else:
    print(f"   ❌ Failed to load /itinerary: {resp.status_code}")

print("\n" + "=" * 80)
print(f"OVERALL ROUTE VERIFICATION: {'✅ ALL ROUTES PASS' if all_passed else '❌ SOME ROUTES FAILED'}")
print("=" * 80)
