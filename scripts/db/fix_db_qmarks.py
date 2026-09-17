import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor(commit=True) as cur:
    # 1. Update district_foods
    cur.execute("SELECT id, name, description, best_places_to_eat FROM district_foods")
    foods = cur.fetchall()
    food_fixes = 0
    for f in foods:
        new_desc = f['description'].replace(' ??? ', ' — ').replace('???', '—') if f['description'] else f['description']
        new_best = f['best_places_to_eat'].replace(' ??? ', ' — ').replace('???', '—') if f['best_places_to_eat'] else f['best_places_to_eat']
        if new_desc != f['description'] or new_best != f['best_places_to_eat']:
            cur.execute("UPDATE district_foods SET description = %s, best_places_to_eat = %s WHERE id = %s", (new_desc, new_best, f['id']))
            food_fixes += 1
            print(f"Fixed Food #{f['id']} {f['name']}")

    # 2. Update places
    cur.execute("SELECT id, name, description, travel_tips, local_tips, safety_tips, history FROM places")
    places = cur.fetchall()
    place_fixes = 0
    for p in places:
        updates = {}
        for col in ['description', 'travel_tips', 'local_tips', 'safety_tips', 'history']:
            val = p.get(col)
            if val and '???' in val:
                fixed_val = val
                # Fix rupee symbol
                fixed_val = fixed_val.replace('(???', '(₹').replace('???', ' — ')
                # Fix double dash spacing
                fixed_val = fixed_val.replace('  —  ', ' — ')
                # Fix year ranges like 1912 — 1915 -> 1912–1915
                fixed_val = fixed_val.replace('1912 — 1915', '1912–1915')
                updates[col] = fixed_val
        
        if updates:
            sets = [f"{k} = %s" for k in updates.keys()]
            vals = list(updates.values()) + [p['id']]
            cur.execute(f"UPDATE places SET {', '.join(sets)} WHERE id = %s", vals)
            place_fixes += 1
            print(f"Fixed Place #{p['id']} {p['name']}: {list(updates.keys())}")

print(f"\nCompleted: {food_fixes} food items fixed, {place_fixes} places fixed.")
