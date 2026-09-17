import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    cur.execute('''
        SELECT d.id, d.name, d.slug, COUNT(p.id) as places_count
        FROM districts d
        LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
        GROUP BY d.id
        ORDER BY d.name ASC
    ''')
    districts = cur.fetchall()
    print(f'Total Districts in DB: {len(districts)}')
    for d in districts:
        print(f"  - ID {d['id']:2d}: {d['name']:<20} ({d['places_count']} places)")
