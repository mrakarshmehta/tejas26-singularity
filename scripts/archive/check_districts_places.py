import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    cur.execute("SELECT id, name, slug FROM districts WHERE name LIKE '%Vaishali%'")
    d = cur.fetchone()
    print('District:', d)
    if d:
        cur.execute("SELECT id, name, slug, latitude, longitude FROM places WHERE district_id = %s AND deleted_at IS NULL", (d['id'],))
        for p in cur.fetchall():
            print('  Place:', p)
