"""
Audit OpenStreetMap admin_level=6 (Subdistrict/Block) coverage for Bihar bbox via Overpass API.
"""

import urllib.request
import urllib.parse
import json
import time

def audit_osm_blocks():
    print("Querying Overpass API for admin_level=6 in Bihar bbox [24.2, 83.3, 27.6, 88.3]...")
    query = """
    [out:json][timeout:30];
    (
      relation["boundary"="administrative"]["admin_level"="6"](24.2, 83.3, 27.6, 88.3);
    );
    out tags;
    """
    url = "https://overpass-api.de/api/interpreter"
    data = query.encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'HiddenYatra-GIS-Audit/1.0'})

    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            result = json.loads(response.read().decode('utf-8'))
            elements = result.get('elements', [])
            print(f"OSM admin_level=6 relations found in Bihar bbox: {len(elements)}")
            
            # Print sample tags
            for i, el in enumerate(elements[:10]):
                tags = el.get('tags', {})
                print(f"  [{i+1}] ID: {el.get('id')}, Name: {tags.get('name')}, admin_level: {tags.get('admin_level')}, is_in: {tags.get('is_in:state') or tags.get('addr:state') or tags.get('state')}")
    except Exception as e:
        print(f"Overpass query error: {e}")

if __name__ == "__main__":
    audit_osm_blocks()
