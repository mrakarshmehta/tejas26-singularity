import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

text_cols_places = ['description', 'travel_tips', 'local_tips', 'safety_tips', 'best_time_to_visit', 'entry_fee', 'history']

with get_cursor() as cur:
    cur.execute("SELECT id, name, " + ", ".join(text_cols_places) + " FROM places WHERE deleted_at IS NULL")
    places = cur.fetchall()
    
    found_places = []
    for p in places:
        for col in text_cols_places:
            val = p.get(col) or ''
            if '???' in val:
                found_places.append((p['id'], p['name'], col, val))
    
    print(f"Places with '???': {len(found_places)}")
    for pid, pname, col, val in found_places:
        print(f"  #{pid} {pname} [{col}]: {repr(val[:100])}")

with get_cursor() as cur:
    cur.execute("SELECT id, name, description, best_places_to_eat FROM district_foods")
    foods = cur.fetchall()
    
    found_foods = []
    for f in foods:
        for col in ['description', 'best_places_to_eat']:
            val = f.get(col) or ''
            if '???' in val:
                found_foods.append((f['id'], f['name'], col, val))
    
    print(f"\nDistrict foods with '???': {len(found_foods)}")
    for fid, fname, col, val in found_foods:
        print(f"  #{fid} {fname} [{col}]: {repr(val[:100])}")
