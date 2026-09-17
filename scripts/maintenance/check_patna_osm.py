"""
Check OSM admin_level=7 and admin_level=8 coverage for Patna district in Bihar.
"""

import urllib.request
import urllib.parse
import json

def check_patna_osm():
    # Patna district bbox approx: 25.2, 84.7, 25.8, 85.5
    query = """
    [out:json][timeout:25];
    (
      relation["boundary"="administrative"]["admin_level"="7"](25.2, 84.7, 25.8, 85.5);
      relation["boundary"="administrative"]["admin_level"="8"](25.2, 84.7, 25.8, 85.5);
    );
    out tags;
    """
    url = "https://overpass-api.de/api/interpreter"
    data = query.encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'HiddenYatra-GIS-Audit/1.0'})

    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.loads(response.read().decode('utf-8'))
            elements = result.get('elements', [])
            print(f"OSM admin_level=7/8 in Patna bbox: {len(elements)}")
            for el in elements:
                print(" ", el.get('id'), el.get('tags', {}).get('name'), el.get('tags', {}).get('admin_level'))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_patna_osm()
