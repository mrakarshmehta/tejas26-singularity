import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cursor:
    cursor.execute("SELECT id, name, slug, state_id FROM districts ORDER BY id")
    all_d = cursor.fetchall()
    print(f"Total districts in DB: {len(all_d)}")
    for d in all_d:
        print(f"ID: {d['id']:2} | Name: {repr(d['name']):25} | Slug: {d['slug']}")
