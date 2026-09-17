import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

cur.execute("""
    SELECT d.id, d.name, d.slug, COUNT(p.id) AS active_cnt
    FROM districts d
    LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
    GROUP BY d.id, d.name, d.slug
    ORDER BY active_cnt ASC, d.name ASC
""")
rows = cur.fetchall()

print(f"{'District':<25} | {'DB ID':<5} | {'Active Places':<14} | {'Slug'}")
print("-" * 60)
for r in rows:
    print(f"{r['name']:<25} | {r['id']:<5} | {r['active_cnt']:<14} | {r['slug']}")
