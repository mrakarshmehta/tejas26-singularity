import sys, csv, os, math
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with get_cursor() as cur:
    cur.execute('SELECT id, name, slug, category, latitude, longitude, district_id FROM places WHERE deleted_at IS NULL')
    active_places = cur.fetchall()

active_names = {p['name'].lower().strip() for p in active_places}
print(f'Total Active Places in MySQL: {len(active_places)}')

# Load PHASE5_MASTER_CANDIDATE_QUEUE.csv
with open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', mode='r', encoding='utf-8') as f:
    p5 = list(csv.DictReader(f))

candidates = []
for row in p5:
    name = row.get('place_name', '').strip()
    # Check if already active in MySQL
    is_active = any(name.lower() in ap['name'].lower() or ap['name'].lower() in name.lower() for ap in active_places)
    
    coord_str = row.get('coordinates', '')
    lat, lng = None, None
    if ',' in coord_str:
        try:
            parts = coord_str.split(',')
            lat = float(parts[0].strip())
            lng = float(parts[1].strip())
        except Exception:
            pass

    min_dist = 9999.0
    nearest_p = None
    if lat and lng:
        for ap in active_places:
            alat = float(ap['latitude'] or 0)
            alng = float(ap['longitude'] or 0)
            if alat and alng:
                d = haversine(lat, lng, alat, alng)
                if d < min_dist:
                    min_dist = d
                    nearest_p = ap['name']
                    
    candidates.append({
        'rank': int(row.get('rank', 999)),
        'name': name,
        'district': row.get('district', ''),
        'category': row.get('category', ''),
        'lat': lat,
        'lng': lng,
        'is_active': is_active,
        'min_dist': min_dist,
        'nearest_p': nearest_p,
        'prio': row.get('recommended_priority', ''),
        'primary_source': row.get('primary_source', ''),
        'secondary_source': row.get('secondary_source', ''),
        'reason': row.get('reason', '')
    })

print(f"\n--- NON-ACTIVE CANDIDATES FROM MASTER QUEUE ---")
non_active = [c for c in candidates if not c['is_active']]
print(f"Total non-active candidates: {len(non_active)}")

for c in non_active:
    print(f"Rank #{c['rank']:>2} [{c['prio']:2}]: {c['name']:42} | Dist: {c['district']:15} | Cat: {c['category']:10} | MinDist: {c['min_dist']:5.1f}km ({c['nearest_p']})")
