import sys, os
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

def resolve_district_display_image(district, district_places_map=None, base_dir='.'):
    """
    Resolves the best display image URL for a district using the strict fallback chain:
    1. Valid district cover_image (if file exists locally in uploads/districts or is http URL)
    2. First valid place cover_image belonging to this district (if file exists in uploads/places or is http URL)
    3. district.image_url (if http URL)
    4. None (triggers clean gradient/emoji fallback)
    """
    # 1. District cover_image
    cover = district.get('cover_image') or ''
    if cover:
        if cover.startswith(('http://', 'https://')):
            return cover
        # Check static/uploads/districts
        local_path = os.path.join(base_dir, 'static', 'uploads', 'districts', cover)
        if os.path.isfile(local_path):
            return f"/static/uploads/districts/{cover}"
        # Also check if cover was mistakenly stored referencing uploads/places
        local_places_path = os.path.join(base_dir, 'static', 'uploads', 'places', cover)
        if os.path.isfile(local_places_path):
            return f"/static/uploads/places/{cover}"

    # 2. First valid place image in this district
    if district_places_map and district['id'] in district_places_map:
        for p in district_places_map[district['id']]:
            p_cover = p.get('cover_image') or ''
            if p_cover:
                if p_cover.startswith(('http://', 'https://')):
                    return p_cover
                p_local = os.path.join(base_dir, 'static', 'uploads', 'places', p_cover)
                if os.path.isfile(p_local):
                    return f"/static/uploads/places/{p_cover}"

    # 3. District image_url
    img_url = district.get('image_url') or ''
    if img_url and img_url.startswith(('http://', 'https://')):
        return img_url

    # 4. Fallback
    return None

# Test on all 38 districts
with get_cursor() as cur:
    cur.execute("SELECT * FROM districts WHERE state_id = 1 AND is_visible = 1 ORDER BY sort_order, name")
    districts = cur.fetchall()
    
    cur.execute("SELECT id, name, district_id, cover_image FROM places WHERE deleted_at IS NULL ORDER BY id")
    places = cur.fetchall()

places_map = {}
for p in places:
    places_map.setdefault(p['district_id'], []).append(p)

print(f"Testing resolve_district_display_image on {len(districts)} districts:")
with_image = 0
with_fallback = 0

for d in districts:
    img = resolve_district_display_image(d, places_map)
    if img:
        with_image += 1
        print(f"  [IMG] District #{d['id']:2d} {d['name']:22s} -> {img}")
    else:
        with_fallback += 1
        print(f"  [FALLBACK] District #{d['id']:2d} {d['name']:22s} -> [CLEAN GRADIENT/EMOJI FALLBACK]")

print(f"\nSummary: {with_image} districts with real valid images, {with_fallback} districts with clean gradient fallback.")
