import sys
import os
import csv
import math
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

with get_cursor() as cursor:
    cursor.execute("""
        SELECT d.id, d.name, COUNT(p.id) as place_count 
        FROM districts d 
        LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL 
        GROUP BY d.id, d.name 
        ORDER BY place_count ASC, d.name ASC
    """)
    rows = cursor.fetchall()

    cursor.execute("""
        SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name 
        FROM places p 
        JOIN districts d ON p.district_id = d.id 
        WHERE p.deleted_at IS NULL 
        ORDER BY p.id
    """)
    active_places = cursor.fetchall()

print("=== DISTRICT PLACE COUNTS IN ACTIVE DB (118 TOTAL) ===")
one_place = [r for r in rows if r['place_count'] == 1]
two_place = [r for r in rows if r['place_count'] == 2]
three_plus = [r for r in rows if r['place_count'] >= 3]

print(f"Districts with 1 place ({len(one_place)}): {[r['name'] for r in one_place]}")
print(f"Districts with 2 places ({len(two_place)}): {[r['name'] for r in two_place]}")
print(f"Districts with >=3 places ({len(three_plus)}): {[r['name'] + ' (' + str(r['place_count']) + ')' for r in three_plus]}")

# Load all candidates from master queue and priority queue
with open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', mode='r', encoding='utf-8') as f:
    master = list(csv.DictReader(f))

with open('BIHAR_PRIORITY_APPROVAL_QUEUE.csv', mode='r', encoding='utf-8') as f:
    priority = list(csv.DictReader(f))

# Collect candidates from 1-place and 2-place districts
print("\n=== CANDIDATES IN 1-PLACE DISTRICTS ===")
for r in one_place:
    dist_name = r['name']
    cands_m = [c for c in master if c['district'].lower() == dist_name.lower()]
    cands_p = [c for c in priority if c['district'].lower() == dist_name.lower()]
    print(f"\nDistrict: {dist_name} (Current active: 1)")
    seen = set()
    for c in cands_m:
        name = c['place_name']
        if name in seen: continue
        seen.add(name)
        # check distance to existing place in this district
        coords = c['coordinates'].split(',')
        min_d = 999
        np = ""
        if len(coords) >= 2:
            try:
                clat, clng = float(coords[0]), float(coords[1])
                for p in active_places:
                    d = haversine(clat, clng, float(p['latitude']), float(p['longitude']))
                    if d < min_d:
                        min_d = d
                        np = p['name']
            except: pass
        print(f"  - [Master/{c['recommended_priority']}] {name} | Cat: {c['category']} | Nearest: {np} ({min_d:.2f} km) | Source: {c['primary_source']}")

