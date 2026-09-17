"""
Overpass API Extraction Script for Bihar Rivers and Waterbodies (Lakes & Dams).
Fetches genuine OpenStreetMap vector geometries within Bihar bounding box [24.2, 83.3, 27.6, 88.3].
Converts OSM elements into validated, simplified GeoJSON files with 100% source traceability.
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

OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
]

BIHAR_BBOX = "24.2,83.3,27.6,88.3"

def query_overpass(query_str):
    data = urllib.parse.urlencode({'data': query_str}).encode('utf-8')
    for server in OVERPASS_SERVERS:
        print(f"[Overpass] Querying {server} ...")
        req = urllib.request.Request(
            server,
            data=data,
            headers={
                'User-Agent': 'HiddenYatra-GIS-Extraction/1.0 (https://github.com/mrakarshmehta/HiddenYatra)'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                if response.status == 200:
                    raw_bytes = response.read()
                    print(f"  Received {len(raw_bytes)} bytes.")
                    return json.loads(raw_bytes.decode('utf-8'))
        except Exception as e:
            print(f"  Failed on {server}: {e}. Trying next server...")
            time.sleep(2.0)
    raise RuntimeError("All Overpass servers failed or timed out.")

def douglas_peucker(point_list, epsilon):
    """Simple, pure-Python Douglas-Peucker line simplification algorithm."""
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

def extract_rivers():
    print("\n" + "="*60)
    print("  1. EXTRACTING BIHAR RIVERS FROM OPENSTREETMAP")
    print("="*60)

    # Query major named rivers in Bihar
    query = f"""
[out:json][timeout:90];
(
  way["waterway"="river"]["name"]({BIHAR_BBOX});
  relation["waterway"="river"]["name"]({BIHAR_BBOX});
);
out geom;
"""
    osm_data = query_overpass(query)
    elements = osm_data.get('elements', [])
    timestamp = osm_data.get('osm3s', {}).get('timestamp_osm_base', datetime.now(timezone.utc).isoformat())
    print(f"  OSM base timestamp: {timestamp}")
    print(f"  Raw OSM elements count: {len(elements)}")

    # Target key rivers to group segments
    # Group way geometries by river name to avoid fragmented micro-ways
    river_groups = {}
    for el in elements:
        tags = el.get('tags', {})
        name = tags.get('name', '').strip()
        if not name:
            continue

        geometry = el.get('geometry', [])
        if not geometry or len(geometry) < 2:
            continue

        # Extract [lng, lat]
        coords = [[round(pt['lon'], 5), round(pt['lat'], 5)] for pt in geometry]

        if name not in river_groups:
            river_groups[name] = {
                'name': name,
                'name_hi': tags.get('name:hi', tags.get('name:hindi', '')),
                'name_en': tags.get('name:en', ''),
                'wikidata': tags.get('wikidata', ''),
                'wikipedia': tags.get('wikipedia', ''),
                'osm_ids': [f"{el.get('type')}/{el.get('id')}"],
                'segments': []
            }
        else:
            river_groups[name]['osm_ids'].append(f"{el.get('type')}/{el.get('id')}")
            if not river_groups[name]['name_hi'] and tags.get('name:hi'):
                river_groups[name]['name_hi'] = tags.get('name:hi')
            if not river_groups[name]['wikidata'] and tags.get('wikidata'):
                river_groups[name]['wikidata'] = tags.get('wikidata')

        river_groups[name]['segments'].append(coords)

    print(f"  Unique named rivers found: {len(river_groups)}")
    for name, info in list(river_groups.items())[:15]:
        print(f"    - {name} ({len(info['segments'])} segments, OSM IDs: {info['osm_ids'][:2]})")

    # Build GeoJSON features
    features = []
    total_raw_points = 0
    total_simplified_points = 0

    for name, info in river_groups.items():
        # Keep rivers that have substantial length / recognizable presence
        all_segments = info['segments']
        raw_pts_count = sum(len(s) for s in all_segments)
        total_raw_points += raw_pts_count

        # Simplify segments using epsilon ~ 0.0008 (approx 80m ground resolution)
        simplified_segments = []
        for s in all_segments:
            sim_s = douglas_peucker(s, 0.0008)
            if len(sim_s) >= 2:
                simplified_segments.append(sim_s)

        sim_pts_count = sum(len(s) for s in simplified_segments)
        total_simplified_points += sim_pts_count

        if not simplified_segments:
            continue

        if len(simplified_segments) == 1:
            geom = {
                "type": "LineString",
                "coordinates": simplified_segments[0]
            }
        else:
            geom = {
                "type": "MultiLineString",
                "coordinates": simplified_segments
            }

        feature = {
            "type": "Feature",
            "properties": {
                "name": info['name'],
                "name_hi": info['name_hi'] or None,
                "name_en": info['name_en'] or None,
                "waterway": "river",
                "osm_ids": info['osm_ids'][:10], # List up to 10 primary way IDs
                "osm_primary_id": info['osm_ids'][0],
                "source": "OpenStreetMap",
                "source_url": f"https://www.openstreetmap.org/{info['osm_ids'][0]}",
                "wikidata": info['wikidata'] or None,
                "wikipedia": info['wikipedia'] or None,
                "segment_count": len(all_segments)
            },
            "geometry": geom
        }
        features.append(feature)

    # Sort features by segment count descending (major rivers first)
    features.sort(key=lambda f: f['properties']['segment_count'], reverse=True)

    rivers_geojson = {
        "type": "FeatureCollection",
        "name": "Bihar Rivers",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap",
            "attribution": "© OpenStreetMap contributors",
            "license": "Open Data Commons Open Database License 1.0 (ODbL)",
            "query": f'way["waterway"="river"]["name"]({BIHAR_BBOX}); relation["waterway"="river"]["name"]({BIHAR_BBOX});',
            "timestamp": timestamp,
            "feature_count": len(features),
            "raw_points_count": total_raw_points,
            "simplified_points_count": total_simplified_points
        },
        "features": features
    }

    return rivers_geojson, total_raw_points, total_simplified_points, len(elements), timestamp

def extract_waterbodies():
    print("\n" + "="*60)
    print("  2. EXTRACTING BIHAR LAKES, DAMS & RESERVOIRS FROM OPENSTREETMAP")
    print("="*60)

    # Query named lakes, reservoirs, dams, and wetlands in Bihar
    query = f"""
