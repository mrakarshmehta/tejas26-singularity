import sys
import os
import csv
import math
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

sys.stdout.reconfigure(encoding='utf-8')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with get_cursor() as cursor:
    cursor.execute("""
        SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name 
        FROM places p 
        JOIN districts d ON p.district_id = d.id 
        WHERE p.deleted_at IS NULL 
        ORDER BY p.id
    """)
    active_places = cursor.fetchall()

with open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', mode='r', encoding='utf-8') as f:
    master = list(csv.DictReader(f))

# Let's see all candidates that have P0 or P1 priority and are NOT in active_places
uninserted_p0_p1 = []

for row in master:
    prio = row.get('recommended_priority', '').strip()
    if prio not in ('P0', 'P1'):
        continue
    name = row['place_name'].strip()
    dist_name = row['district'].strip()
    coords = row['coordinates'].strip().split(',')
    lat = float(coords[0].strip()) if len(coords) >= 2 else None
    lng = float(coords[1].strip()) if len(coords) >= 2 else None
    
    # check if in active_places
    matched = None
    for p in active_places:
        p_name = p['name'].lower().replace('&', 'and').replace(',', '').strip()
        c_name = name.lower().replace('&', 'and').replace(',', '').strip()
        if c_name in p_name or p_name in c_name:
            matched = p
            break
        # token overlap
        words_c = set(c_name.split()) - {'and', 'the', 'of', 'temple', 'fort', 'sanctuary', 'lake', 'dham', 'caves'}
        words_p = set(p_name.split()) - {'and', 'the', 'of', 'temple', 'fort', 'sanctuary', 'lake', 'dham', 'caves'}
        if words_c and words_p and words_c.intersection(words_p) == words_c:
            matched = p
            break
        if lat and lng and p['latitude'] and p['longitude']:
            try:
                dist = haversine(lat, lng, float(p['latitude']), float(p['longitude']))
                if dist < 0.5:
                    matched = p
                    break
            except: pass
    
    if not matched:
        min_dist = 9999.0
        nearest_p = None
        if lat and lng:
            for p in active_places:
                if p['latitude'] and p['longitude']:
                    d = haversine(lat, lng, float(p['latitude']), float(p['longitude']))
                    if d < min_dist:
                        min_dist = d
                        nearest_p = p
        uninserted_p0_p1.append({
            'name': name,
            'district': dist_name,
            'category': row.get('category'),
            'lat': lat,
            'lng': lng,
            'min_dist': min_dist,
            'nearest_p': nearest_p['name'] if nearest_p else 'None',
            'rec_priority': prio,
            'primary_source': row.get('primary_source'),
            'secondary_source': row.get('secondary_source'),
            'reason': row.get('reason'),
        })

print(f"Total uninserted P0/P1 candidates: {len(uninserted_p0_p1)}\n")
print("\n=== UNINSERTED P0 CANDIDATES ===")
p0_list = [c for c in uninserted_p0_p1 if c['rec_priority'] == 'P0']
for c in p0_list:
    print(f"P0 | {c['name']:<42} | {c['district']:<15} | {c['category']:<12} | {c['min_dist']:>6.2f} km | {c['nearest_p']}")

print(f"\nTotal P0 candidates uninserted: {len(p0_list)}")
