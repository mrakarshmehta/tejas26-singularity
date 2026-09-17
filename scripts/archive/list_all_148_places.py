import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
    ORDER BY d.id, p.id
""")
rows = cur.fetchall()

print(f"ACTIVE PLACES IN DATABASE: {len(rows)}\n")
current_d = None
for r in rows:
    if r['district_name'] != current_d:
        current_d = r['district_name']
        print(f"\n[{r['district_id']}] {current_d}:")
    print(f"   ID {r['id']:<3} | {r['name']:<45} | {r['category']:<12} | ({r['latitude']}, {r['longitude']}) | slug: {r['slug']}")
