import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    cur.execute("""
        SELECT hl.id, hl.host_id, hl.title, hl.slug, hl.listing_type, hl.price_per_night,
               hl.district_id, d.name AS district_name, hl.status, hl.cover_image,
               hp.user_id, u.username, u.display_name, hp.verification_status, hp.is_verified_badge
        FROM host_listings hl
        LEFT JOIN host_profiles hp ON hl.host_id = hp.id
        LEFT JOIN users u ON hp.user_id = u.id
        LEFT JOIN districts d ON hl.district_id = d.id
        ORDER BY hl.id ASC
    """)
    listings = cur.fetchall()
    print("=== ALL CURRENT HOST LISTINGS ===")
    for l in listings:
        print(f"ID {l['id']:2d}: '{l['title']}'")
        print(f"       Type={l['listing_type']}, Price=Rs.{l['price_per_night']}, Status={l['status']}")
        print(f"       District={l['district_name']} (ID {l['district_id']}), Host='{l['display_name']}' (ID {l['host_id']}), User='{l['username']}'")
        print(f"       Cover='{l['cover_image']}'")
        print()

    cur.execute("""
        SELECT hp.id, hp.user_id, u.username, u.display_name, u.email,
               hp.verification_status, hp.is_verified_badge, hp.district_id, d.name as district_name
        FROM host_profiles hp
        LEFT JOIN users u ON hp.user_id = u.id
        LEFT JOIN districts d ON hp.district_id = d.id
        ORDER BY hp.id ASC
    """)
    hosts = cur.fetchall()
    print("=== ALL CURRENT HOST PROFILES ===")
    for h in hosts:
        print(f"Host ID {h['id']:2d}: User ID={h['user_id']}, Username='{h['username']}', Name='{h['display_name']}', Status='{h['verification_status']}', Badge={h['is_verified_badge']}, District={h['district_name']}")
