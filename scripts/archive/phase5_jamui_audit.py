"""
Phase 5 Jamui Data Recovery Audit - 100% Read-Only.
Verifies all Jamui places, blocks, services, descriptions, images and food items.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

print("=== 1. ALL PLACES RELATED TO JAMUI IN DATABASE ===")
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, p.district_id, p.cover_image, p.latitude, p.longitude,
           p.description, p.history, p.travel_tips, p.deleted_at,
           d.name AS current_district_name, d.slug AS current_district_slug
    FROM places p
    LEFT JOIN districts d ON p.district_id = d.id
    WHERE p.district_id = 22 
       OR p.district_id = 4
       OR p.name LIKE '%Jamui%'
       OR p.slug LIKE '%jamui%'
       OR p.name IN ('Giddheswar Temple', 'Patneshwar Mandir', 'Simultala Hill Station',
                     'Kali Mandir, Malaypur', 'Minto Tower, Gidhaur', 'Maa Netula Temple',
                     'Lachhuar Jain Temple', 'Bhim Bandh Hot Springs', 'Nagi Dam Bird Sanctuary',
                     'Kshatriya Kund', 'Nakti Dam Bird Sanctuary', 'Gidhaur Raj Palace',
                     'Garhi Reservoir & Dam', 'Indrape Hill', 'Dharhara Waterfall',
                     'Laka Ring Dam & Eco Park', 'Chateshwar Nath Temple, Kakwara',
                     'Simultala Waterfall')
    ORDER BY p.id
""")
jamui_places = cur.fetchall()
print(f"Total Jamui-related places found in DB: {len(jamui_places)}")
for p in jamui_places:
    del_flag = " [SOFT DELETED]" if p['deleted_at'] else ""
    print(f"  - Place ID {p['id']:3d}: '{p['name']}' (slug: {p['slug']}) | Cat: {p['category']:12s} | DID: {p['district_id']} ({p['current_district_name']}){del_flag}")
    print(f"    Image: {p['cover_image'][:60] if p['cover_image'] else 'None'}")
    print(f"    Desc: {p['description'][:80]}...")

print("\n=== 2. ALL BLOCKS RELATED TO JAMUI IN DATABASE ===")
cur.execute("""
    SELECT b.id, b.district_id, b.name, b.slug,
           d.name AS dist_name, d.slug AS dist_slug
    FROM blocks b
    LEFT JOIN districts d ON b.district_id = d.id
    WHERE b.district_id = 22 OR b.district_id = 4 OR b.name LIKE '%Jamui%'
    ORDER BY b.id
""")
jamui_blocks = cur.fetchall()
print(f"Total blocks currently linked to ID 22 or ID 4: {len(jamui_blocks)}")
for b in jamui_blocks:
    print(f"  - Block ID {b['id']:3d}: '{b['name']}' (slug: {b['slug']}) | Linked to DID: {b['district_id']} ({b['dist_name']})")

print("\n=== 3. ALL SERVICES RELATED TO JAMUI IN DATABASE ===")
cur.execute("""
    SELECT s.*,
           d.name AS dist_name, d.slug AS dist_slug
    FROM nearby_services s
    LEFT JOIN districts d ON s.district_id = d.id
    WHERE s.district_id = 22 OR s.name LIKE '%Jamui%'
    ORDER BY s.id
""")
jamui_services = cur.fetchall()
print(f"Total services related to Jamui: {len(jamui_services)}")
for s in jamui_services:
    print(f"  - Service ID {s['id']:3d}: '{s['name']}' | Type: {s['service_type']:15s} | DID: {s['district_id']} ({s['dist_name']}) | Addr: {s['address'][:50] if s['address'] else ''}")

print("\n=== 4. ALL HOST LISTINGS FOR JAMUI ===")
cur.execute("""
    SELECT hl.id, hl.title, hl.slug, hl.district_id, hl.address_text,
           d.name AS dist_name
    FROM host_listings hl
    LEFT JOIN districts d ON hl.district_id = d.id
    WHERE hl.district_id = 4 OR hl.district_id = 22 OR hl.title LIKE '%Jamui%' OR hl.title LIKE '%Simultala%'
""")
for hl in cur.fetchall():
    print(f"  - Listing ID {hl['id']}: '{hl['title']}' | DID: {hl['district_id']} ({hl['dist_name']}) | Addr: {hl['address_text']}")

cur.close()
conn.close()
