import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    cur.execute("""
        SELECT p.id, p.name, p.slug, p.district_id, d.name as district_name, p.category, p.deleted_at
        FROM places p
        LEFT JOIN districts d ON p.district_id = d.id
        WHERE p.name LIKE '%Mahabodhi%' OR p.name LIKE '%Buddha%' OR p.name LIKE '%Bodh%'
    """)
    for r in cur.fetchall():
        print(r)
