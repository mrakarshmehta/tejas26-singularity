import sys
import os
import math
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor, get_db

sys.stdout.reconfigure(encoding='utf-8')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

batch6_candidates = [
    {
        "rank": 1,
        "name": "Kahalgaon Rock-Cut Temples",
        "district": "Bhagalpur",
        "district_id": 5,
        "category": "historical",
        "lat": 25.2689,
        "lng": 87.2345,
        "slug": "kahalgaon-rock-cut-temples-bhagalpur"
    },
    {
        "rank": 2,
        "name": "Vishwa Shanti Stupa & Ratnagiri Ropeway",
        "district": "Nalanda",
        "district_id": 3,
        "category": "cultural",
        "lat": 25.0085,
        "lng": 85.4385,
        "slug": "vishwa-shanti-stupa-and-ratnagiri-ropeway-nalanda"
    },
    {
        "rank": 3,
        "name": "Shringirishi Dham",
        "district": "Lakhisarai",
        "district_id": 26,
        "category": "nature",
        "lat": 25.1278,
        "lng": 86.2344,
        "slug": "shringirishi-dham-lakhisarai"
    },
    {
        "rank": 4,
        "name": "Girihinda Pahar & Shiv Temple",
        "district": "Sheikhpura",
        "district_id": 32,
        "category": "mountain",
        "lat": 25.1385,
        "lng": 85.8562,
        "slug": "girihinda-pahar-and-shiv-temple-sheikhpura"
    },
    {
        "rank": 5,
        "name": "Matsyagandha Lake & Raktakali Temple",
        "district": "Saharsa",
        "district_id": 29,
        "category": "lake",
        "lat": 25.8825,
        "lng": 86.5985,
        "slug": "matsyagandha-lake-and-raktakali-temple-saharsa"
    },
    {
        "rank": 6,
        "name": "Kajha Kothi Eco Park",
        "district": "Purnia",
        "district_id": 28,
        "category": "nature",
        "lat": 25.7185,
        "lng": 87.3512,
        "slug": "kajha-kothi-eco-park-purnia"
    },
    {
        "rank": 7,
        "name": "Guru Tegh Bahadur Historic Gurdwara, Lakshmipur",
        "district": "Katihar",
        "district_id": 23,
        "category": "cultural",
        "lat": 25.3912,
        "lng": 87.2812,
        "slug": "guru-tegh-bahadur-historic-gurdwara-lakshmipur-katihar"
    },
    {
        "rank": 8,
        "name": "Dighwa Dubauli Archaeological Mounds",
        "district": "Gopalganj",
        "district_id": 19,
        "category": "historical",
        "lat": 26.2485,
        "lng": 84.7312,
        "slug": "dighwa-dubauli-archaeological-mounds-gopalganj"
    },
    {
        "rank": 9,
        "name": "Champanagar Ancient Capital & Jain Tirth",
        "district": "Bhagalpur",
        "district_id": 5,
        "category": "cultural",
        "lat": 25.2312,
        "lng": 86.9245,
        "slug": "champanagar-ancient-capital-and-jain-tirth-bhagalpur"
    },
    {
        "rank": 10,
        "name": "Deokund",
        "district": "Aurangabad",
        "district_id": 13,
        "category": "temple",
        "lat": 24.9512,
        "lng": 84.5829,
        "slug": "deokund-aurangabad"
    }
]

def main():
    print("================================================================================")
    print("HIDDENYATRA — BATCH 6 PRE-INSERT VALIDATION AUDIT")
    print("================================================================================")
    
    with get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        total_active = cursor.fetchone()['cnt']
        print(f"1. Baseline Active Places Count: {total_active} (Expected: 118)")
        assert total_active == 118, f"ABORT: Active places count is {total_active}, expected 118!"

        cursor.execute("SELECT MAX(id) as max_id FROM places WHERE deleted_at IS NULL")
        max_id = cursor.fetchone()['max_id']
        print(f"2. Current Max Place ID: {max_id} (Expected: 168)")
        assert max_id == 168, f"ABORT: Max place ID is {max_id}, expected 168!"

        cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        districts_covered = cursor.fetchone()['cnt']
        print(f"3. Districts Covered: {districts_covered}/38")
        assert districts_covered == 38, f"ABORT: Districts covered is {districts_covered}, expected 38!"

        # Fetch all active places for collision analysis
        cursor.execute("""
            SELECT id, name, slug, category, latitude, longitude, district_id 
            FROM places 
            WHERE deleted_at IS NULL 
            ORDER BY id
        """)
        active_places = cursor.fetchall()
        
        # Fetch districts
        cursor.execute("SELECT id, name FROM districts")
        district_map = {d['id']: d['name'] for d in cursor.fetchall()}

    # Allowed categories
    allowed_categories = {'tourist_spot', 'temple', 'food_place', 'hidden_gem', 'nature', 'historical', 'beach', 'mountain', 'market', 'adventure', 'cultural', 'waterfall', 'lake', 'other'}

    print("\n4. Candidate-by-Candidate Verification:")
    print("--------------------------------------------------------------------------------")
    print(f"{'#':<3} | {'Candidate Name':<42} | {'District':<12} | {'Cat':<10} | {'Nearest Place':<30} | {'Dist (km)':<9} | {'Status'}")
    print("--------------------------------------------------------------------------------")

    for c in batch6_candidates:
        # Check district_id
        assert c['district_id'] in district_map, f"Invalid district_id {c['district_id']}"
        assert district_map[c['district_id']].lower() == c['district'].lower(), f"District ID mismatch for {c['name']}"
        
        # Check category
        assert c['category'] in allowed_categories, f"Invalid category {c['category']}"

        # Collision detection against 118 places
        nearest_d = 9999.0
        nearest_p = None

        for p in active_places:
            # Exact name
            if c['name'].lower() == p['name'].lower():
                raise AssertionError(f"FATAL: Exact name match found in DB: {p['name']} (ID {p['id']})")
            
            # Slug collision
            if c['slug'] == p['slug']:
                raise AssertionError(f"FATAL: Slug collision found in DB: {p['slug']} (ID {p['id']})")

            # Exact coordinate collision (to 4 decimal places)
            if round(c['lat'], 4) == round(float(p['latitude']), 4) and round(c['lng'], 4) == round(float(p['longitude']), 4):
                raise AssertionError(f"FATAL: Exact coordinate collision with {p['name']} (ID {p['id']}) at {c['lat']},{c['lng']}")

            # Haversine distance
            d = haversine(c['lat'], c['lng'], float(p['latitude']), float(p['longitude']))
            if d < nearest_d:
                nearest_d = d
                nearest_p = p

        c['min_dist'] = nearest_d
        c['nearest_name'] = nearest_p['name']
        c['nearest_id'] = nearest_p['id']

        print(f"{c['rank']:<3} | {c['name']:<42} | {c['district']:<12} | {c['category']:<10} | {c['nearest_name'][:28]:<30} | {c['min_dist']:>7.2f} km | PASSED [OK]")

    print("--------------------------------------------------------------------------------")
    print("\nPRE-INSERT INTEGRITY CHECK PASSED: ALL 10 CANDIDATES VERIFIED & ZERO CONFLICTS FOUND.")
    print("Ready for Atomic Insertion.\n")

if __name__ == "__main__":
    main()
