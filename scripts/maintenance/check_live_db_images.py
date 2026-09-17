import json

with open('scratch/live_district_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

j_places = d['jamui']['places_from_map_attr']
print(f"Total places in live Jamui data-places: {len(j_places)}")
for p in j_places:
    img = p.get('cover_image')
    print(f"  - [{p['id']:2d}] {p['name']:32s} (slug: {p['slug']:35s}, cover_image: '{img}')")
