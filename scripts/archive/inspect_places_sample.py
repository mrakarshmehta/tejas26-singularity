import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    for did, name in [(2, 'Gaya'), (3, 'Nalanda'), (4, 'Jamui'), (1, 'Patna')]:
        cur.execute("""
            SELECT id, name, slug, category, district_id
            FROM places
            WHERE district_id = %s AND deleted_at IS NULL
            ORDER BY name
        """, (did,))
        rows = cur.fetchall()
        print(f"\n--- {name} (District ID {did}) ({len(rows)} places) ---")
        for r in rows:
            print(f"  ID {r['id']:3d}: {r['name']:<35} [{r['category']}]")
