"""
FULL READ-ONLY DATABASE AUDIT — HiddenYatra District Data Integrity
No writes. No deletes. No updates. Pure SELECT queries only.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')

# Load .env BEFORE importing anything that reads config
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

from models.connection import get_db

conn = get_db()
cur = conn.cursor()

# ──────────────────────────────────────────────
# 1. FULL DISTRICTS TABLE DUMP
# ──────────────────────────────────────────────
print("=" * 80)
print("SECTION 1: ALL DISTRICTS (id, name, slug, description, famous_for, cover_image)")
print("=" * 80)
cur.execute("""
    SELECT id, state_id, name, slug, description, famous_for, cover_image, image_url,
           sort_order, is_featured, is_visible
    FROM districts ORDER BY id
""")
districts = cur.fetchall()
for d in districts:
    print(f"  ID={d['id']:3d} | Name={d['name']:20s} | Slug={d['slug']:25s} | "
          f"Featured={d['is_featured']} | Visible={d['is_visible']} | "
          f"CoverImg={str(d.get('cover_image',''))[:60]} | "
          f"ImageURL={str(d.get('image_url',''))[:60]}")

# ──────────────────────────────────────────────
# 2. NAME vs SLUG MISMATCH CHECK
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 2: NAME vs SLUG MISMATCH DETECTION")
print("=" * 80)

def expected_slug(name):
    """Simple slugify to compare."""
    import re
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

mismatch_count = 0
for d in districts:
    exp = expected_slug(d['name'])
    actual = d['slug']
    if exp != actual:
        mismatch_count += 1
        print(f"  ❌ MISMATCH: ID={d['id']:3d} Name='{d['name']}' → Expected slug='{exp}' | Actual slug='{actual}'")
    else:
        print(f"  ✅ OK:       ID={d['id']:3d} Name='{d['name']}' → slug='{actual}'")

print(f"\n  TOTAL MISMATCHES: {mismatch_count} / {len(districts)}")

# ──────────────────────────────────────────────
# 3. ALL PLACES WITH DISTRICT ASSIGNMENT
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 3: ALL PLACES — district_id ASSIGNMENT")
print("=" * 80)
cur.execute("""
    SELECT p.id, p.name, p.slug, p.district_id, p.state_id, p.category,
           p.cover_image, p.description, p.deleted_at,
           d.name AS district_name, d.slug AS district_slug
    FROM places p
    LEFT JOIN districts d ON p.district_id = d.id
    ORDER BY p.district_id, p.id
""")
places = cur.fetchall()
for p in places:
    flag = ""
    if p['district_id'] is None:
        flag = " ⚠️ NULL DISTRICT"
    if not p['name'] or p['name'].strip() == '':
        flag += " ⚠️ EMPTY NAME"
    if p['deleted_at']:
        flag += " 🗑️ SOFT-DELETED"
    print(f"  PlaceID={p['id']:4d} | DistrictID={str(p['district_id']):5s} | "
          f"DistrictName={str(p.get('district_name','')):20s} | "
          f"DistrictSlug={str(p.get('district_slug','')):20s} | "
          f"PlaceName={str(p['name']):40s} | Cat={str(p['category']):15s}{flag}")

# ──────────────────────────────────────────────
# 4. PLACES PER DISTRICT COUNT
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 4: PLACE COUNTS PER DISTRICT")
print("=" * 80)
cur.execute("""
    SELECT d.id, d.name, d.slug, COUNT(p.id) AS place_count
    FROM districts d
    LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
    GROUP BY d.id
    ORDER BY d.id
""")
counts = cur.fetchall()
for c in counts:
    print(f"  ID={c['id']:3d} | Name={c['name']:20s} | Slug={c['slug']:20s} | Places={c['place_count']}")

# ──────────────────────────────────────────────
# 5. BLOCKS TABLE
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 5: ALL BLOCKS")
print("=" * 80)
cur.execute("""
    SELECT b.id, b.name, b.slug, b.district_id, d.name AS district_name, d.slug AS district_slug
    FROM blocks b
    LEFT JOIN districts d ON b.district_id = d.id
    ORDER BY b.district_id, b.id
""")
blocks = cur.fetchall()
for b in blocks:
    print(f"  BlockID={b['id']:4d} | DistrictID={b['district_id']:3d} | "
          f"DistrictName={str(b.get('district_name','')):20s} | DistrictSlug={str(b.get('district_slug','')):20s} | "
          f"BlockName={b['name']:25s} | BlockSlug={b['slug']}")

# ──────────────────────────────────────────────
# 6. ORPHAN PLACES (no district or invalid district)
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 6: ORPHAN / PROBLEM PLACES")
print("=" * 80)
cur.execute("""
    SELECT p.id, p.name, p.slug, p.district_id, p.description
    FROM places p
    WHERE p.district_id IS NULL OR p.district_id NOT IN (SELECT id FROM districts)
       OR p.name IS NULL OR p.name = ''
