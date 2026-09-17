import sys, os
sys.path.insert(0, os.path.abspath('.'))
from dotenv import load_dotenv
load_dotenv()

from models.connection import get_cursor

def check_all():
    with get_cursor() as cur:
        # Places with missing name or district_id or description
        cur.execute("SELECT id, name, slug, district_id, category, description FROM places WHERE deleted_at IS NULL AND (name = '' OR district_id IS NULL OR name IS NULL)")
        print("=== PLACES WITH MISSING NAME OR DISTRICT_ID ===")
        for p in cur.fetchall():
            print(p)

        # Check all districts table entries
        cur.execute("SELECT id, name, slug FROM districts ORDER BY id")
        print("\n=== CURRENT DISTRICTS TABLE ===")
        for d in cur.fetchall():
            print(f"ID {d['id']:2d}: Name = {d['name']:25s} | Slug = {d['slug']}")

check_all()
