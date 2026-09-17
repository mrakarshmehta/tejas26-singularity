import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor
from collections import Counter

with get_cursor() as cur:
    cur.execute("SELECT id, name, category, district_id FROM places WHERE deleted_at IS NULL")
    places = cur.fetchall()

    cur.execute("SELECT id, name FROM districts")
    dist_map = {d['id']: d['name'] for d in cur.fetchall()}

cats = Counter(p['category'] for p in places)
print("=== CATEGORY DISTRIBUTION (108 PLACES) ===")
for cat, count in cats.most_common():
    print(f"  {cat:15}: {count}")

dist_counts = Counter(dist_map.get(p['district_id'], 'Unknown') for p in places)
print("\n=== DISTRICT COUNTS ===")
for dname, cnt in sorted(dist_counts.items(), key=lambda x: x[1]):
    print(f"  {dname:25}: {cnt}")
