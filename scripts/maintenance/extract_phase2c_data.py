"""
Phase 2C Data Extraction: Forests and Waterfalls.
Queries genuine Overpass API endpoints and saves static/data/bihar/forests.geojson and static/data/bihar/waterfalls.geojson.
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
SERVERS = [
    "https://lz4.overpass-api.de/api/interpreter",
    "https://z.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter"
]

def query_overpass(query_str):
    data = urllib.parse.urlencode({'data': query_str}).encode('utf-8')
    for server in SERVERS:
        try:
            print(f"  Querying {server} ...", flush=True)
            req = urllib.request.Request(
                server,
                data=data,
                headers={'User-Agent': 'HiddenYatra-Phase2C/1.0 (https://github.com/mrakarshmehta/HiddenYatra)'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    raw_bytes = response.read()
                    print(f"    Success! Received {len(raw_bytes)} bytes.", flush=True)
                    return json.loads(raw_bytes.decode('utf-8'))
        except Exception as e:
            print(f"    Server {server} failed: {e}. Trying next...", flush=True)
            time.sleep(1.0)
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

def load_bihar_polygons():
    dist_path = os.path.abspath("static/data/bihar/districts.geojson")
    with open(dist_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [f.get("geometry", {}).get("coordinates", [[]])[0] for f in data.get("features", [])]

def run_extraction():
    bihar_polys = load_bihar_polygons()
    print(f"Loaded {len(bihar_polys)} Bihar boundary polygons.", flush=True)

    # ─────────────────────────────────────────────────────────────
    # 1. EXTRACT FORESTS & PROTECTED AREAS
    # ─────────────────────────────────────────────────────────────
    print("\n" + "="*60, flush=True)
    print("  1. EXTRACTING FORESTS & PROTECTED AREAS", flush=True)
    print("="*60, flush=True)

    forest_queries = [
        f'way["boundary"="protected_area"]["name"]({BIHAR_BBOX});',
        f'way["leisure"="nature_reserve"]["name"]({BIHAR_BBOX});',
        f'way["boundary"="national_park"]["name"]({BIHAR_BBOX});',
        f'way["landuse"="forest"]["name"]({BIHAR_BBOX});'
    ]

    all_forest_elements = []
    forest_timestamp = datetime.now(timezone.utc).isoformat()

    for fq in forest_queries:
        q = f"""
[out:json][timeout:25];
(
  {fq}
);
out body geom qt;
"""
        try:
            res = query_overpass(q)
            els = res.get('elements', [])
            all_forest_elements.extend(els)
            print(f"  Got {len(els)} elements for query: {fq[:40]}...", flush=True)
            if 'osm3s' in res and 'timestamp_osm_base' in res['osm3s']:
                forest_timestamp = res['osm3s']['timestamp_osm_base']
        except Exception as e:
            print(f"  Warning: Query {fq[:40]} failed: {e}", flush=True)
        time.sleep(1.0)

    print(f"Total raw forest elements fetched: {len(all_forest_elements)}", flush=True)

    forest_features = []
    seen_forest_ids = set()
    total_f_raw_pts = 0
    total_f_sim_pts = 0
    dropped_f_outside = 0

    for el in all_forest_elements:
        osm_id = f"{el.get('type')}/{el.get('id')}"
        if osm_id in seen_forest_ids:
            continue
        seen_forest_ids.add(osm_id)

        tags = el.get('tags', {})
        name = tags.get('name', '').strip()
        if not name:
            continue

        geometry = el.get('geometry', [])
        if not geometry or len(geometry) < 3:
            continue

        raw_ring = [[round(pt['lon'], 5), round(pt['lat'], 5)] for pt in geometry]
        if raw_ring[0] != raw_ring[-1]:
            raw_ring.append(raw_ring[0])

        total_f_raw_pts += len(raw_ring)

        avg_lng = sum(p[0] for p in raw_ring) / len(raw_ring)
        avg_lat = sum(p[1] for p in raw_ring) / len(raw_ring)

        if not any(point_in_polygon(avg_lng, avg_lat, poly) for poly in bihar_polys):
            dropped_f_outside += 1
            continue

        sim_ring = douglas_peucker(raw_ring, 0.0005)
        if len(sim_ring) < 4:
            sim_ring = raw_ring
        if sim_ring[0] != sim_ring[-1]:
            sim_ring.append(sim_ring[0])

        total_f_sim_pts += len(sim_ring)

        forest_type = tags.get('boundary', tags.get('leisure', tags.get('landuse', tags.get('natural', 'forest'))))

        feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "name_hi": tags.get('name:hi', tags.get('name:hindi', None)),
                "name_en": tags.get('name:en', None),
                "type": forest_type,
                "protect_class": tags.get('protect_class', None),
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
        forest_features.append(feature)

    print(f"Retained Bihar forest features: {len(forest_features)} (dropped {dropped_f_outside} outside Bihar)", flush=True)
    for f in forest_features:
        print(f"  ✓ [Forest] {f['properties']['name']} ({f['properties']['type']}, OSM ID: {f['properties']['osm_id']})", flush=True)

    forests_fc = {
        "type": "FeatureCollection",
        "name": "Bihar Forests and Protected Natural Areas",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap",
            "attribution": "© OpenStreetMap contributors",
            "license": "Open Data Commons Open Database License 1.0 (ODbL)",
            "timestamp": forest_timestamp,
            "feature_count": len(forest_features),
            "raw_points_count": total_f_raw_pts,
            "simplified_points_count": total_f_sim_pts,
            "processing": "Spatially filtered to Bihar administrative boundaries, simplified via Douglas-Peucker (epsilon=0.0005)"
        },
        "features": forest_features
    }

    # ─────────────────────────────────────────────────────────────
    # 2. EXTRACT WATERFALLS
    # ─────────────────────────────────────────────────────────────
    print("\n" + "="*60, flush=True)
    print("  2. EXTRACTING WATERFALLS", flush=True)
    print("="*60, flush=True)

    wf_query = f"""
