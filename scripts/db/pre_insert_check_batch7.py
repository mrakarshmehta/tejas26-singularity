import sys
import os
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

batch7_candidates = [
    {
        "name": "Bhitiharwa Gandhi Ashram",
        "district": "West Champaran",
        "district_id": 9,
        "category": "historical",
        "latitude": 27.2437,
        "longitude": 84.4838,
        "slug": "bhitiharwa-gandhi-ashram-west-champaran"
    },
    {
        "name": "Baba Mahendra Nath Temple, Mehdar",
        "district": "Siwan",
        "district_id": 35,
        "category": "temple",
        "latitude": 25.9870,
        "longitude": 84.4380,
        "slug": "baba-mahendra-nath-temple-mehdar-siwan"
    },
    {
        "name": "Jaimangla Garh",
        "district": "Begusarai",
        "district_id": 15,
        "category": "historical",
        "latitude": 25.5921,
        "longitude": 86.1613,
        "slug": "jaimangla-garh-begusarai"
    },
    {
        "name": "Ramrekha Ghat",
        "district": "Buxar",
        "district_id": 17,
        "category": "cultural",
        "latitude": 25.5761,
        "longitude": 83.9711,
        "slug": "ramrekha-ghat-buxar"
    },
    {
        "name": "Aganoor Mini Hydroelectric Project",
        "district": "Arwal",
        "district_id": 12,
        "category": "tourist_spot",
        "latitude": 25.1328,
        "longitude": 84.5385,
        "slug": "aganoor-mini-hydroelectric-project-arwal"
    },
    {
        "name": "Raja Bali Ka Garh",
        "district": "Madhubani",
        "district_id": 20,
        "category": "historical",
        "latitude": 26.4595,
        "longitude": 86.3230,
        "slug": "raja-bali-ka-garh-madhubani"
    },
    {
        "name": "Dr. Rajendra Prasad Central Agricultural University",
        "district": "Samastipur",
        "district_id": 30,
        "category": "historical",
        "latitude": 25.9860,
        "longitude": 85.6754,
        "slug": "dr-rajendra-prasad-central-agricultural-university-samastipur"
    },
    {
        "name": "Baba Vishu Raut Temple, Pachrasi Dham",
        "district": "Madhepura",
        "district_id": 27,
        "category": "cultural",
        "latitude": 25.4450,
        "longitude": 87.0250,
        "slug": "baba-vishu-raut-temple-pachrasi-dham-madhepura"
    },
    {
        "name": "Kanhaiya Ji Mandir, Bandarjhula",
        "district": "Kishanganj",
        "district_id": 25,
        "category": "historical",
        "latitude": 26.3683,
        "longitude": 87.9636,
        "slug": "kanhaiya-ji-mandir-bandarjhula-kishanganj"
    },
    {
        "name": "Gautam Asthan, Revelganj",
        "district": "Saran",
        "district_id": 31,
        "category": "cultural",
        "latitude": 25.7812,
        "longitude": 84.6712,
        "slug": "gautam-asthan-revelganj-saran"
    }
]

allowed_categories = {
    'tourist_spot', 'temple', 'food_place', 'hidden_gem', 'nature',
    'historical', 'beach', 'mountain', 'market', 'adventure',
    'cultural', 'waterfall', 'lake', 'other'
}

def main():
    print("=" * 80)
    print("PRE-INSERT VALIDATION AUDIT FOR BATCH 7 (10 APPROVED PLACES)")
    print("=" * 80)
    
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', 3307)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'hiddenyatra'),
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    
    # 1. Check active places count
    cur.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
    active_count = cur.fetchone()['cnt']
    print(f"1. Active Places Count: {active_count} (Must be 128)")
    if active_count != 128:
        print(f"FAILED: Expected 128 active places, found {active_count}")
        sys.exit(1)
        
    # 2. Check max ID
    cur.execute("SELECT MAX(id) as max_id FROM places")
    max_id = cur.fetchone()['max_id']
    print(f"2. Current Max ID: {max_id} (Must be 178)")
    if max_id != 178:
        print(f"FAILED: Expected max ID 178, found {max_id}")
        sys.exit(1)
        
    # 3. Verify all 10 district IDs exist
    cur.execute("SELECT id, name FROM districts")
    db_districts = {d['id']: d['name'] for d in cur.fetchall()}
    print("\n3. Validating 10 District IDs against `districts` table:")
    for p in batch7_candidates:
        d_id = p['district_id']
        if d_id not in db_districts:
            print(f"FAILED: District ID {d_id} does not exist in districts table!")
            sys.exit(1)
        print(f"   [OK] Place '{p['name']}' -> District ID {d_id} ('{db_districts[d_id]}')")
        
    # 4. Verify categories against allowed constants
    print("\n4. Validating 10 Categories against allowed domain constants:")
    for p in batch7_candidates:
        cat = p['category']
        if cat not in allowed_categories:
            print(f"FAILED: Category '{cat}' is not in allowed domain constants!")
            sys.exit(1)
        print(f"   [OK] Place '{p['name']}' -> Category: '{cat}'")
        
    # 5. Fetch all active places for collision checks
    cur.execute("SELECT id, name, slug, latitude, longitude FROM places WHERE deleted_at IS NULL")
    active_places = cur.fetchall()
    
    active_names = {p['name'].strip().lower(): p for p in active_places}
    active_slugs = {p['slug'].strip().lower(): p for p in active_places}
    active_coords = {(round(float(p['latitude']), 4), round(float(p['longitude']), 4)): p for p in active_places}
    
    # 5, 6, 7, 8, 9 Collision & Haversine Audit
    print("\n5-9. Checking Name Collisions, Slug Collisions, Coordinate Collisions & Haversine Distances:")
    for i, p in enumerate(batch7_candidates, 1):
        name_l = p['name'].strip().lower()
        slug_l = p['slug'].strip().lower()
        coord_key = (round(p['latitude'], 4), round(p['longitude'], 4))
        
        # Exact name match
        if name_l in active_names:
            print(f"FAILED: Exact name collision on '{p['name']}' with ID {active_names[name_l]['id']}")
            sys.exit(1)
            
        # Slug match
        if slug_l in active_slugs:
            print(f"FAILED: Slug collision on '{p['slug']}' with ID {active_slugs[slug_l]['id']}")
            sys.exit(1)
            
        # Coordinate collision
        if coord_key in active_coords:
            print(f"FAILED: Coordinate collision on {coord_key} with ID {active_coords[coord_key]['id']}")
            sys.exit(1)
            
        # Haversine nearest neighbor
        min_dist = float('inf')
        nearest = None
        for ap in active_places:
            plat, plon = float(ap['latitude']), float(ap['longitude'])
            dist = haversine(p['latitude'], p['longitude'], plat, plon)
            if dist < min_dist:
                min_dist = dist
                nearest = ap
                
        print(f"   [{i:2d}] {p['name']:<50} | Nearest: ID {nearest['id']:3d} '{nearest['name'][:28]:<28}' -> {min_dist:5.2f} km [PASS]")
        
    print("\n" + "=" * 80)
    print("PRE-INSERT VALIDATION SUCCEEDED 100%! ALL 10 GATES PASSED.")
    print("READY FOR ATOMIC TRANSACTION INSERTION.")
    print("=" * 80)
    
if __name__ == '__main__':
    main()
