import sys
import csv
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

# 10 approved candidates
approved_ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

with open('PHASE6_TOP30_FACTCHECK.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_candidates = {int(r['rank']): r for r in reader}

batch3_candidates = [all_candidates[r] for r in approved_ranks]

print("=== PRE-INSERT VALIDATION ===")
with get_cursor() as cursor:
    cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
    active_places = cursor.fetchone()['cnt']
    cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
    covered_districts = cursor.fetchone()['cnt']
    cursor.execute("SELECT MAX(id) as max_id FROM places")
    max_id = cursor.fetchone()['max_id']
    
    print(f"Pre-insert active places: {active_places} (Expected: 88)")
    print(f"Pre-insert covered districts: {covered_districts} (Expected: 38)")
    print(f"Current MAX(id): {max_id} (Expected: 138)")
    
    cursor.execute("SELECT name, slug, latitude, longitude FROM places WHERE deleted_at IS NULL")
    existing_places = cursor.fetchall()
    existing_slugs = set(p['slug'] for p in existing_places)
    existing_names = set(p['name'].lower() for p in existing_places)
    
    district_map = {
        'Madhubani': 20,
        'Rohtas': 8,
        'Bhagalpur': 5,
        'Araria': 11,
        'West Champaran': 9,
        'Nalanda': 3,
        'Darbhanga': 18,
        'East Champaran': 10,
        'Saran': 31
    }
    
    print("\nVerifying 10 Approved Batch 3 Candidates:")
    for c in batch3_candidates:
        rank = c['rank']
        name = c['place_name']
        dist = c['district']
        cat = c['category']
        lat = float(c['latitude'])
        lng = float(c['longitude'])
        dist_id = district_map[dist]
        
        # Check if already exists in DB
        assert name.lower() not in existing_names, f"Name already exists: {name}"
        
        # Determine slug
        slug = name.lower().replace('&', 'and').replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace('.', '')
        slug = '-'.join(slug.split()) + f"-{dist.lower().replace(' ', '-')}"
        assert slug not in existing_slugs, f"Slug collision: {slug}"
        
        print(f"Rank {rank:>2}: {name} ({dist} -> district_id: {dist_id}) | Cat: {cat} | Lat: {lat}, Lng: {lng} | Slug: {slug} | Status: VALID")

print("\nALL 10 CANDIDATES VERIFIED AND READY FOR ATOMIC TRANSACTION INSERTION.")
