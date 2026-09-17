"""
Inspect subdistrict names for Patna, Gaya, and Jamui in BIHAR_SUBDISTRICTS.geojson.
"""

import json
import urllib.request

url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson"
req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Audit/1.0'})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode('utf-8'))

for dist_target in ['Patna', 'Gaya', 'Jamui']:
    print(f"\n=== Subdistricts in {dist_target} ===")
    for f in data['features']:
        p = f['properties']
        if p.get('dtname', '').lower() == dist_target.lower():
            print(f"  - sdtname: '{p.get('sdtname')}' (sdtcode11: {p.get('sdtcode11')}, LGD: {p.get('Subdt_LGD')})")
