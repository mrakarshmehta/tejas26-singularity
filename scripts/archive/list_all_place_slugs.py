import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute('SELECT p.id, p.name, p.slug, d.name AS district_name FROM places p JOIN districts d ON d.id = p.district_id WHERE p.deleted_at IS NULL ORDER BY d.id, p.id')
    for r in cur.fetchall():
        print(f"#{r['id']:2d} [{r['district_name']:15s}] {r['name']:35s} -> /place/{r['slug']}")
