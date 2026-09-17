import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor
import requests

BASE = "http://127.0.0.1:5000"
session = requests.Session()

print("=" * 70)
print("COMPREHENSIVE ALL-PLACES & CONTENT AUDIT")
print("=" * 70)

# Fetch all places
with get_cursor() as cur:
    cur.execute("SELECT id, name, slug, district_id FROM places WHERE deleted_at IS NULL ORDER BY district_id, id")
    places = cur.fetchall()

print(f"\n1. AUDITING ALL {len(places)} PLACE DETAIL PAGES:")
place_errors = []
place_qmarks = []
place_broken_imgs = []

for p in places:
    url = f"{BASE}/place/{p['slug']}"
    r = session.get(url, timeout=10)
    if r.status_code != 200:
        place_errors.append((p['id'], p['name'], p['slug'], r.status_code))
        continue
    
    # Check ???
    q_count = r.text.count('???')
    if q_count > 0:
        place_qmarks.append((p['id'], p['name'], p['slug'], q_count))
    
    # Check broken images
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text)
    for img in imgs:
        if img.startswith('/static/'):
            local = img.lstrip('/')
            if not os.path.exists(local) and img != '/static/':
                place_broken_imgs.append((p['slug'], img))

print(f"  Total places checked: {len(places)}")
print(f"  HTTP 200 places: {len(places) - len(place_errors)} / {len(places)}")
if place_errors:
    print(f"  [ERROR] Non-200 places: {place_errors}")
print(f"  Places with '???': {len(place_qmarks)}")
if place_qmarks:
    print(f"  [WARN] Qmark places: {place_qmarks}")
print(f"  Broken place image tags: {len(place_broken_imgs)}")
if place_broken_imgs:
    print(f"  [WARN] Broken images: {place_broken_imgs}")

# Fetch all districts
with get_cursor() as cur:
    cur.execute("SELECT id, name, slug FROM districts WHERE state_id = 1 AND is_visible = 1 ORDER BY sort_order, name")
    districts = cur.fetchall()

print(f"\n2. AUDITING ALL {len(districts)} BIHAR DISTRICT PAGES:")
district_errors = []
district_qmarks = []
district_broken_imgs = []

for d in districts:
    url = f"{BASE}/state/bihar/{d['slug']}"
    r = session.get(url, timeout=10)
    if r.status_code != 200:
        district_errors.append((d['id'], d['name'], d['slug'], r.status_code))
        continue
    
    q_count = r.text.count('???')
    if q_count > 0:
        district_qmarks.append((d['id'], d['name'], d['slug'], q_count))
    
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text)
    for img in imgs:
        if img.startswith('/static/'):
            local = img.lstrip('/')
            if not os.path.exists(local):
                district_broken_imgs.append((d['slug'], img))

print(f"  Total districts checked: {len(districts)}")
print(f"  HTTP 200 districts: {len(districts) - len(district_errors)} / {len(districts)}")
print(f"  Districts with '???': {len(district_qmarks)}")
print(f"  Broken district image tags: {len(district_broken_imgs)}")

print(f"\n3. AUDITING FOOD & CULTURE, STAYS, SAFETY:")
r_food = session.get(f"{BASE}/food-culture", timeout=10)
print(f"  /food-culture -> HTTP {r_food.status_code}, '???' count = {r_food.text.count('???')}")

for page in [1, 2, 3]:
    r_stays = session.get(f"{BASE}/stays?page={page}", timeout=10)
    print(f"  /stays?page={page} -> HTTP {r_stays.status_code}, '???' count = {r_stays.text.count('???')}")

r_safety = session.get(f"{BASE}/safety", timeout=10)
print(f"  /safety -> HTTP {r_safety.status_code}, '???' count = {r_safety.text.count('???')}")

print("\n" + "=" * 70)
print("AUDIT SUMMARY:")
print(f"  Total defects: {len(place_errors) + len(place_qmarks) + len(place_broken_imgs) + len(district_errors) + len(district_qmarks) + len(district_broken_imgs)}")
print("=" * 70)
