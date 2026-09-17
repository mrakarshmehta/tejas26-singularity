import sys, os, re
sys.path.insert(0, '.')
import requests

BASE = "http://127.0.0.1:5000"

print("=" * 70)
print("VERIFYING DISTRICT IMAGE FALLBACK CHAIN ACROSS PAGES")
print("=" * 70)

session = requests.Session()

# 1. State Page
r = session.get(f"{BASE}/state/bihar", timeout=10)
print(f"\n1. GET /state/bihar -> HTTP {r.status_code} ({len(r.content)} bytes)")
assert r.status_code == 200

# Check for missing uploads/districts/ 404s
dist_upload_refs = re.findall(r'uploads/districts/[^"\')\s]+', r.text)
print(f"   References to uploads/districts/: {len(dist_upload_refs)} (should be 0 because folder is empty)")

# Check background images rendered on district cards
bg_imgs = re.findall(r'background(?:-image)?:\s*url\([\'"]?([^"\'\)]+)[\'"]?\)', r.text)
print(f"   Total background-image urls found: {len(bg_imgs)}")
broken_bgs = []
for bg in bg_imgs:
    if bg.startswith('/static/'):
        local = bg.lstrip('/')
        if not os.path.exists(local):
            broken_bgs.append(bg)
print(f"   Broken local background image paths: {len(broken_bgs)} -> {broken_bgs}")

# Check for Patna, Gaya, Nalanda images in HTML
for dist_name in ['Patna', 'Gaya', 'Nalanda', 'Vaishali', 'Jamui', 'Begusarai', 'Aurangabad']:
    has_dist = dist_name in r.text
    print(f"   District '{dist_name}' present in state page: {has_dist}")

# Check fallback districts (Araria, Arwal)
for dist_name in ['Araria', 'Arwal', 'Banka']:
    has_dist = dist_name in r.text
    print(f"   Fallback District '{dist_name}' present in state page: {has_dist}")

# 2. Homepage
r = session.get(f"{BASE}/", timeout=10)
print(f"\n2. GET / -> HTTP {r.status_code} ({len(r.content)} bytes)")
assert r.status_code == 200
dist_upload_refs_hp = re.findall(r'uploads/districts/[^"\')\s]+', r.text)
print(f"   Homepage references to uploads/districts/: {len(dist_upload_refs_hp)} (should be 0)")

# 3. Individual District Pages
for dist_slug in ['patna', 'gaya', 'nalanda', 'araria']:
    r = session.get(f"{BASE}/state/bihar/{dist_slug}", timeout=10)
    print(f"\n3. GET /state/bihar/{dist_slug} -> HTTP {r.status_code} ({len(r.content)} bytes)")
    assert r.status_code == 200
    dist_upload_refs_dp = re.findall(r'uploads/districts/[^"\')\s]+', r.text)
    print(f"   District page '{dist_slug}' references to uploads/districts/: {len(dist_upload_refs_dp)} (should be 0)")

print("\n" + "=" * 70)
print("TEST COMPLETED")
print("=" * 70)
