import sys
from collections import Counter
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
    ORDER BY d.name, p.name
""")
places = cur.fetchall()

print(f"Total Active Places: {len(places)}")

# District counts
dist_counts = Counter(p['district_name'] for p in places)
print("\n--- DISTRICT DISTRIBUTION (Sorted by count ascending) ---")
for d, c in sorted(dist_counts.items(), key=lambda x: (x[1], x[0])):
    print(f"  {d:<25} ({c} places)")

# Category counts
cat_counts = Counter(p['category'] for p in places)
print("\n--- CATEGORY DISTRIBUTION ---")
for cat, c in sorted(cat_counts.items(), key=lambda x: -x[1]):
    print(f"  {cat:<15}: {c:>3} ({c/len(places)*100:>5.1f}%)")

print("\n--- DISTRICTS WITH <= 2 PLACES ---")
for d, c in sorted(dist_counts.items(), key=lambda x: (x[1], x[0])):
    if c <= 2:
        print(f"  {d}: {c} places")

print("\n--- DISTRICTS WITH 3 PLACES ---")
for d, c in sorted(dist_counts.items(), key=lambda x: (x[1], x[0])):
    if c == 3:
        print(f"  {d}: {c} places")
