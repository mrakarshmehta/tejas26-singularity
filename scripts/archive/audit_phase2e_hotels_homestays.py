"""
Comprehensive read-only audit for Phase 2E: Hotels and Homestays in HiddenYatra.
"""

import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))
from models.connection import get_db

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def audit():
    print("=" * 70)
    print("  PHASE 2E COMPREHENSIVE READ-ONLY AUDIT: HOTELS & HOMESTAYS")
    print("=" * 70)

    with get_db() as db:
        cursor = db.cursor()

        # 1. HOMESTAYS AUDIT (host_listings & host_profiles)
        print("\n--- 1. HOMESTAYS AUDIT (`host_listings`) ---")
        cursor.execute("""
            SELECT l.id, l.host_id, l.title, l.slug, l.listing_type, l.property_type,
                   l.district_id, d.name as district_name, d.slug as district_slug,
                   l.block_id, b.name as block_name,
                   l.latitude, l.longitude, l.price_per_night, l.currency,
                   l.max_guests, l.num_rooms, l.num_beds, l.num_bathrooms,
                   l.cover_image, l.status, l.is_featured, l.avg_rating, l.review_count,
                   l.created_at,
                   u.display_name as host_display_name, u.full_name as host_full_name,
                   u.email as host_email, u.phone as host_phone,
                   hp.verification_status, hp.is_verified_badge
            FROM host_listings l
            LEFT JOIN districts d ON l.district_id = d.id
            LEFT JOIN blocks b ON l.block_id = b.id
            LEFT JOIN users u ON l.host_id = u.id
            LEFT JOIN host_profiles hp ON l.host_id = hp.user_id
            ORDER BY l.id
        """)
        all_listings = cursor.fetchall()
        print(f"Total host_listings records: {len(all_listings)}")

        published_listings = [l for l in all_listings if l['status'] == 'published']
        draft_listings = [l for l in all_listings if l['status'] != 'published']
        with_coords = [l for l in published_listings if l['latitude'] is not None and l['longitude'] is not None]
        without_coords = [l for l in published_listings if l['latitude'] is None or l['longitude'] is None]

        print(f"  Published listings: {len(published_listings)}")
        print(f"  Draft/other status listings: {len(draft_listings)}")
        print(f"  Published with valid coordinates: {len(with_coords)}")
        print(f"  Published with missing coordinates: {len(without_coords)}")

        print("\n  Published Homestays with Coordinates (Map Candidates):")
        for l in with_coords:
            img = l['cover_image'] or 'None'
            print(f"    - ID {l['id']}: '{l['title']}' | Type: {l['listing_type']} ({l['property_type']}) | Dist: {l['district_name']} | Coords: ({float(l['latitude']):.5f}, {float(l['longitude']):.5f}) | Price: ₹{l['price_per_night']} | Img: {img}")

        if without_coords:
            print("\n  Published Homestays WITHOUT Coordinates (Missing):")
            for l in without_coords:
                print(f"    - ID {l['id']}: '{l['title']}' | Dist: {l['district_name']} | Status: {l['status']}")

        # 2. HOTELS AUDIT
        print("\n--- 2. HOTELS AUDIT (`places` and other tables) ---")
        cursor.execute("""
            SELECT id, name, slug, category, district_id, latitude, longitude, cover_image, is_featured, is_hidden_gem
            FROM places
            WHERE LOWER(category) IN ('hotel', 'resort', 'stay', 'homestay', 'accommodation', 'hospitality', 'lodging')
               OR LOWER(name) LIKE '%hotel%'
               OR LOWER(name) LIKE '%resort%'
               OR LOWER(name) LIKE '%bhawan%'
               OR LOWER(name) LIKE '%ashram%'
               OR LOWER(name) LIKE '%dharamshala%'
               OR LOWER(name) LIKE '%guest house%'
            ORDER BY id
        """)
        places_hotel_like = cursor.fetchall()
        print(f"Total hotel-like places in `places` table: {len(places_hotel_like)}")
        for p in places_hotel_like:
            print(f"    - ID {p['id']}: '{p['name']}' | Cat: {p['category']} | Coords: ({p['latitude']}, {p['longitude']})")

        cursor.execute("SELECT DISTINCT category FROM places ORDER BY category")
        all_place_cats = [r['category'] for r in cursor.fetchall()]
        print(f"\nAll distinct categories in `places` table ({len(all_place_cats)}):")
        print(f"    {all_place_cats}")

        # Check for any other tables containing hotel data
        cursor.execute("SHOW TABLES")
        tables = [list(r.values())[0] for r in cursor.fetchall()]
        print(f"\nAll DB tables check: {tables}")

if __name__ == "__main__":
    audit()
