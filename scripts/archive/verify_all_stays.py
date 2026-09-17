import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    cur.execute("""
        SELECT hl.id, hl.title, hl.slug, hl.listing_type, hl.price_per_night,
               hl.district_id, d.name AS district_name, hl.status, hl.cover_image,
               u.display_name AS host_name, hp.is_verified_badge, hp.avg_host_rating,
               (SELECT COUNT(*) FROM listing_photos lp WHERE lp.listing_id = hl.id) as gallery_photo_count
        FROM host_listings hl
        JOIN host_profiles hp ON hl.host_id = hp.id
        JOIN users u ON hp.user_id = u.id
        LEFT JOIN districts d ON hl.district_id = d.id
        WHERE hl.status = 'published'
        ORDER BY hl.id ASC
    """)
    listings = cur.fetchall()
    print(f"=== ALL PUBLISHED LISTINGS ({len(listings)} total) ===")
    for l in listings:
        price_str = f"Rs.{int(l['price_per_night'])}" if l['listing_type'] == 'paid_homestay' else 'FREE (Rs.0)'
        print(f"ID {l['id']:2d}: {l['title']:<40} | {price_str:<12} | District: {l['district_name']:<20} | Host: {l['host_name']} | Photos: {l['gallery_photo_count']}")
