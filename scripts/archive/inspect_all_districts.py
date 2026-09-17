import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()
cur.execute("""
    SELECT d.id AS district_id, d.name AS district_name, p.id, p.name, p.category, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
    ORDER BY d.name, p.id
""")
rows = cur.fetchall()

dmap = {}
for r in rows:
    dmap.setdefault((r['district_id'], r['district_name']), []).append(r)

print(f"--- ACTIVE 138 DESTINATIONS ACROSS {len(dmap)} DISTRICTS ---")
for (did, dname), places in sorted(dmap.items(), key=lambda x: x[0][1]):
    names = [f"{p['id']}:{p['name']} ({p['category']})" for p in places]
    print(f"\n{dname} (ID {did}, Total: {len(places)}):")
    for n in names:
        print(f"  - {n}")