[out:json][timeout:25];
(
  node["waterway"="waterfall"]({BIHAR_BBOX});
  way["waterway"="waterfall"]({BIHAR_BBOX});
);
out body center qt;
"""
    wf_res = query_overpass(wf_query)
    wf_elements = wf_res.get('elements', [])
    wf_timestamp = wf_res.get('osm3s', {}).get('timestamp_osm_base', datetime.now(timezone.utc).isoformat())
    print(f"Total raw waterfall elements: {len(wf_elements)}", flush=True)

    wf_features = []
    seen_wf_ids = set()
    dropped_wf_outside = 0

    for el in wf_elements:
        osm_id = f"{el.get('type')}/{el.get('id')}"
        if osm_id in seen_wf_ids:
            continue
        seen_wf_ids.add(osm_id)

        lat = el.get('lat', el.get('center', {}).get('lat'))
        lon = el.get('lon', el.get('center', {}).get('lon'))
        if lat is None or lon is None:
            continue

        if not any(point_in_polygon(lon, lat, poly) for poly in bihar_polys):
            dropped_wf_outside += 1
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
        wf_features.append(feature)

    print(f"Retained Bihar waterfall features: {len(wf_features)} (dropped {dropped_wf_outside} outside Bihar)", flush=True)
    for f in wf_features:
        print(f"  ✓ [Waterfall] {f['properties']['name']} at {f['geometry']['coordinates']} (OSM ID: {f['properties']['osm_id']})", flush=True)

    waterfalls_fc = {
        "type": "FeatureCollection",
        "name": "Bihar Waterfalls",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap",
            "attribution": "© OpenStreetMap contributors",
            "license": "Open Data Commons Open Database License 1.0 (ODbL)",
            "timestamp": wf_timestamp,
            "feature_count": len(wf_features),
            "processing": "Spatially filtered to Bihar administrative boundaries"
        },
        "features": wf_features
    }

    # ─────────────────────────────────────────────────────────────
    # 3. SAVE OUTPUT FILES
    # ─────────────────────────────────────────────────────────────
    out_dir = os.path.join(os.path.dirname(__file__), "..", "static", "data", "bihar")
    os.makedirs(out_dir, exist_ok=True)

    f_file = os.path.join(out_dir, "forests.geojson")
    with open(f_file, "w", encoding="utf-8") as f:
        json.dump(forests_fc, f, indent=2, ensure_ascii=False)
    f_size = os.path.getsize(f_file)
    print(f"\n[OUTPUT] Saved forests.geojson: {len(forest_features)} features, {f_size} bytes ({f_size/1024:.1f} KB)", flush=True)

    wf_file = os.path.join(out_dir, "waterfalls.geojson")
    with open(wf_file, "w", encoding="utf-8") as f:
        json.dump(waterfalls_fc, f, indent=2, ensure_ascii=False)
    wf_size = os.path.getsize(wf_file)
    print(f"[OUTPUT] Saved waterfalls.geojson: {len(wf_features)} features, {wf_size} bytes ({wf_size/1024:.1f} KB)", flush=True)

if __name__ == "__main__":
    run_extraction()
