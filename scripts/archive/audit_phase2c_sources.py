"""
Read-only audit script for Phase 2C: Forests and Waterfalls.
Queries Overpass API and checks existing project assets for Bihar forests and waterfalls.
"""

import os
import sys
import json
import urllib.request
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BIHAR_BBOX = "24.2,83.3,27.6,88.3"
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
]

def query_overpass(query_str):
    data = urllib.parse.urlencode({'data': query_str}).encode('utf-8')
    for server in OVERPASS_SERVERS:
        try:
            req = urllib.request.Request(
                server,
                data=data,
                headers={'User-Agent': 'HiddenYatra-Phase2C-Audit/1.0'}
            )
            with urllib.request.urlopen(req, timeout=45) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"Server {server} failed: {e}. Trying next...")
    raise RuntimeError("All Overpass servers failed.")

def point_in_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def load_bihar_polygons():
    dist_path = os.path.abspath("static/data/bihar/districts.geojson")
    with open(dist_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [f.get("geometry", {}).get("coordinates", [[]])[0] for f in data.get("features", [])]

def audit_waterfalls():
    print("\n" + "="*60)
    print("  1. AUDITING WATERFALLS IN OPENSTREETMAP")
    print("="*60)

    bihar_polys = load_bihar_polygons()

    query = f"""
[out:json][timeout:90];
(
  node["waterway"="waterfall"]({BIHAR_BBOX});
  way["waterway"="waterfall"]({BIHAR_BBOX});
);
out body center qt;
"""
    res = query_overpass(query)
    elements = res.get('elements', [])
    print(f"Raw OSM waterfall elements in bbox: {len(elements)}")

    bihar_waterfalls = []
    for el in elements:
        lat = el.get('lat', el.get('center', {}).get('lat'))
        lon = el.get('lon', el.get('center', {}).get('lon'))
        if lat is None or lon is None:
            continue

        # Check inside Bihar
        inside = any(point_in_polygon(lon, lat, poly) for poly in bihar_polys)
        tags = el.get('tags', {})
        name = tags.get('name', 'Unnamed Waterfall')

        item = {
            'id': f"{el.get('type')}/{el.get('id')}",
            'name': name,
            'name_hi': tags.get('name:hi', tags.get('name:hindi', '')),
            'lat': round(lat, 5),
            'lon': round(lon, 5),
            'in_bihar': inside,
            'tags': tags
        }
        if inside:
            bihar_waterfalls.append(item)
            print(f"  ✓ [OSM {item['id']}] {item['name']} ({item['name_hi']}) at ({lat}, {lon})")
        else:
            print(f"  x (Outside Bihar) [OSM {item['id']}] {item['name']} at ({lat}, {lon})")

    print(f"Total verified waterfalls strictly inside Bihar: {len(bihar_waterfalls)}")
    return bihar_waterfalls

def audit_forests():
    print("\n" + "="*60)
    print("  2. AUDITING FORESTS & PROTECTED AREAS IN OPENSTREETMAP")
    print("="*60)

    bihar_polys = load_bihar_polygons()

    query = f"""
[out:json][timeout:60];
(
  relation["boundary"="protected_area"]["name"]({BIHAR_BBOX});
  relation["boundary"="national_park"]["name"]({BIHAR_BBOX});
  relation["leisure"="nature_reserve"]["name"]({BIHAR_BBOX});
  way["boundary"="protected_area"]["name"]({BIHAR_BBOX});
  way["boundary"="national_park"]["name"]({BIHAR_BBOX});
  way["leisure"="nature_reserve"]["name"]({BIHAR_BBOX});
  relation["landuse"="forest"]["name"]({BIHAR_BBOX});
);
out body center qt;
"""
    res = query_overpass(query)
    elements = res.get('elements', [])
    print(f"Raw OSM forest / protected area elements: {len(elements)}")

    bihar_forests = []
    seen_ids = set()

    for el in elements:
        el_id = f"{el.get('type')}/{el.get('id')}"
        if el_id in seen_ids:
            continue
        seen_ids.add(el_id)

        lat = el.get('lat', el.get('center', {}).get('lat'))
        lon = el.get('lon', el.get('center', {}).get('lon'))
        if lat is None or lon is None:
            continue

        inside = any(point_in_polygon(lon, lat, poly) for poly in bihar_polys)
        tags = el.get('tags', {})
        name = tags.get('name', 'Unnamed Forest')

        item = {
            'id': el_id,
            'name': name,
            'name_hi': tags.get('name:hi', tags.get('name:hindi', '')),
            'type': tags.get('boundary', tags.get('leisure', tags.get('landuse', tags.get('natural', 'forest')))),
            'protect_class': tags.get('protect_class', ''),
            'lat': round(lat, 5),
            'lon': round(lon, 5),
            'in_bihar': inside,
            'tags': tags
        }
        if inside:
            bihar_forests.append(item)
            print(f"  ✓ [OSM {item['id']}] {item['name']} ({item['type']}, {item['name_hi']}) at ({lat}, {lon})")

    print(f"Total verified forests / protected areas strictly inside Bihar: {len(bihar_forests)}")
    return bihar_forests

if __name__ == "__main__":
    wf = audit_waterfalls()
    fo = audit_forests()
