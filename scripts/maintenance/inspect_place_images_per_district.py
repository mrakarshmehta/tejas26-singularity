import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor
import os

with get_cursor() as cur:
    cur.execute("""
        SELECT p.id, p.name, p.district_id, d.name AS district_name, p.cover_image
        FROM places p
        JOIN districts d ON d.id = p.district_id
        WHERE p.deleted_at IS NULL
        ORDER BY p.district_id, p.id
    """)
    places = cur.fetchall()

print(f"Total active places: {len(places)}")
by_district = {}
for p in places:
    did = p['district_id']
    dname = p['district_name']
    cover = p['cover_image'] or ''
    exists = False
    if cover.startswith(('http://', 'https://')):
        exists = True
    elif cover:
        exists = os.path.exists(os.path.join('static', 'uploads', 'places', cover))
    
    if did not in by_district:
        by_district[did] = {'name': dname, 'valid_place_images': [], 'invalid_place_images': []}
    
    if exists and cover:
        by_district[did]['valid_place_images'].append((p['name'], cover))
    else:
        by_district[did]['invalid_place_images'].append((p['name'], cover))

for did, info in sorted(by_district.items()):
    val = len(info['valid_place_images'])
    inval = len(info['invalid_place_images'])
    print(f"District #{did:2d} {info['name']:22s} | Valid place images: {val} | Invalid: {inval}")
    if val > 0:
        for name, img in info['valid_place_images'][:2]:
            print(f"   -> [VALID] {name}: {img}")
