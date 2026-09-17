import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute("SELECT id, name, description, famous_places FROM district_foods WHERE description LIKE '%?%' OR famous_places LIKE '%?%'")
    rows = cur.fetchall()
    print(f"District foods with '?' or '???': {len(rows)}")
    for r in rows[:10]:
        print(f"#{r['id']} {r['name']}:")
        print(f"  Desc: {repr(r['description'][:100])}")
        print(f"  Places: {repr(r['famous_places'])}")

with get_cursor() as cur:
    cur.execute("SELECT id, name, description, tips FROM places WHERE description LIKE '%?%' OR tips LIKE '%?%'")
    p_rows = cur.fetchall()
    print(f"\nPlaces with '?' or '???': {len(p_rows)}")
    for r in p_rows[:10]:
        print(f"#{r['id']} {r['name']}:")
        print(f"  Desc: {repr(r['description'][:100]) if r['description'] else 'None'}")
        print(f"  Tips: {repr(r['tips'][:100]) if r['tips'] else 'None'}")
