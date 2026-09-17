"""
Generate static/data/bihar/hotels.geojson and static/data/bihar/homestays.geojson from MySQL.
Applies strict privacy filtering: NO private host phone, email, ID hash, emergency phone, or full address.
"""

import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))
from models.connection import get_db

def build_hotels_geojson():
    print("\n--- Generating Hotels GeoJSON ---")
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT ns.id, ns.name, ns.service_type, ns.address, ns.phone,
                   ns.latitude, ns.longitude,
                   d.id as district_id, d.name as district_name, d.slug as district_slug
            FROM nearby_services ns
            LEFT JOIN districts d ON ns.district_id = d.id
            WHERE LOWER(ns.service_type) = 'hotel'
              AND ns.is_active = 1
              AND ns.latitude IS NOT NULL
              AND ns.longitude IS NOT NULL
            ORDER BY d.id, ns.id
        """)
        hotels = cursor.fetchall()

    print(f"Total active hotels with coordinates: {len(hotels)}")
    features = []
    for h in hotels:
        lat = float(h['latitude'])
        lng = float(h['longitude'])
        features.append({
            "type": "Feature",
            "properties": {
                "id": h['id'],
                "name": h['name'],
                "district_id": h['district_id'],
                "district_name": h['district_name'],
                "district_slug": h['district_slug'],
                "address": h['address'] or '',
                "phone": h['phone'] or '',
                "source": "HiddenYatra",
                "source_table": "nearby_services"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [round(lng, 6), round(lat, 6)]
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "name": "Bihar Hotels & Lodging",
            "source": "HiddenYatra Database (nearby_services)",
            "total_features": len(features),
            "timestamp": "2026-08-16T18:36:00Z"
        },
        "features": features
    }

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'bihar', 'hotels.geojson'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(features)} hotels to {out_path} ({os.path.getsize(out_path)/1024:.2f} KB)")
    return len(features)


def build_homestays_geojson():
    print("\n--- Generating Homestays GeoJSON ---")
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT l.id, l.title, l.slug, l.listing_type, l.property_type,
                   l.district_id, d.name as district_name, d.slug as district_slug,
                   l.latitude, l.longitude, l.price_per_night, l.currency,
                   l.cover_image, l.avg_rating, l.review_count, l.status
            FROM host_listings l
            LEFT JOIN districts d ON l.district_id = d.id
            WHERE l.status = 'published'
              AND l.latitude IS NOT NULL
              AND l.longitude IS NOT NULL
            ORDER BY d.id, l.id
        """)
        homestays = cursor.fetchall()

    print(f"Total published homestays with coordinates: {len(homestays)}")
    features = []
    for s in homestays:
        lat = float(s['latitude'])
        lng = float(s['longitude'])
        price = float(s['price_per_night']) if s['price_per_night'] is not None else 0.0
        rating = float(s['avg_rating']) if s['avg_rating'] is not None else 5.0
        rev_count = int(s['review_count']) if s['review_count'] is not None else 0

        features.append({
            "type": "Feature",
            "properties": {
                "id": s['id'],
                "title": s['title'],
                "slug": s['slug'],
                "district_id": s['district_id'],
                "district_name": s['district_name'],
                "district_slug": s['district_slug'],
                "listing_type": s['listing_type'],
                "property_type": s['property_type'] or 'homestay',
                "price_per_night": price,
                "currency": s['currency'] or 'INR',
                "cover_image": s['cover_image'] or '',
                "avg_rating": rating,
                "review_count": rev_count,
                "detail_url": f"/stays/{s['slug']}",
                "source": "HiddenYatra",
                "source_table": "host_listings"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [round(lng, 6), round(lat, 6)]
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "name": "Bihar Homestays & Eco Stays",
            "source": "HiddenYatra Database (host_listings)",
            "total_features": len(features),
            "timestamp": "2026-08-16T18:36:00Z"
        },
        "features": features
    }

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'bihar', 'homestays.geojson'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(features)} homestays to {out_path} ({os.path.getsize(out_path)/1024:.2f} KB)")
    return len(features)


if __name__ == "__main__":
    h_count = build_hotels_geojson()
    s_count = build_homestays_geojson()
    print("\n" + "=" * 60)
    print(f"  Summary: Hotels={h_count} (Expected: 12), Homestays={s_count} (Expected: 10)")
    print("=" * 60)
