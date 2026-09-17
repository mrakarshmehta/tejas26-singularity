import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()
cur.execute("SELECT id, name, slug FROM districts ORDER BY id")
rows = cur.fetchall()

print(f"Total districts in DB: {len(rows)}")
for r in rows:
    print(f"ID: {r['id']:2d} | Name: {r['name']:<25} | Slug: {r['slug']}")

# Specific lookups for the 10 Batch 8 candidates:
candidates_dist = [
    'Bhojpur',
    'Darbhanga',
    'Muzaffarpur',
    'Saharsa',
    'Purnia',
    'Buxar',
    'Nawada',
    'Saran',
    'Gopalganj',
    'Supaul'
]

print("\n--- EXACT LOOKUP FOR THE 10 BATCH 8 DISTRICTS ---")
for dname in candidates_dist:
    cur.execute("SELECT id, name, slug FROM districts WHERE LOWER(name) LIKE %s", (f"%{dname.lower()}%",))
    matches = cur.fetchall()
    print(f"Query '{dname}':")
    for m in matches:
        print(f"  -> id={m['id']}, name='{m['name']}', slug='{m['slug']}'")
