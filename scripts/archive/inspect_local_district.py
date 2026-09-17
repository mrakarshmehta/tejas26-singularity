import os, sys
# Load .env into os.environ
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from models.connection import get_cursor

def inspect(district_slug):
    with get_cursor() as cur:
        cur.execute("SELECT * FROM districts WHERE slug=%s OR name=%s", (district_slug, district_slug.capitalize()))
        district = cur.fetchone()
        print(f"\n==================== DISTRICT: {district_slug.upper()} ====================")
        print("=== METADATA ===")
        print(json.dumps(district, indent=2, default=str))

        if not district:
            print(f"District {district_slug} NOT FOUND in local database.")
            return None

        dist_id = district['id']
        cur.execute("SELECT * FROM blocks WHERE district_id=%s ORDER BY id", (dist_id,))
        blocks = cur.fetchall()
        print(f"\n=== BLOCKS ({len(blocks)}) ===")
        for b in blocks:
            print(f"  - [{b['id']}] {b['name']} (slug: {b['slug']})")

        cur.execute("SELECT * FROM places WHERE district_id=%s ORDER BY id", (dist_id,))
        places = cur.fetchall()
        print(f"\n=== PLACES ({len(places)}) ===")
        for p in places:
            print(f"  - [{p['id']}] {p['name']} (slug: {p['slug']}, category: {p['category']}, coords: {p.get('latitude')},{p.get('longitude')}, gem: {p.get('is_hidden_gem')}, feat: {p.get('is_featured')}, img: {p.get('cover_image')})")

        cur.execute("SELECT * FROM district_foods WHERE district_id=%s ORDER BY id", (dist_id,))
        foods = cur.fetchall()
        print(f"\n=== FOODS ({len(foods)}) ===")
        for f in foods:
            print(f"  - [{f['id']}] {f['name']}: {f.get('description')} (img: {f.get('image_url') or f.get('cover_image')})")

        return {
            'district': district,
            'blocks': blocks,
            'places': places,
            'foods': foods
        }

if __name__ == '__main__':
    jamui_local = inspect('jamui')
    gaya_local = inspect('gaya')
    
    with open('scratch/local_district_data.json', 'w', encoding='utf-8') as f:
        json.dump({'jamui': jamui_local, 'gaya': gaya_local}, f, indent=2, default=str)
