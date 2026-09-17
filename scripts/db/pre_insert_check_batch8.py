import sys
import math
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

print("=" * 80)
print("PRE-INSERT CHECK FOR BATCH 8")
print("=" * 80)

# 1. Active count must be 138
cur.execute("SELECT COUNT(*) AS active_cnt FROM places WHERE deleted_at IS NULL")
active_cnt = cur.fetchone()['active_cnt']
print(f"1. Active places count: {active_cnt} (Must be 138) -> {'PASS' if active_cnt == 138 else 'FAIL'}")
if active_cnt != 138:
    print("FATAL: Baseline active count is not 138! Aborting.")
    sys.exit(1)

# 2. MAX(id) must be 188
cur.execute("SELECT MAX(id) AS max_id FROM places WHERE deleted_at IS NULL")
max_id = cur.fetchone()['max_id']
print(f"2. Current MAX(id): {max_id} (Must be 188) -> {'PASS' if max_id == 188 else 'FAIL'}")
if max_id != 188:
    print("FATAL: Current MAX(id) is not 188! Aborting.")
    sys.exit(1)

# 3. District count must be 38
cur.execute("SELECT COUNT(DISTINCT district_id) AS dist_cnt FROM places WHERE deleted_at IS NULL")
dist_cnt = cur.fetchone()['dist_cnt']
print(f"3. Distinct districts in active places: {dist_cnt}/38 -> {'PASS' if dist_cnt == 38 else 'FAIL'}")
if dist_cnt != 38:
    print("FATAL: District count is not 38! Aborting.")
    sys.exit(1)

# 4. Verify all 10 district IDs from LIVE DB
candidate_districts = {
    'Ara House': ('Bhojpur', 16),
    'Ahilya Sthan, Ahiyari': ('Darbhanga', 18),
    'Baba Garibnath Temple': ('Muzaffarpur', 7),
    'Surya Mandir, Kandaha': ('Saharsa', 29),
    'Mata Puran Devi Temple': ('Purnia', 28),
    'Baba Brahmeshwar Nath Temple, Brahmpur': ('Buxar', 17),
    'Gunawa Ji (Jain Tirth)': ('Nawada', 38),
    'Ambika Sthan, Aami': ('Saran', 31),
    'Lakri Dargah': ('Gopalganj', 19),
    'Baba Tileshwar Nath Mandir, Sukhpur': ('Supaul', 36)
}

print("\n4. District ID Live Verification:")
for cname, (dname, exp_id) in candidate_districts.items():
    cur.execute("SELECT id, name, slug FROM districts WHERE name = %s", (dname,))
    row = cur.fetchone()
    if not row or row['id'] != exp_id:
        print(f"  FAIL: {dname} expected id {exp_id}, found {row}")
        sys.exit(1)
    else:
        print(f"  PASS: {cname:<38} -> District: {dname:<12} (DB ID: {row['id']})")

# 5 & 6. Verify names and slugs are not active
batch8_names = list(candidate_districts.keys())
batch8_slugs = [
    'ara-house-bhojpur',
    'ahilya-sthan-ahiyari-darbhanga',
    'baba-garibnath-temple-muzaffarpur',
    'surya-mandir-kandaha-saharsa',
    'mata-puran-devi-temple-purnia',
    'baba-brahmeshwar-nath-temple-brahmpur-buxar',
    'gunawa-ji-jain-tirth-nawada',
    'ambika-sthan-aami-saran',
    'lakri-dargah-gopalganj',
    'baba-tileshwar-nath-mandir-sukhpur-supaul'
]

cur.execute("SELECT id, name FROM places WHERE deleted_at IS NULL AND name IN %s", (tuple(batch8_names),))
existing_names = cur.fetchall()
print(f"\n5. Active duplicate names: {len(existing_names)} (Must be 0) -> {'PASS' if len(existing_names) == 0 else 'FAIL'}")
if existing_names:
    print(f"  Existing: {existing_names}")
    sys.exit(1)

cur.execute("SELECT id, slug FROM places WHERE deleted_at IS NULL AND slug IN %s", (tuple(batch8_slugs),))
existing_slugs = cur.fetchall()
print(f"6. Active duplicate slugs: {len(existing_slugs)} (Must be 0) -> {'PASS' if len(existing_slugs) == 0 else 'FAIL'}")
if existing_slugs:
    print(f"  Existing: {existing_slugs}")
    sys.exit(1)

# 7. Verify coordinates are not duplicate
batch8_coords = [
    (25.5539, 84.6680),
    (26.2917, 85.8015),
    (26.1205, 85.3912),
    (25.8820, 86.4670),
    (25.7725, 87.4580),
    (25.5992, 84.2882),
    (24.8944, 85.5312),
    (25.6881, 85.0062),
    (26.3150, 84.4720),
    (26.0620, 86.6080)
]

print(f"\n7. Coordinate exact duplicate check:")
for lat, lng in batch8_coords:
    cur.execute("SELECT id, name FROM places WHERE deleted_at IS NULL AND ABS(latitude - %s) < 0.0001 AND ABS(longitude - %s) < 0.0001", (lat, lng))
    c_dupes = cur.fetchall()
    if c_dupes:
        print(f"  FAIL: Coords ({lat}, {lng}) collide with {c_dupes}")
        sys.exit(1)
print("  PASS: All 10 coordinates are unique and non-colliding.")

# 8. Categories valid
cur.execute("SELECT DISTINCT category FROM places WHERE deleted_at IS NULL")
valid_categories = {r['category'] for r in cur.fetchall()}
print(f"\n8. Category validation (Valid set: {valid_categories}):")
batch8_categories = ['historical', 'cultural', 'temple']
for cat in batch8_categories:
    if cat not in valid_categories:
        print(f"  FAIL: Category {cat} not in valid categories!")
        sys.exit(1)
    print(f"  PASS: Category '{cat}' is valid.")

# 9 & 10. Haversine overlap against all 138 active places
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

cur.execute("SELECT id, name, latitude, longitude FROM places WHERE deleted_at IS NULL")
all_active = cur.fetchall()

print("\n10. Complete Haversine Overlap Against All 138 Active Places:")
for idx, (name, slug) in enumerate(zip(batch8_names, batch8_slugs)):
    lat, lng = batch8_coords[idx]
    min_d = 99999
    nearest = None
    for ap in all_active:
        d = haversine_km(lat, lng, ap['latitude'], ap['longitude'])
        if d < min_d:
            min_d = d
            nearest = ap
    print(f"  [{idx+1}] {name:<38} -> Nearest: ID {nearest['id']} {nearest['name']} ({min_d:.2f} km)")

print("\nALL PRE-INSERT CHECKS PASSED PERFECTLY!")
