"""
Extraction and processing script for Bihar Forests and Waterfalls.
Queries OpenStreetMap Overpass API for genuine vector data.
Filters to Bihar administrative boundary and generates clean, optimized GeoJSON files.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone

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
        print(f"[Overpass] Querying {server} ...")
        req = urllib.request.Request(
            server,
            data=data,
            headers={'User-Agent': 'HiddenYatra-Phase2C-GIS/1.0 (https://github.com/mrakarshmehta/HiddenYatra)'}
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                if response.status == 200:
                    raw_bytes = response.read()
                    print(f"  Received {len(raw_bytes)} bytes.")
                    return json.loads(raw_bytes.decode('utf-8'))
        except Exception as e:
            print(f"  Server {server} failed: {e}. Trying next...")
            time.sleep(2.0)
    raise RuntimeError("All Overpass servers failed or timed out.")

def douglas_peucker(point_list, epsilon):
    if len(point_list) < 3:
        return point_list

    def perpendicular_distance(point, line_start, line_end):
        x, y = point[0], point[1]
        x1, y1 = line_start[0], line_start[1]
        x2, y2 = line_end[0], line_end[1]
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return ((x - x1)**2 + (y - y1)**2)**0.5
        numerator = abs(dy * x - dx * y + x2 * y1 - y2 * x1)
        denominator = (dx**2 + dy**2)**0.5
        return numerator / denominator

    dmax = 0.0
    index = 0
    end = len(point_list) - 1
    for i in range(1, end):
        d = perpendicular_distance(point_list[i], point_list[0], point_list[end])
        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        rec_results1 = douglas_peucker(point_list[:index + 1], epsilon)
        rec_results2 = douglas_peucker(point_list[index:], epsilon)
        return rec_results1[:-1] + rec_results2
    else:
        return [point_list[0], point_list[end]]

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

def load_bihar_district_polygons():
    dist_path = os.path.abspath("static/data/bihar/districts.geojson")
    with open(dist_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [f.get("geometry", {}).get("coordinates", [[]])[0] for f in data.get("features", [])]

def extract_forests(district_polys):
    print("\n" + "="*60)
    print("  1. EXTRACTING BIHAR FORESTS & PROTECTED AREAS")
    print("="*60)

    # Use smaller, fast targeted queries
    subqueries = [
        f'way["boundary"="protected_area"]["name"]({BIHAR_BBOX});',
        f'way["boundary"="national_park"]["name"]({BIHAR_BBOX});',
        f'way["leisure"="nature_reserve"]["name"]({BIHAR_BBOX});',
        f'way["landuse"="forest"]["name"]({BIHAR_BBOX});',
        f'relation["boundary"="protected_area"]["name"]({BIHAR_BBOX});'
    ]

    elements = []
    timestamp = datetime.now(timezone.utc).isoformat()

    for sq in subqueries:
        q = f"""
[out:json][timeout:30];
(
  {sq}
);
out body geom qt;
"""
        try:
            print(f"  Querying: {sq[:50]}...")
            data = query_overpass(q)
            els = data.get('elements', [])
            print(f"    Got {len(els)} elements.")
            elements.extend(els)
            if 'osm3s' in data and 'timestamp_osm_base' in data['osm3s']:
                timestamp = data['osm3s']['timestamp_osm_base']
        except Exception as err:
            print(f"    Warning: subquery failed: {err}")
        time.sleep(1.0)

    features = []
    seen_ids = set()
    total_raw_points = 0
    total_sim_points = 0
    dropped_outside = 0
    dropped_unnamed = 0

    for el in elements:
        osm_id = f"{el.get('type')}/{el.get('id')}"
        if osm_id in seen_ids:
            continue
        seen_ids.add(osm_id)

        tags = el.get('tags', {})
        name = tags.get('name', '').strip()
        if not name:
            dropped_unnamed += 1
            continue

        geometry = el.get('geometry', [])
        if not geometry or len(geometry) < 3:
            continue

        # Extract ring coordinates [lng, lat]
        raw_ring = [[round(pt['lon'], 5), round(pt['lat'], 5)] for pt in geometry]
        if raw_ring[0] != raw_ring[-1]:
            raw_ring.append(raw_ring[0])

        total_raw_points += len(raw_ring)

        # Check centroid in Bihar
        avg_lng = sum(p[0] for p in raw_ring) / len(raw_ring)
        avg_lat = sum(p[1] for p in raw_ring) / len(raw_ring)

        if not any(point_in_polygon(avg_lng, avg_lat, poly) for poly in district_polys):
            dropped_outside += 1
            continue

        # Simplify via Douglas-Peucker (epsilon=0.0005)
        sim_ring = douglas_peucker(raw_ring, 0.0005)
        if len(sim_ring) < 4:
            sim_ring = raw_ring
        if sim_ring[0] != sim_ring[-1]:
            sim_ring.append(sim_ring[0])

        total_sim_points += len(sim_ring)

        forest_type = tags.get('boundary', tags.get('leisure', tags.get('landuse', tags.get('natural', 'forest'))))
        protect_class = tags.get('protect_class', None)

        feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "name_hi": tags.get('name:hi', tags.get('name:hindi', None)),
                "name_en": tags.get('name:en', None),
                "type": forest_type,
                "protect_class": protect_class,
                "boundary": tags.get('boundary', None),
                "leisure": tags.get('leisure', None),
                "landuse": tags.get('landuse', None),
                "natural": tags.get('natural', None),
                "osm_id": osm_id,
                "source": "OpenStreetMap",
                "source_url": f"https://www.openstreetmap.org/{osm_id}",
                "wikidata": tags.get('wikidata', None),
                "wikipedia": tags.get('wikipedia', None)
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [sim_ring]
            }
        }
        features.append(feature)

    print(f"  Retained Bihar forest/protected area polygons: {len(features)} (dropped {dropped_outside} outside Bihar, {dropped_unnamed} unnamed)")
    for f in features[:15]:
        props = f['properties']
        print(f"    - {props['name']} ({props['type']}, OSM ID: {props['osm_id']})")

    forests_geojson = {
        "type": "FeatureCollection",
        "name": "Bihar Forests and Protected Natural Areas",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap",
            "attribution": "© OpenStreetMap contributors",
            "license": "Open Data Commons Open Database License 1.0 (ODbL)",
            "query": f'relation["boundary"="protected_area"]["name"]({BIHAR_BBOX}); way["boundary"="protected_area"]["name"]({BIHAR_BBOX}); way["landuse"="forest"]["name"]({BIHAR_BBOX}); ...',
            "timestamp": timestamp,
            "feature_count": len(features),
            "raw_points_count": total_raw_points,
            "simplified_points_count": total_sim_points,
            "processing": "Spatially filtered to Bihar administrative boundaries, simplified via Douglas-Peucker (epsilon=0.0005)"
        },
        "features": features
    }

    return forests_geojson, total_raw_points, total_sim_points, len(elements), dropped_outside, dropped_unnamed

def extract_waterfalls(district_polys):
    print("\n" + "="*60)
    print("  2. EXTRACTING BIHAR WATERFALLS")
    print("="*60)

    query = f"""
