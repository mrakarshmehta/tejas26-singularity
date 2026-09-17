"""
Detailed district parity analysis between local MySQL and LIVE Render.
"""
import os, sys
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

def run_analysis():
    # 1. Fetch complete local data for Jamui, Gaya, Patna
    local_data = {}
    with get_cursor() as cur:
        for dist_name, dist_slug in [('Jamui', 'jamui'), ('Gaya', 'gaya'), ('Patna', 'patna')]:
            cur.execute("SELECT * FROM districts WHERE slug=%s OR name=%s", (dist_slug, dist_name))
            d = cur.fetchone()
            if d:
                dist_id = d['id']
                cur.execute("SELECT * FROM blocks WHERE district_id=%s ORDER BY id", (dist_id,))
                blocks = cur.fetchall()
                cur.execute("SELECT * FROM places WHERE district_id=%s ORDER BY id", (dist_id,))
                places = cur.fetchall()
                cur.execute("SELECT * FROM district_foods WHERE district_id=%s ORDER BY id", (dist_id,))
                foods = cur.fetchall()
                
                local_data[dist_slug] = {
                    'district': d,
                    'blocks': blocks,
                    'places': places,
                    'foods': foods
                }
            else:
                print(f"District {dist_name} not found locally!")

    # 2. Load live scraped data
    with open('scratch/live_district_data.json', 'r', encoding='utf-8') as f:
        live_data = json.load(f)

    print("================================================================================")
    print("HIDDENYATRA — LOCAL VS LIVE DISTRICT PARITY AUDIT")
    print("================================================================================")
    
    # 3. Analyze Jamui
    print("\n" + "="*80)
    print("DISTRICT 1: JAMUI (/state/bihar/jamui)")
    print("="*80)
    j_local = local_data.get('jamui', {})
    j_live = live_data.get('jamui', {})
    
    j_d_local = j_local.get('district', {})
    print(f"Local District ID: {j_d_local.get('id')}, Name: '{j_d_local.get('name')}', Slug: '{j_d_local.get('slug')}'")
    print(f"Live Heading: '{j_live.get('heading')}', Title: '{j_live.get('title')}'")
    
    # Compare Places
    local_places_by_slug = {p['slug']: p for p in j_local.get('places', [])}
    live_places_by_slug = {p['slug']: p for p in j_live.get('places_from_map_attr', [])}
    
    print(f"\nPlaces Count: Local = {len(local_places_by_slug)}, Live = {len(live_places_by_slug)}")
    
    missing_on_live = set(local_places_by_slug.keys()) - set(live_places_by_slug.keys())
    extra_on_live = set(live_places_by_slug.keys()) - set(local_places_by_slug.keys())
    common_places = set(local_places_by_slug.keys()) & set(live_places_by_slug.keys())
    
    print(f"Common places ({len(common_places)}):")
    for s in sorted(common_places):
        lp = local_places_by_slug[s]
        rp = live_places_by_slug[s]
        print(f"  - [{s}] '{lp['name']}' (Local ID: {lp['id']}, Live ID: {rp['id']})")
        
    print(f"\nAdded locally but MISSING on live ({len(missing_on_live)}):")
    for s in sorted(missing_on_live):
        print(f"  - {s}: {local_places_by_slug[s]['name']}")
        
    print(f"\nMissing locally but PRESENT on live ({len(extra_on_live)}):")
    for s in sorted(extra_on_live):
        print(f"  - {s}: {live_places_by_slug[s]['name']}")

    # Compare Blocks
    local_blocks = {b['slug']: b for b in j_local.get('blocks', [])}
    live_blocks = {b['href'].split('/')[-1]: b for b in j_live.get('blocks', [])}
    print(f"\nBlocks: Local = {len(local_blocks)}, Live = {len(live_blocks)}")
    print(f"Local block slugs: {sorted(local_blocks.keys())}")
    print(f"Live block slugs: {sorted(live_blocks.keys())}")
    
    # Compare Foods
    print(f"\nFoods: Local = {len(j_local.get('foods', []))}, Live = {len(j_live.get('foods', []))}")
    
    # 4. Analyze Control District 1: Gaya vs Gaya-Ji
    print("\n" + "="*80)
    print("CONTROL DISTRICT 1: GAYA / GAYA-JI")
    print("="*80)
    g_local = local_data.get('gaya', {})
    g_live = live_data.get('gaya_ji', {})
    print(f"Local Slug: 'gaya', Live Slug: 'gaya-ji'")
    print(f"Local Places Count: {len(g_local.get('places', []))}, Live Places Count: {len(g_live.get('places_from_map_attr', []))}")
    print(f"Local Blocks Count: {len(g_local.get('blocks', []))}, Live Blocks Count: {len(g_live.get('blocks', []))}")
    print(f"Local Foods Count: {len(g_local.get('foods', []))}, Live Foods Count: {len(g_live.get('foods', []))}")
    
    g_local_slugs = set(p['slug'] for p in g_local.get('places', []))
    g_live_slugs = set(p['slug'] for p in g_live.get('places_from_map_attr', []))
    print(f"Places matched: {len(g_local_slugs & g_live_slugs)} of {len(g_local_slugs)}")
    if g_local_slugs - g_live_slugs:
        print(f"Missing on live Gaya: {g_local_slugs - g_live_slugs}")
    if g_live_slugs - g_local_slugs:
        print(f"Extra on live Gaya: {g_live_slugs - g_local_slugs}")

    # 5. Analyze Control District 2: Patna
    print("\n" + "="*80)
    print("CONTROL DISTRICT 2: PATNA")
    print("="*80)
    p_local = local_data.get('patna', {})
    p_live = live_data.get('patna', {})
    print(f"Local Places Count: {len(p_local.get('places', []))}, Live Places Count: {len(p_live.get('places_from_map_attr', []))}")
    print(f"Local Blocks Count: {len(p_local.get('blocks', []))}, Live Blocks Count: {len(p_live.get('blocks', []))}")
    print(f"Local Foods Count: {len(p_local.get('foods', []))}, Live Foods Count: {len(p_live.get('foods', []))}")
    
    p_local_slugs = set(p['slug'] for p in p_local.get('places', []))
    p_live_slugs = set(p['slug'] for p in p_live.get('places_from_map_attr', []))
    print(f"Places matched: {len(p_local_slugs & p_live_slugs)} of {len(p_local_slugs)}")
    if p_local_slugs - p_live_slugs:
        print(f"Missing on live Patna: {p_local_slugs - p_live_slugs}")
    if p_live_slugs - p_local_slugs:
        print(f"Extra on live Patna: {p_live_slugs - p_local_slugs}")

if __name__ == '__main__':
    run_analysis()
