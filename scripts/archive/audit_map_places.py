import sys, os
sys.path.insert(0, os.path.abspath('.'))

from dotenv import load_dotenv
load_dotenv()

import json
from models.places import get_places_for_map
from models.database import get_districts_by_state, get_state_by_slug

places = get_places_for_map()
bihar = get_state_by_slug('bihar')
districts = get_districts_by_state(bihar['id']) if bihar else []

print(f"Total places returned for map: {len(places)}")
print(f"Total districts in DB for Bihar: {len(districts)}")

sample_districts = ['Patna', 'Gaya', 'Nalanda', 'Jamui', 'Bhagalpur']
for d in sample_districts:
    d_places = [p for p in places if p.get('district_name') == d]
    print(f"\n--- District: {d} ({len(d_places)} places) ---")
    for p in d_places:
        print(f"  * {p['name']} | Lat: {p['latitude']} | Lng: {p['longitude']} | Category: {p['category']} | Slug: {p['slug']}")
