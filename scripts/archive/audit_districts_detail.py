import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()
cur.execute('''
    SELECT d.id, d.name, COUNT(p.id) as place_count, GROUP_CONCAT(CONCAT(p.id, ':', p.name) SEPARATOR ' | ') as places
    FROM districts d
    LEFT JOIN places p ON d.id = p.district_id AND p.deleted_at IS NULL
    GROUP BY d.id, d.name
    ORDER BY place_count ASC, d.name ASC
''')
print("=" * 100)
print("DISTRICT BREAKDOWN IN LIVE DATABASE (148 ACTIVE PLACES)")
print("=" * 100)
for r in cur.fetchall():
    print(f"{r['id']:2d} | {r['name']:15s} | Count: {r['place_count']} | {r['places']}")
