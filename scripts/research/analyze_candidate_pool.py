import csv
import sys
import math
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 1. Load active 138 places
conn = get_db()
cur = conn.cursor()
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
""")
active_places = cur.fetchall()
active_names_lower = {p['name'].lower(): p for p in active_places}
active_slugs = {p['slug']: p for p in active_places}

print(f"Loaded {len(active_places)} active places from DB.")

# District counts
dist_counts = {}
for p in active_places:
    dist_counts[p['district_name']] = dist_counts.get(p['district_name'], 0) + 1

# Inspect candidates in queues
queues = ['PHASE6_TOP30_FACTCHECK.csv', 'BIHAR_PRIORITY_APPROVAL_QUEUE.csv', 'PHASE5_MASTER_CANDIDATE_QUEUE.csv']
seen_candidates = set()
candidate_pool = []

for qfile in queues:
    try:
        reader = list(csv.DictReader(open(qfile, encoding='utf-8')))
        for r in reader:
            name = r.get('name') or r.get('candidate_name') or r.get('place_name') or ''
            name = name.strip()
            if not name or name.lower() in seen_candidates:
                continue
            seen_candidates.add(name.lower())
            
            district = r.get('district') or r.get('district_name') or ''
            category = r.get('category') or ''
            lat = r.get('latitude') or r.get('lat') or ''
            lng = r.get('longitude') or r.get('lng') or ''
            
            # Check if already inserted (exact name match or slug match)
            is_inserted = False
            for ap in active_places:
                if name.lower() in ap['name'].lower() or ap['name'].lower() in name.lower():
                    # Check how close
                    is_inserted = True
                    break
            
            candidate_pool.append({
                'source_file': qfile,
                'name': name,
                'district': district,
                'category': category,
                'lat': lat,
                'lng': lng,
                'matched_active': is_inserted
            })
    except Exception as e:
        print(f"Error reading {qfile}: {e}")

print(f"Total unique candidates parsed from queues: {len(candidate_pool)}")
uninserted = [c for c in candidate_pool if not c['matched_active']]
print(f"Uninserted candidates: {len(uninserted)}")

# Group uninserted by district
by_dist = {}
for c in uninserted:
    d = c['district'] or 'Unknown'
    by_dist.setdefault(d, []).append(c)

print("\nDistricts with lowest current active place counts:")
low_districts = sorted(dist_counts.items(), key=lambda x: x[1])
for d, count in low_districts[:15]:
    cands = [c['name'] for c in by_dist.get(d, [])]
    print(f"  {d:<24} Current active: {count} | Queue candidates: {len(cands)} -> {cands[:3]}")
