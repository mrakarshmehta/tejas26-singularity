"""
Post-Repair Complete Integrity Check & Verification
Checks:
1. District name/slug consistency across all 38 districts
2. Duplicate district slugs
3. Places pointing to nonexistent districts
4. Places with NULL district_id
5. Orphan places or empty names
6. Blocks pointing to nonexistent districts
7. Food/services pointing to nonexistent districts
8. Rajgir status verification (Rajgir is NOT a district, places/blocks under Nalanda)
9. Specific districts deep check: Jamui, Nalanda, Gaya, Bhagalpur, Kaimur, Patna, Muzaffarpur
"""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

print("=" * 80)
print("POST-REPAIR DATA INTEGRITY AUDIT")
print("=" * 80)

errors = []

# 1. Total districts count
cur.execute("SELECT COUNT(*) AS c FROM districts")
dist_count = cur.fetchone()['c']
print(f"1. Total Districts: {dist_count} (Expected: 38)")
if dist_count != 38:
    errors.append(f"Expected 38 districts, got {dist_count}")

# 2. District name ↔ slug consistency
cur.execute("SELECT id, name, slug FROM districts ORDER BY id")
districts = cur.fetchall()
slug_mismatches = 0
for d in districts:
    expected_slug = re.sub(r'[^a-z0-9]+', '-', d['name'].lower().strip()).strip('-')
    if d['slug'] != expected_slug:
        slug_mismatches += 1
        errors.append(f"District ID {d['id']} ('{d['name']}'): slug is '{d['slug']}', expected '{expected_slug}'")
print(f"2. District Name ↔ Slug Consistency: {len(districts) - slug_mismatches}/{len(districts)} matched (Mismatches: {slug_mismatches})")

# 3. Duplicate slugs
cur.execute("SELECT state_id, slug, COUNT(*) AS c FROM districts GROUP BY state_id, slug HAVING c > 1")
dup_slugs = cur.fetchall()
print(f"3. Duplicate Slugs: {len(dup_slugs)}")
if dup_slugs:
    for ds in dup_slugs:
        errors.append(f"Duplicate slug: {ds['slug']} (count: {ds['c']})")

# 4. Places pointing to nonexistent districts
cur.execute("SELECT p.id, p.name, p.district_id FROM places p LEFT JOIN districts d ON p.district_id = d.id WHERE d.id IS NULL AND p.deleted_at IS NULL")
invalid_places = cur.fetchall()
print(f"4. Places with Invalid district_id: {len(invalid_places)}")
if invalid_places:
    for ip in invalid_places:
        errors.append(f"Place ID {ip['id']} ('{ip['name']}') has invalid district_id {ip['district_id']}")

# 5. Empty or orphan places
cur.execute("SELECT id, name, slug, district_id FROM places WHERE name IS NULL OR TRIM(name) = ''")
empty_places = cur.fetchall()
print(f"5. Places with Empty Names: {len(empty_places)}")
if empty_places:
    for ep in empty_places:
        errors.append(f"Place ID {ep['id']} has empty name")

# 6. Blocks pointing to nonexistent districts
cur.execute("SELECT b.id, b.name, b.district_id FROM blocks b LEFT JOIN districts d ON b.district_id = d.id WHERE d.id IS NULL")
invalid_blocks = cur.fetchall()
print(f"6. Blocks with Invalid district_id: {len(invalid_blocks)}")
if invalid_blocks:
    for ib in invalid_blocks:
        errors.append(f"Block ID {ib['id']} ('{ib['name']}') has invalid district_id {ib['district_id']}")

# 7. Foods pointing to nonexistent districts
cur.execute("SELECT df.id, df.name, df.district_id FROM district_foods df LEFT JOIN districts d ON df.district_id = d.id WHERE d.id IS NULL")
invalid_foods = cur.fetchall()
print(f"7. Foods with Invalid district_id: {len(invalid_foods)}")
if invalid_foods:
    for ifd in invalid_foods:
        errors.append(f"Food ID {ifd['id']} ('{ifd['name']}') has invalid district_id {ifd['district_id']}")

# 8. Services pointing to nonexistent districts
cur.execute("SELECT s.id, s.name, s.district_id FROM nearby_services s LEFT JOIN districts d ON s.district_id = d.id WHERE s.district_id IS NOT NULL AND d.id IS NULL")
invalid_services = cur.fetchall()
print(f"8. Services with Invalid district_id: {len(invalid_services)}")
if invalid_services:
    for isv in invalid_services:
        errors.append(f"Service ID {isv['id']} ('{isv['name']}') has invalid district_id {isv['district_id']}")

# 9. Rajgir check (must NOT exist as district)
cur.execute("SELECT id, name, slug FROM districts WHERE name LIKE '%Rajgir%' OR slug LIKE '%rajgir%'")
rajgir_dist = cur.fetchall()
print(f"9. Rajgir as District Check: {len(rajgir_dist)} found ({'CORRECT: Rajgir is NOT a district' if len(rajgir_dist) == 0 else 'ERROR: Rajgir exists as district'})")
if rajgir_dist:
    errors.append("Rajgir exists as a district row")

# 10. Deep verification on specific key districts
print("\n" + "=" * 80)
print("DEEP VERIFICATION ON KEY DISTRICTS")
print("=" * 80)

key_districts = {
    'patna': 1,
    'gaya': 2,
    'nalanda': 3,
    'jamui': 4,
    'bhagalpur': 5,
    'munger': 6,
    'muzaffarpur': 7,
    'rohtas': 8,
    'kaimur': 22,
    'nawada': 38
}

for slug, expected_id in key_districts.items():
    cur.execute("""
        SELECT d.id, d.name, d.slug, d.cover_image,
               COUNT(DISTINCT p.id) AS place_count,
               COUNT(DISTINCT b.id) AS block_count,
               COUNT(DISTINCT df.id) AS food_count,
               COUNT(DISTINCT ns.id) AS service_count,
               GROUP_CONCAT(DISTINCT p.name SEPARATOR ' | ') AS places_list
        FROM districts d
        LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
        LEFT JOIN blocks b ON b.district_id = d.id
        LEFT JOIN district_foods df ON df.district_id = d.id
        LEFT JOIN nearby_services ns ON ns.district_id = d.id
        WHERE d.slug = %s
        GROUP BY d.id
    """, (slug,))
    row = cur.fetchone()
    if row:
        print(f"\n📍 District: {row['name']} (Slug: {row['slug']}, ID: {row['id']})")
        print(f"   Cover Image: {row['cover_image']}")
        print(f"   Places ({row['place_count']}): {str(row['places_list'])[:100]}...")
        print(f"   Blocks: {row['block_count']} | Foods: {row['food_count']} | Services: {row['service_count']}")
    else:
        print(f"\n❌ District slug '{slug}' not found!")
        errors.append(f"District slug '{slug}' not found")

cur.close()
conn.close()

print("\n" + "=" * 80)
if errors:
    print(f"❌ INTEGRITY CHECK FAILED WITH {len(errors)} ERRORS:")
    for e in errors:
        print(f"   - {e}")
else:
    print("✅ ALL POST-REPAIR INTEGRITY CHECKS PASSED WITH ZERO ERRORS!")
print("=" * 80)
