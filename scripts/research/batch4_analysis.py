import sys
import csv
import math
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 1. Load active 98 places from DB
with get_cursor() as cursor:
    cursor.execute("SELECT id, name, slug, district_id, category, latitude, longitude FROM places WHERE deleted_at IS NULL")
    active_places = cursor.fetchall()

print(f"Total active places in DB: {len(active_places)}")
assert len(active_places) == 98, f"Expected 98 active places, got {len(active_places)}"

active_slugs = set(p['slug'] for p in active_places)
active_names = set(p['name'].lower() for p in active_places)

# 2. Load remaining candidates from Phase 6 Factcheck (ranks 11 to 30)
with open('PHASE6_TOP30_FACTCHECK.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    phase6_candidates = list(reader)

# Exclude Batch 3 (ranks 1-10) and Buddha Relic Stupa (#19 HOLD)
remaining_pool = [c for c in phase6_candidates if int(c['rank']) > 10 and int(c['rank']) != 19]

print(f"Remaining candidates from Phase 6 Top 30 (excluding Batch 3 and #19 HOLD): {len(remaining_pool)}")

print("\n--- DISTANCE AUDIT AGAINST ALL 98 ACTIVE DB PLACES ---")
audit_results = []
for c in remaining_pool:
    c_lat = float(c['latitude'])
    c_lng = float(c['longitude'])
    c_name = c['place_name']
    c_dist = c['district']
    c_cat = c['category']
    
    # Calculate distances to all 98 active places
    distances = []
    for ap in active_places:
        ap_lat = float(ap['latitude'])
        ap_lng = float(ap['longitude'])
        d_km = haversine_km(c_lat, c_lng, ap_lat, ap_lng)
        distances.append((d_km, ap))
    
    distances.sort(key=lambda x: x[0])
    closest_km, closest_ap = distances[0]
    
    # Classification
    if closest_km < 1.0:
        flag = "HIGH OVERLAP RISK (<1km)"
    elif closest_km < 3.0:
        flag = "REVIEW (1-3km)"
    elif closest_km < 5.0:
        flag = "CHECK COMPLEX RELATION (3-5km)"
    else:
        flag = f"SAFE (>5km: {closest_km:.1f}km)"
        
    audit_results.append({
        'rank': c['rank'],
        'name': c_name,
        'district': c_dist,
        'category': c_cat,
        'lat': c_lat,
        'lng': c_lng,
        'closest_km': closest_km,
        'closest_place': closest_ap['name'],
        'closest_id': closest_ap['id'],
        'flag': flag,
        'raw_c': c
    })
    print(f"Rank {c['rank']:>2}: {c_name:42} ({c_dist:14}) | Closest: {closest_ap['name']} (ID {closest_ap['id']}) @ {closest_km:5.2f} km | {flag}")
