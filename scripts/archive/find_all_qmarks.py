import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute("SELECT id, name, description, tips, best_time, entry_fee FROM places WHERE description LIKE '%?%' OR tips LIKE '%?%' OR best_time LIKE '%?%' OR entry_fee LIKE '%?%'")
    p_rows = cur.fetchall()
    print(f"Places with literal '???': {len(p_rows)}")
    for r in p_rows:
        for col in ['description', 'tips', 'best_time', 'entry_fee']:
            val = r.get(col) or ''
            if '???' in val:
                print(f"  Place #{r['id']} {r['name']} [{col}]: {val}")

with get_cursor() as cur:
    cur.execute("SELECT id, name, description, best_places_to_eat FROM district_foods WHERE description LIKE '%?%' OR best_places_to_eat LIKE '%?%'")
    f_rows = cur.fetchall()
    print(f"\nDistrict foods with literal '???': {len(f_rows)}")
    for r in f_rows:
        for col in ['description', 'best_places_to_eat']:
            val = r.get(col) or ''
            if '???' in val:
                print(f"  Food #{r['id']} {r['name']} [{col}]: {val}")

with get_cursor() as cur:
    cur.execute("SELECT id, name, description, famous_for FROM districts WHERE description LIKE '%?%' OR famous_for LIKE '%?%'")
    d_rows = cur.fetchall()
    print(f"\nDistricts with literal '???': {len(d_rows)}")
    for r in d_rows:
        for col in ['description', 'famous_for']:
            val = r.get(col) or ''
            if '???' in val:
                print(f"  District #{r['id']} {r['name']} [{col}]: {val}")
