import sys
import os
import csv
import math
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
print(f"Total active places: {len(active_places)}")

# 2. District counts
cur.execute("""
    SELECT d.id, d.name, COUNT(p.id) as count
    FROM districts d
    LEFT JOIN places p ON d.id = p.district_id AND p.deleted_at IS NULL
    GROUP BY d.id, d.name
    ORDER BY count ASC, d.name ASC
""")
dist_counts = cur.fetchall()
print("\n--- Current District Counts (Active 128) ---")
for d in dist_counts:
    print(f"District {d['id']:2d}: {d['name']:<18} = {d['count']}")

# 3. Read queues and gather all candidates
candidates = []
seen_names = set()

# Read PHASE5_MASTER_CANDIDATE_QUEUE.csv
if os.path.exists('PHASE5_MASTER_CANDIDATE_QUEUE.csv'):
    with open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            candidates.append({
                'source_file': 'PHASE5_MASTER',
                'name': r.get('place_name', '').strip(),
                'district': r.get('district', '').strip(),
                'category': r.get('category', '').strip(),
                'coords': r.get('coordinates', '').strip(),
                'verification': r.get('verification_level', '').strip(),
                'primary_source': r.get('primary_source', '').strip(),
                'secondary_source': r.get('secondary_source', '').strip(),
                'recommended_priority': r.get('recommended_priority', '').strip(),
                'reason': r.get('reason', '').strip(),
                'why': r.get('tourism_value', '').strip()
            })

print(f"\nTotal loaded candidates from PHASE5_MASTER: {len(candidates)}")
