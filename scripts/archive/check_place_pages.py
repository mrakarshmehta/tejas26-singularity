import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    cur.execute("""
        SELECT p.id, p.name, d.name as district_name, p.is_featured
        FROM places p
        JOIN districts d ON p.district_id = d.id
        WHERE d.name IN ('Patna', 'Gaya', 'Jamui', 'Nalanda', 'Bhagalpur') AND p.deleted_at IS NULL
        ORDER BY p.id ASC
    """)
    rows = cur.fetchall()
    print(f"Total found: {len(rows)}")
    for r in rows:
        print(f"ID {r['id']}: {r['name']} ({r['district_name']}) - is_featured={r['is_featured']}")