""")
orphans = cur.fetchall()
if orphans:
    for o in orphans:
        print(f"  ⚠️ PlaceID={o['id']} | Name='{o['name']}' | DistrictID={o['district_id']} | "
              f"Slug='{o['slug']}' | Desc='{str(o['description'])[:50]}'")
else:
    print("  ✅ No orphan places found.")

# ──────────────────────────────────────────────
# 7. DUPLICATE DISTRICT CHECK
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 7: DUPLICATE DISTRICT NAMES")
print("=" * 80)
cur.execute("""
    SELECT name, COUNT(*) AS cnt, GROUP_CONCAT(id) AS ids, GROUP_CONCAT(slug) AS slugs
    FROM districts
    GROUP BY name
    HAVING COUNT(*) > 1
""")
dupes = cur.fetchall()
if dupes:
    for dd in dupes:
        print(f"  ⚠️ DUPLICATE: Name='{dd['name']}' Count={dd['cnt']} IDs=[{dd['ids']}] Slugs=[{dd['slugs']}]")
else:
    print("  ✅ No duplicate district names.")

# ──────────────────────────────────────────────
# 8. DISTRICT FOODS
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 8: DISTRICT FOODS")
print("=" * 80)
try:
    cur.execute("""
        SELECT df.id, df.district_id, d.name AS district_name, d.slug AS district_slug,
               df.name AS food_name
        FROM district_foods df
        LEFT JOIN districts d ON df.district_id = d.id
        ORDER BY df.district_id, df.id
    """)
    foods = cur.fetchall()
    for f in foods:
        print(f"  FoodID={f['id']:4d} | DistrictID={f['district_id']:3d} | "
              f"DistrictName={str(f.get('district_name','')):20s} | Food='{f['food_name']}'")
except Exception as e:
    print(f"  (district_foods table not found or error: {e})")

# ──────────────────────────────────────────────
# 9. SERVICES TABLE SAMPLE
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 9: SERVICES (sample — first 20)")
print("=" * 80)
try:
    cur.execute("""
        SELECT s.id, s.name, s.district_id, d.name AS district_name, d.slug AS district_slug,
               s.service_type, s.block_id
        FROM services s
        LEFT JOIN districts d ON s.district_id = d.id
        ORDER BY s.district_id, s.id
        LIMIT 20
    """)
    services = cur.fetchall()
    for s in services:
        print(f"  ServiceID={s['id']:4d} | DistrictID={s['district_id']:3d} | "
              f"DistrictName={str(s.get('district_name','')):20s} | Type={s['service_type']:15s} | Name={s['name']}")
except Exception as e:
    print(f"  (services table not found or error: {e})")

# ──────────────────────────────────────────────
# 10. CROSS-REFERENCE: Seed script order vs DB order
# ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("SECTION 10: SEED SCRIPT ORDER vs DB DISTRICT ORDER")
print("=" * 80)

seed_order = [
    "Patna", "Gaya", "Nalanda", "Vaishali", "Muzaffarpur", "Bhagalpur",
    "Munger", "Rohtas", "Madhubani", "Darbhanga", "Sitamarhi",
    "West Champaran", "East Champaran", "Saran", "Siwan", "Gopalganj",
    "Nawada", "Aurangabad", "Jehanabad", "Arwal", "Jamui", "Lakhisarai",
    "Sheikhpura", "Begusarai", "Samastipur", "Khagaria", "Katihar",
    "Purnia", "Kishanganj", "Araria", "Supaul", "Madhepura", "Saharsa",
    "Banka", "Buxar", "Bhojpur", "Kaimur", "Sheohar"
]

print(f"  Seed script has {len(seed_order)} districts.")
print(f"  Database has {len(districts)} districts.")
print()
print(f"  {'Seed#':>6} {'SeedName':20s} | {'DB_ID':>5} {'DB_Name':20s} {'DB_Slug':25s} {'MATCH':>8}")
print(f"  {'─'*6} {'─'*20} | {'─'*5} {'─'*20} {'─'*25} {'─'*8}")

for i, seed_name in enumerate(seed_order):
    db_idx = i  # 0-indexed into districts list
    if db_idx < len(districts):
        db = districts[db_idx]
        name_match = "✅" if db['name'] == seed_name else "❌ NAME"
        expected = expected_slug(seed_name)
        slug_match = "✅" if db['slug'] == expected else "❌ SLUG"
        print(f"  {i+1:>6} {seed_name:20s} | {db['id']:>5} {db['name']:20s} {db['slug']:25s} {name_match} {slug_match}")
    else:
        print(f"  {i+1:>6} {seed_name:20s} | (no matching DB row)")

cur.close()
conn.close()
print("\n" + "=" * 80)
print("AUDIT COMPLETE — ALL QUERIES WERE READ-ONLY")
print("=" * 80)