[out:json][timeout:90];
(
  way["natural"="water"]["name"]({BIHAR_BBOX});
  relation["natural"="water"]["name"]({BIHAR_BBOX});
  way["landuse"="reservoir"]["name"]({BIHAR_BBOX});
  way["water"]["name"]({BIHAR_BBOX});
);
out geom;
"""
    osm_data = query_overpass(query)
    elements = osm_data.get('elements', [])
    timestamp = osm_data.get('osm3s', {}).get('timestamp_osm_base', datetime.now(timezone.utc).isoformat())
    print(f"  OSM base timestamp: {timestamp}")
    print(f"  Raw OSM water elements count: {len(elements)}")

    features = []
    total_raw_points = 0
    total_simplified_points = 0

    seen_ids = set()

    for el in elements:
        osm_id = f"{el.get('type')}/{el.get('id')}"
        if osm_id in seen_ids:
            continue
        seen_ids.add(osm_id)

        tags = el.get('tags', {})
        name = tags.get('name', '').strip()
        if not name:
            continue

        geometry = el.get('geometry', [])
        if not geometry or len(geometry) < 3:
            continue

        raw_ring = [[round(pt['lon'], 5), round(pt['lat'], 5)] for pt in geometry]
        # Ensure closed polygon
        if raw_ring[0] != raw_ring[-1]:
            raw_ring.append(raw_ring[0])

        total_raw_points += len(raw_ring)

        # Simplify using epsilon ~ 0.0004 (~40m resolution)
        sim_ring = douglas_peucker(raw_ring, 0.0004)
        if len(sim_ring) < 4:
            sim_ring = raw_ring # preserve minimal polygon if over-simplified
        if sim_ring[0] != sim_ring[-1]:
            sim_ring.append(sim_ring[0])

        total_simplified_points += len(sim_ring)

        water_type = tags.get('water', tags.get('natural', tags.get('landuse', 'water')))

        feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "name_hi": tags.get('name:hi', tags.get('name:hindi', None)),
                "name_en": tags.get('name:en', None),
                "natural": tags.get('natural', None),
                "water": water_type,
                "landuse": tags.get('landuse', None),
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

    print(f"  Extracted valid named waterbody polygons: {len(features)}")
    for f in features[:15]:
        props = f['properties']
        print(f"    - {props['name']} ({props['water']}, OSM ID: {props['osm_id']})")

    lakes_geojson = {
        "type": "FeatureCollection",
        "name": "Bihar Lakes, Reservoirs and Waterbodies",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap",
            "attribution": "© OpenStreetMap contributors",
            "license": "Open Data Commons Open Database License 1.0 (ODbL)",
            "query": f'way["natural"="water"]["name"]({BIHAR_BBOX}); relation["natural"="water"]["name"]({BIHAR_BBOX}); way["landuse"="reservoir"]["name"]({BIHAR_BBOX}); way["water"]["name"]({BIHAR_BBOX});',
            "timestamp": timestamp,
            "feature_count": len(features),
            "raw_points_count": total_raw_points,
            "simplified_points_count": total_simplified_points
        },
        "features": features
    }

    return lakes_geojson, total_raw_points, total_simplified_points, len(elements), timestamp

if __name__ == "__main__":
    rivers_geojson, r_raw_pts, r_sim_pts, r_raw_els, r_time = extract_rivers()
    lakes_geojson, l_raw_pts, l_sim_pts, l_raw_els, l_time = extract_waterbodies()

    out_dir = os.path.join(os.path.dirname(__file__), "..", "static", "data", "bihar")
    os.makedirs(out_dir, exist_ok=True)

    rivers_file = os.path.join(out_dir, "rivers.geojson")
    with open(rivers_file, "w", encoding="utf-8") as f:
        json.dump(rivers_geojson, f, indent=2, ensure_ascii=False)
    r_size = os.path.getsize(rivers_file)
    print(f"\n[OUTPUT] Saved rivers.geojson: {len(rivers_geojson['features'])} features, {r_size} bytes")

    lakes_file = os.path.join(out_dir, "lakes_dams.geojson")
    with open(lakes_file, "w", encoding="utf-8") as f:
        json.dump(lakes_geojson, f, indent=2, ensure_ascii=False)
    l_size = os.path.getsize(lakes_file)
    print(f"[OUTPUT] Saved lakes_dams.geojson: {len(lakes_geojson['features'])} features, {l_size} bytes")
