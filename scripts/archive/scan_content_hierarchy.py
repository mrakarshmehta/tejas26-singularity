import sys, os, re
sys.path.insert(0, '.')
import requests

BASE = "http://127.0.0.1:5000"
session = requests.Session()

print("=" * 70)
print("PHASE 1: DEEP CONTENT HIERARCHY SCAN")
print("=" * 70)

# 1. District Pages
districts_to_test = ['patna', 'gaya', 'nalanda', 'jamui', 'nawada', 'vaishali', 'araria']
for dist in districts_to_test:
    r = session.get(f"{BASE}/state/bihar/{dist}", timeout=10)
    print(f"\n[DISTRICT] /state/bihar/{dist} -> HTTP {r.status_code}")
    if r.status_code != 200:
        print(f"  ERROR: status code {r.status_code}")
        continue
    
    # Check broken image references
    broken_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text)
    invalid_imgs = [img for img in broken_imgs if img.startswith('/static/') and not os.path.exists(img.lstrip('/'))]
    if invalid_imgs:
        print(f"  [WARN] Invalid <img> src: {invalid_imgs}")
    else:
        print(f"  [OK] All {len(broken_imgs)} <img> src paths valid")

    # Check for '???' encoding artifacts
    raw_q = r.text.count('???')
    if raw_q > 0:
        print(f"  [WARN] Found {raw_q} occurrences of '???'")
    else:
        print(f"  [OK] No '???' encoding artifacts")

# 2. Place Detail Pages
places_to_test = [
    'golghar', 
    'takht-sri-patna-sahib', 
    'barabar-caves-gaya', 
    'vishnupad-temple-gaya',
    'nalanda-university-ruins', 
    'rajgir-rajagriha', 
    'giddheswar-temple-jamui',
    'kakolat-waterfall-nawada',
    'vaishali-stupa-democracy',
    'deo-sun-temple-aurangabad'
]
for p_slug in places_to_test:
    r = session.get(f"{BASE}/place/{p_slug}", timeout=10)
    print(f"\n[PLACE DETAIL] /place/{p_slug} -> HTTP {r.status_code}")
    if r.status_code != 200:
        print(f"  ERROR: status code {r.status_code}")
        continue
    
    # Check CTA links
    has_plan_cta = '/itinerary?place_id=' in r.text
    has_map_cta = '/explore?place_id=' in r.text
    has_gmaps_cta = 'google.com/maps' in r.text
    print(f"  CTAs: Plan Trip={has_plan_cta}, View on Map={has_map_cta}, Google Maps/Directions={has_gmaps_cta}")

    # Check broken image references
    broken_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text)
    invalid_imgs = [img for img in broken_imgs if img.startswith('/static/') and not os.path.exists(img.lstrip('/'))]
    # Filter out empty lightbox src="" which gets populated via JS
    invalid_imgs = [img for img in invalid_imgs if img.strip() != '']
    if invalid_imgs:
        print(f"  [WARN] Invalid <img> src: {invalid_imgs}")
    else:
        print(f"  [OK] <img> src paths valid")

    # Check for '???'
    raw_q = r.text.count('???')
    if raw_q > 0:
        print(f"  [WARN] Found {raw_q} occurrences of '???'")

# 3. Food & Culture
r = session.get(f"{BASE}/food-culture", timeout=10)
print(f"\n[FOOD & CULTURE] /food-culture -> HTTP {r.status_code}")
raw_q_food = r.text.count('???')
print(f"  '???' occurrences in food-culture: {raw_q_food}")

# 4. Stays
for page in [1, 2, 3]:
    r = session.get(f"{BASE}/stays?page={page}", timeout=10)
    print(f"\n[STAYS] /stays?page={page} -> HTTP {r.status_code}")

# 5. Safety
r = session.get(f"{BASE}/safety", timeout=10)
print(f"\n[SAFETY] /safety -> HTTP {r.status_code}")

print("\n" + "=" * 70)
print("PHASE 1 SCAN COMPLETE")
print("=" * 70)