[out:json][timeout:90];
(
  node["waterway"="waterfall"]({BIHAR_BBOX});
  way["waterway"="waterfall"]({BIHAR_BBOX});
);
out body center qt;
"""
    osm_data = query_overpass(query)
    elements = osm_data.get('elements', [])
    timestamp = osm_data.get('osm3s', {}).get('timestamp_osm_base', datetime.now(timezone.utc).isoformat())
    print(f"  Raw OSM elements: {len(elements)} (Timestamp: {timestamp})")

    features = []
    seen_ids = set()
    dropped_outside = 0

    for el in elements:
        osm_id = f"{el.get('type')}/{el.get('id')}"
        if osm_id in seen_ids:
            continue
        seen_ids.add(osm_id)

        lat = el.get('lat', el.get('center', {}).get('lat'))
        lon = el.get('lon', el.get('center', {}).get('lon'))
        if lat is None or lon is None:
            continue

        # Check inside Bihar
        if not any(point_in_polygon(lon, lat, poly) for poly in district_polys):
            dropped_outside += 1
            continue

        tags = el.get('tags', {})
        name = tags.get('name', 'Waterfall')

        feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "name_hi": tags.get('name:hi', tags.get('name:hindi', None)),
                "name_en": tags.get('name:en', None),
                "waterway": "waterfall",
                "height": tags.get('height', None),
                "osm_id": osm_id,
                "source": "OpenStreetMap",
                "source_url": f"https://www.openstreetmap.org/{osm_id}",
                "wikidata": tags.get('wikidata', None),
                "wikipedia": tags.get('wikipedia', None)
            },
            "geometry": {
                "type": "Point",
                "coordinates": [round(lon, 5), round(lat, 5)]
            }
        }
        features.append(feature)

    print(f"  Retained Bihar waterfalls: {len(features)} (dropped {dropped_outside} outside Bihar)")
    for f in features:
        props = f['properties']
        print(f"    - {props['name']} at {f['geometry']['coordinates']} (OSM ID: {props['osm_id']})")

    waterfalls_geojson = {
        "type": "FeatureCollection",
        "name": "Bihar Waterfalls",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap",
            "attribution": "© OpenStreetMap contributors",
            "license": "Open Data Commons Open Database License 1.0 (ODbL)",
            "query": f'node["waterway"="waterfall"]({BIHAR_BBOX}); way["waterway"="waterfall"]({BIHAR_BBOX});',
            "timestamp": timestamp,
            "feature_count": len(features),
            "processing": "Spatially filtered to Bihar administrative boundaries"
        },
        "features": features
    }

    return waterfalls_geojson, len(elements), dropped_outside

if __name__ == "__main__":
    polys = load_bihar_district_polygons()
    print(f"Loaded {len(polys)} Bihar district boundary polygons.")

    forests_fc, f_raw_pts, f_sim_pts, f_raw_els, f_drop_out, f_drop_un = extract_forests(polys)
    wf_fc, wf_raw_els, wf_drop_out = extract_waterfalls(polys)

    out_dir = os.path.join(os.path.dirname(__file__), "..", "static", "data", "bihar")
    os.makedirs(out_dir, exist_ok=True)

    forests_file = os.path.join(out_dir, "forests.geojson")
    with open(forests_file, "w", encoding="utf-8") as f:
        json.dump(forests_fc, f, indent=2, ensure_ascii=False)
    f_sz = os.path.getsize(forests_file)
    print(f"\n[OUTPUT] Saved forests.geojson: {len(forests_fc['features'])} features, {f_sz} bytes ({f_sz/1024:.1f} KB)")

    wf_file = os.path.join(out_dir, "waterfalls.geojson")
    with open(wf_file, "w", encoding="utf-8") as f:
        json.dump(wf_fc, f, indent=2, ensure_ascii=False)
    wf_sz = os.path.getsize(wf_file)
    print(f"[OUTPUT] Saved waterfalls.geojson: {len(wf_fc['features'])} features, {wf_sz} bytes ({wf_sz/1024:.1f} KB)")
