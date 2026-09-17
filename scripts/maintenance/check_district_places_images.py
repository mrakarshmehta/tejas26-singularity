import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor
import os

with get_cursor() as cur:
    cur.execute("""
        SELECT d.id, d.name, d.slug, d.cover_image AS district_cover, d.image_url AS district_image_url,
               p.id AS place_id, p.name AS place_name, p.cover_image AS place_cover
        FROM districts d
        LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
        ORDER BY d.id, p.id
    """)
    rows = cur.fetchall()

districts = {}
for r in rows:
    did = r['id']
    if did not in districts:
        districts[did] = {
            'id': did,
            'name': r['name'],
            'slug': r['slug'],
            'district_cover': r['district_cover'],
            'district_image_url': r['district_image_url'],
            'places': []
        }
    if r['place_id']:
        districts[did]['places'].append({
            'id': r['place_id'],
            'name': r['place_name'],
            'cover_image': r['place_cover'],
        })

print(f"Total districts: {len(districts)}")
for did, d in sorted(districts.items()):
    places_count = len(d['places'])
    sample_place_cover = d['places'][0]['cover_image'] if places_count > 0 else 'None'
    # Check if district cover exists on disk
    dist_cover = d['district_cover'] or ''
    dist_exists = False
    if dist_cover.startswith(('http://', 'https://')):
        dist_exists = True
    elif dist_cover:
        dist_exists = os.path.exists(os.path.join('static', 'uploads', 'districts', dist_cover))
    
    # Check if sample place cover exists on disk
    place_exists = False
    if sample_place_cover.startswith(('http://', 'https://')):
        place_exists = True
    elif sample_place_cover != 'None' and sample_place_cover:
        place_exists = os.path.exists(os.path.join('static', 'uploads', 'places', sample_place_cover))
        
    print(f"#{d['id']:2d} {d['name']:22s} | Places: {places_count:2d} | DistCover: {dist_cover[:20]:20s} (exists={dist_exists}) | PlaceCover: {sample_place_cover[:20]:20s} (exists={place_exists})")
