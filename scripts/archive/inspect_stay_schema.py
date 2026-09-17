import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    for table in ['host_profiles', 'host_listings', 'listing_photos', 'stay_requests', 'users']:
        cur.execute(f'DESCRIBE {table}')
        print(f'\n=== {table} ===')
        for col in cur.fetchall():
            print(f"  {col['Field']:<24} {col['Type']:<20} Null={col['Null']} Key={col['Key']}")

    # Baseline counts
    print("\n=== CURRENT BASELINE COUNTS ===")
    for table in ['host_profiles', 'host_listings', 'listing_photos', 'stay_requests', 'users']:
        cur.execute(f'SELECT COUNT(*) as cnt FROM {table}')
        print(f"  {table}: {cur.fetchone()['cnt']} rows")

    # Current listings
    cur.execute("SELECT id, host_id, title, slug, stay_type, price_per_night, district_id, status, cover_image FROM host_listings")
    print("\n=== CURRENT HOST LISTINGS ===")
    for row in cur.fetchall():
        print(f"  ID {row['id']:2d}: {row['title']:<38} Type={row['stay_type']} Price={row['price_per_night']} Status={row['status']} District={row['district_id']} Cover={row['cover_image']}")
