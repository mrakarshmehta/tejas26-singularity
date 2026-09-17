"""
Deep inspection of host_listings and places (hotels/homestays).
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

def inspect_listings():
    with get_db() as db:
        cursor = db.cursor()

        print("=== Table: host_listings ===")
        cursor.execute("DESCRIBE host_listings")
        for col in cursor.fetchall():
            print(f"  {col['Field']} ({col['Type']}) Nullable={col['Null']} Key={col['Key']}")

        cursor.execute("""
            SELECT l.id, l.host_id, l.title, l.slug, l.listing_type, l.property_type,
                   l.district_id, d.name as district_name,
                   l.latitude, l.longitude, l.price_per_night, l.status,
                   l.cover_image, l.is_featured, l.avg_rating, l.review_count
            FROM host_listings l
            LEFT JOIN districts d ON l.district_id = d.id
            ORDER BY l.id
        """)
        listings = cursor.fetchall()
        print(f"\nTotal Host Listings: {len(listings)}")
        print("\nListing breakdown by status and listing_type:")
        status_counts = {}
        for l in listings:
            k = (l['status'], l['listing_type'])
            status_counts[k] = status_counts.get(k, 0) + 1
        for k, v in status_counts.items():
            print(f"  - Status: {k[0]}, Type: {k[1]} -> Count: {v}")

        print("\nActive/Published Listings Detail:")
        for l in listings:
            print(f"  ID {l['id']}: '{l['title']}' | Type: {l['listing_type']} | Prop: {l['property_type']} | Dist: {l['district_name']} | Lat/Lng: ({l['latitude']}, {l['longitude']}) | Status: {l['status']} | Price: ₹{l['price_per_night']}")

        # Check places for hotels
        print("\n=== Places with Category related to Accommodation/Hotel ===")
        cursor.execute("""
            SELECT id, name, slug, category, district_id, latitude, longitude, rating, review_count
            FROM places
            WHERE LOWER(category) LIKE '%hotel%'
               OR LOWER(category) LIKE '%stay%'
               OR LOWER(category) LIKE '%resort%'
               OR LOWER(category) LIKE '%guest%'
               OR LOWER(category) LIKE '%homestay%'
               OR LOWER(category) LIKE '%lodge%'
               OR LOWER(name) LIKE '%hotel%'
               OR LOWER(name) LIKE '%resort%'
               OR LOWER(name) LIKE '%bhawan%'
               OR LOWER(name) LIKE '%ashram%'
               OR LOWER(name) LIKE '%dharamshala%'
        """)
        hotel_places = cursor.fetchall()
        print(f"Hotel-like places found in `places`: {len(hotel_places)}")
        for p in hotel_places:
            print(f"  Place ID {p['id']}: '{p['name']}' (Category: {p['category']}, Dist ID: {p['district_id']}, Coords: {p['latitude']}, {p['longitude']})")

if __name__ == "__main__":
    inspect_listings()
