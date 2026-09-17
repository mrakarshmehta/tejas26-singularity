import sys
import os
import csv
import math
import re
import pymysql
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

conn = pymysql.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    port=int(os.getenv('DB_PORT', 3307)),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'hiddenyatra'),
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()

# 1. Fetch active places
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name
    FROM places p
    JOIN districts d ON p.district_id = d.id
    WHERE p.deleted_at IS NULL
    ORDER BY p.id ASC
""")
active_places = cur.fetchall()
print(f"Total active places in DB: {len(active_places)}")

# Map active places by lower name, words, and slugs
active_by_name = {p['name'].strip().lower(): p for p in active_places}
active_by_slug = {p['slug'].strip().lower(): p for p in active_places}

# Helper to normalize place name for matching
def normalize(name):
    s = name.lower()
    s = re.sub(r'[^\w\s]', ' ', s)
    tokens = [w for w in s.split() if w not in ['the', 'and', 'or', 'of', 'in', 'at', 'temple', 'mandir', 'fort', 'sanctuary', 'lake', 'caves', 'cave', 'stupa', 'ashram', 'ghat', 'dam', 'falls', 'waterfall', 'park', 'bihar']]
    return set(tokens)

# Find nearest active place
def find_nearest_active(lat, lon):
    min_dist = float('inf')
    nearest = None
    for p in active_places:
        plat, plon = float(p['latitude']), float(p['longitude'])
        dist = haversine(lat, lon, plat, plon)
        if dist < min_dist:
            min_dist = dist
            nearest = p
    return nearest, min_dist

# Read all candidates across files
inventory = {}

def add_candidate(cand_name, district, category, coords_str, source_file, prio, extra):
    key = cand_name.strip().lower()
    # clean key
    if not key:
        return
    if key not in inventory:
        inventory[key] = {
            'name': cand_name.strip(),
            'district': district.strip(),
            'category': category.strip(),
            'coords_str': coords_str.strip(),
            'sources': set([source_file]),
            'priorities': set([prio]) if prio else set(),
            'extra': extra
        }
    else:
        inventory[key]['sources'].add(source_file)
        if prio:
            inventory[key]['priorities'].add(prio)
        if not inventory[key]['coords_str'] and coords_str:
            inventory[key]['coords_str'] = coords_str.strip()

# 1. PHASE5_MASTER_CANDIDATE_QUEUE.csv
if os.path.exists('PHASE5_MASTER_CANDIDATE_QUEUE.csv'):
    with open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            add_candidate(
                r.get('place_name', ''),
                r.get('district', ''),
                r.get('category', ''),
                r.get('coordinates', ''),
                'PHASE5_MASTER',
                r.get('recommended_priority', ''),
                r
            )

# 2. BIHAR_PRIORITY_APPROVAL_QUEUE.csv
if os.path.exists('BIHAR_PRIORITY_APPROVAL_QUEUE.csv'):
    with open('BIHAR_PRIORITY_APPROVAL_QUEUE.csv', 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            add_candidate(
                r.get('place_name', ''),
                r.get('district', ''),
                r.get('category', ''),
                '',
                'BIHAR_PRIORITY_QUEUE',
                r.get('priority', ''),
                r
            )

# 3. PHASE6_TOP30_FACTCHECK.csv
if os.path.exists('PHASE6_TOP30_FACTCHECK.csv'):
    with open('PHASE6_TOP30_FACTCHECK.csv', 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            lat = r.get('latitude', '')
            lng = r.get('longitude', '')
            coords = f"{lat}, {lng}" if lat and lng else ""
            add_candidate(
                r.get('place_name', ''),
                r.get('district', ''),
                r.get('category', ''),
                coords,
                'PHASE6_TOP30',
                r.get('final_verdict', ''),
                r
            )

print(f"Total unique candidate names collected: {len(inventory)}")

# Classify each candidate against the 128 active places
results = []
for key, c in inventory.items():
    name = c['name']
    name_lower = name.lower()
    
    # Check exact match
    exact_match = None
    if name_lower in active_by_name:
        exact_match = active_by_name[name_lower]
    
    # Check substring / alias match
    alias_match = None
    c_tokens = normalize(name)
    for p in active_places:
        p_name_lower = p['name'].lower()
        if name_lower == p_name_lower:
            exact_match = p
            break
        p_tokens = normalize(p['name'])
        # check Jaccard or subset
        if c_tokens and p_tokens and (c_tokens.issubset(p_tokens) or p_tokens.issubset(c_tokens) or (len(c_tokens & p_tokens) >= 2 and len(c_tokens & p_tokens) / max(len(c_tokens), len(p_tokens)) > 0.6)):
            alias_match = p
    
    # Parse coords if available
    lat, lng = None, None
    if c['coords_str']:
        m = re.findall(r'[-+]?\d*\.\d+|\d+', c['coords_str'])
        if len(m) >= 2:
            try:
                lat, lng = float(m[0]), float(m[1])
            except:
                pass
    
    nearest_p = None
    min_dist = 9999.0
    if lat and lng:
        nearest_p, min_dist = find_nearest_active(lat, lng)
    
    # Status determination
    status = "UNKNOWN"
    reason = ""
    
    if exact_match:
        status = "ALREADY_INSERTED"
        reason = f"Exact match with active place ID {exact_match['id']}: '{exact_match['name']}'"
    elif alias_match and (min_dist < 2.0 or not lat):
        status = "DUPLICATE_ALIAS"
        reason = f"Alias/duplicate of active place ID {alias_match['id']}: '{alias_match['name']}'"
    elif "vaishali" in name_lower and "relic" in name_lower and "stupa" in name_lower:
        status = "HOLD"
        reason = "0.93 km from Vaishali - Birthplace of Democracy (ID 10). Relic casket already at Patna Museum; site in same complex."
    elif min_dist < 1.0 and nearest_p:
        status = "SAME_SITE"
        reason = f"Same-site component: {min_dist:.2f} km from active place ID {nearest_p['id']}: '{nearest_p['name']}'"
    elif "rejected" in str(c['extra']).lower():
        status = "REJECTED"
        reason = "Previously rejected due to low tourism value or lack of authoritative verification"
    else:
        status = "VALID_CANDIDATE"
        reason = f"Distinct candidate. Nearest active: {nearest_p['name'] if nearest_p else 'N/A'} ({min_dist:.2f} km)"
    
    results.append({
        'name': name,
        'district': c['district'],
        'category': c['category'],
        'lat': lat,
        'lng': lng,
        'status': status,
        'nearest': nearest_p['name'] if nearest_p else 'N/A',
        'dist': min_dist,
        'sources': list(c['sources']),
        'priorities': list(c['priorities']),
        'reason': reason,
        'extra': c['extra']
    })

# Print breakdown of statuses
status_counts = {}
for r in results:
    s = r['status']
    status_counts[s] = status_counts.get(s, 0) + 1

print("\n--- Status Counts of Candidates ---")
for s, cnt in status_counts.items():
    print(f"{s}: {cnt}")

print("\n--- Top VALID_CANDIDATEs with coords and distance ---")
valid_candidates = [r for r in results if r['status'] == 'VALID_CANDIDATE']
# Sort by distance or priority
valid_candidates.sort(key=lambda x: (x['district'], x['name']))
print(f"Total valid candidates: {len(valid_candidates)}")
for vc in valid_candidates[:30]:
    coords_str = f"{vc['lat']:.4f}, {vc['lng']:.4f}" if vc['lat'] else "No coords"
    print(f"[{vc['district']}] {vc['name']} | Cat: {vc['category']} | Coords: {coords_str} | Nearest: {vc['nearest']} ({vc['dist']:.1f}km) | Sources: {vc['sources']}")
