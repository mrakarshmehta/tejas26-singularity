"""
Build, match, optimize, and validate static/data/bihar/blocks.geojson for Phase 2D.
"""

import os
import sys
import json
import re
import urllib.request
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))
from models.connection import get_db

def normalize(text):
    if not text:
        return ""
    t = text.lower().strip()
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'[^\w\s]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def point_line_distance(point, start, end):
    if start == end:
        return ((point[0] - start[0])**2 + (point[1] - start[1])**2)**0.5
    n = abs((end[1] - start[1])*point[0] - (end[0] - start[0])*point[1] + end[0]*start[1] - end[1]*start[0])
    d = ((end[1] - start[1])**2 + (end[0] - start[0])**2)**0.5
    return n / d

def douglas_peucker(pts, epsilon):
    if len(pts) <= 3:
        return pts
    dmax = 0.0
    index = 0
    for i in range(1, len(pts) - 1):
        d = point_line_distance(pts[i], pts[0], pts[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax > epsilon:
        rec1 = douglas_peucker(pts[:index+1], epsilon)
        rec2 = douglas_peucker(pts[index:], epsilon)
        return rec1[:-1] + rec2
    else:
        return [pts[0], pts[-1]]

def simplify_ring(ring, epsilon):
    is_closed = (ring[0] == ring[-1])
    if len(ring) <= 4:
        return [[round(pt[0], 5), round(pt[1], 5)] for pt in ring]
    open_ring = ring[:-1] if is_closed else ring
    simplified = douglas_peucker(open_ring, epsilon)
    if len(simplified) < 3:
        simplified = open_ring
    res = [[round(pt[0], 5), round(pt[1], 5)] for pt in simplified]
    if is_closed:
        res.append([res[0][0], res[0][1]])
    return res

def simplify_geometry(geom, epsilon=0.00025):
    gtype = geom.get('type')
    coords = geom.get('coordinates', [])
    if gtype == 'Polygon':
        new_coords = [simplify_ring(r, epsilon) for r in coords]
        return {'type': 'Polygon', 'coordinates': new_coords}
    elif gtype == 'MultiPolygon':
        new_coords = [[simplify_ring(r, epsilon) for r in poly] for poly in coords]
        return {'type': 'MultiPolygon', 'coordinates': new_coords}
    return geom

def count_vertices(geom):
    gtype = geom.get('type')
    coords = geom.get('coordinates', [])
    if gtype == 'Polygon':
        return sum(len(r) for r in coords)
    elif gtype == 'MultiPolygon':
        return sum(sum(len(r) for r in poly) for poly in coords)
    return 0

def build_blocks_geojson():
    print("=" * 60)
    print("  PHASE 2D BLOCKS GEOJSON GENERATION & MATCHING")
    print("=" * 60)

    # 1. Fetch DB districts (all 38) and blocks (92)
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, slug FROM districts WHERE state_id = 1 ORDER BY id")
        db_districts = cursor.fetchall()
        
        cursor.execute("""
            SELECT b.id as block_id, b.name as block_name, b.slug as block_slug,
                   d.id as district_id, d.name as district_name, d.slug as district_slug
            FROM blocks b
            JOIN districts d ON b.district_id = d.id
            ORDER BY d.id, b.id
        """)
        db_blocks = cursor.fetchall()

    print(f"Loaded {len(db_districts)} districts and {len(db_blocks)} blocks from MySQL.")

    # Build district normalization map
    # Maps normalized district names from Census/source to DB district dict
    district_map = {}
    for d in db_districts:
        district_map[normalize(d['name'])] = d
        district_map[d['slug']] = d

    # Additional standard Census district aliases
    census_district_aliases = {
        'pashchim champaran': district_map['west-champaran'],
        'purba champaran': district_map['east-champaran'],
        'kaimur bhabua': district_map['kaimur'],
        'kaimur': district_map['kaimur'],
        'jhanjharpur madhubani': district_map['jhanjharpur-madhubani'],
        'madhubani': district_map['jhanjharpur-madhubani'],
    }
    for k, v in census_district_aliases.items():
        district_map[k] = v

    # 2. Fetch raw GeoJSON from datta07/INDIAN-SHAPEFILES
    url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson"
    print(f"\nFetching upstream GeoJSON from {url} ...")
    req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Audit/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw_content = r.read().decode('utf-8')
    raw_size_kb = len(raw_content) / 1024
    raw_geojson = json.loads(raw_content)
    raw_features = raw_geojson.get('features', [])
    print(f"Source file size: {raw_size_kb:.2f} KB")
    print(f"Source features count: {len(raw_features)}")

    # 3. Known block name aliases between DB and Census 2011
    # Key: (district_id, normalized_census_sdtname) -> db_block
    block_alias_map = {
        # Bhagalpur (ID 5)
        (5, 'colgong'): 'kahalgaon',
        (5, 'jagdishpur'): 'bhagalpur',
        # Gaya (ID 2)
        (2, 'gaya town cdblock'): 'gaya town',
        (2, 'nagar gaya'): 'gaya town',
        (2, 'gaya'): 'gaya town',
        (2, 'gaya sadar'): 'gaya sadar',
        (2, 'tikari'): 'tekari',
        (2, 'neem chak bathani'): 'neemchak bathani',
        (2, 'tan kuppa'): 'tankuppa',
        (2, 'tankuppa'): 'tankuppa',
        # Jamui (ID 4)
        (4, 'lakshmipur'): 'simultala',
        (4, 'jhajha'): 'jhajha',
        # Nalanda (ID 3)
        (3, 'rajgir'): 'rajgir',
        (3, 'bihar'): 'bihar sharif',
        # Patna (ID 1)
        (1, 'dinapur cum khagaul'): 'danapur',
        (1, 'dinapurcumkhagaul'): 'danapur',
        (1, 'dinapur'): 'danapur',
        (1, 'patna rural'): 'patna sadar',
        (1, 'fatwah'): 'fatuha',
        (1, 'mokameh'): 'mokama',
        (1, 'bakhtiarpur'): 'bakhtiyarpur',
        # Muzaffarpur (ID 7)
        (7, 'musahri'): 'mushahari',
        (7, 'baruraj motipur'): 'motipur',
        (7, 'baruraj'): 'motipur',
        # Rohtas (ID 8)
        (8, 'sasaram'): 'sasaram',
        (8, 'dehri'): 'dehri',
    }

    # Index DB blocks by (district_id, normalized_name) and (district_id, slug)
    db_block_lookup = {}
    for b in db_blocks:
        d_id = b['district_id']
        db_block_lookup[(d_id, normalize(b['block_name']))] = b
        db_block_lookup[(d_id, b['block_slug'])] = b

    # 4. Transform, Match, and Simplify Features
    raw_vertex_count = 0
    opt_vertex_count = 0
    matched_db_blocks = set()
    output_features = []

    for f in raw_features:
        props = f.get('properties', {})
        geom = f.get('geometry', {})

        raw_vertex_count += count_vertices(geom)

        # Determine district
        raw_dtname = props.get('dtname', '')
        norm_dt = normalize(raw_dtname)
        matched_dist = district_map.get(norm_dt)
        if not matched_dist:
            print(f"WARNING: Unknown district '{raw_dtname}' (norm: '{norm_dt}')")
            continue

        d_id = matched_dist['id']
        d_name = matched_dist['name']
        d_slug = matched_dist['slug']

        # Determine sub-district / block name
        raw_sdtname = props.get('sdtname', '').strip()
        norm_sdt = normalize(raw_sdtname)
        census_code = str(props.get('sdtcode11', '')).strip()
        lgd_code = props.get('Subdt_LGD')

        # Try to match DB block
        matched_db_block = db_block_lookup.get((d_id, norm_sdt))
        if not matched_db_block:
            # Check alias
            alias_name = block_alias_map.get((d_id, norm_sdt))
            if alias_name:
                matched_db_block = db_block_lookup.get((d_id, alias_name))
        
        if not matched_db_block:
            # Substring fallback
            for (look_did, look_name), b_candidate in db_block_lookup.items():
                if look_did == d_id and (norm_sdt in look_name or look_name in norm_sdt):
                    matched_db_block = b_candidate
                    break

        if matched_db_block:
            matched_db_blocks.add(matched_db_block['block_id'])
            feature_props = {
                "block_id": matched_db_block['block_id'],
                "name": matched_db_block['block_name'],
                "slug": matched_db_block['block_slug'],
                "district_id": d_id,
                "district_name": d_name,
                "district_slug": d_slug,
                "census_code": census_code,
                "lgd_code": lgd_code,
                "source": "Census of India 2011 / Survey of India via datta07/INDIAN-SHAPEFILES",
                "source_url": "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson"
            }
        else:
            feature_props = {
                "block_id": None,
                "name": raw_sdtname,
                "slug": slugify(raw_sdtname),
                "district_id": d_id,
                "district_name": d_name,
                "district_slug": d_slug,
                "census_code": census_code,
                "lgd_code": lgd_code,
                "source": "Census of India 2011 / Survey of India via datta07/INDIAN-SHAPEFILES",
                "source_url": "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson"
            }

        # Simplify geometry
        opt_geom = simplify_geometry(geom, epsilon=0.0006)
        opt_vertex_count += count_vertices(opt_geom)

        output_features.append({
            "type": "Feature",
            "properties": feature_props,
            "geometry": opt_geom
        })

    # Sort output features by district_id, name for deterministic diffs
    output_features.sort(key=lambda x: (x['properties']['district_id'], x['properties']['name']))

    output_geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "name": "Bihar Block Boundaries",
            "source": "Census of India 2011 / Survey of India via datta07/INDIAN-SHAPEFILES",
            "source_url": "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson",
            "source_commit": "7b003e3e8c35491fadf71ced7f168f18a7423bf3",
            "license": "MIT License",
            "attribution": "Boundaries derived from Census of India 2011 & Survey of India via datta07/INDIAN-SHAPEFILES (MIT License)",
            "timestamp": "2026-08-16T17:21:00Z",
            "total_features": len(output_features),
            "total_districts": len(db_districts),
            "matched_db_blocks": len(matched_db_blocks),
            "unseeded_blocks": len(output_features) - len(matched_db_blocks)
        },
        "features": output_features
    }

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'bihar', 'blocks.geojson'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output_geojson, f, ensure_ascii=False, separators=(',', ':'))

    opt_size_kb = os.path.getsize(out_path) / 1024

    print("\n" + "=" * 60)
    print("  SUMMARY OF RESULTS")
    print("=" * 60)
    print(f"Source Features Count:   {len(raw_features)}")
    print(f"Retained Features Count: {len(output_features)}")
    print(f"Raw File Size:           {raw_size_kb:.2f} KB ({raw_size_kb/1024:.2f} MB)")
    print(f"Optimized File Size:     {opt_size_kb:.2f} KB ({opt_size_kb/1024:.2f} MB)")
    print(f"Size Reduction:          {(1 - opt_size_kb/raw_size_kb)*100:.1f}%")
    print(f"Raw Vertex Count:        {raw_vertex_count}")
    print(f"Optimized Vertex Count:  {opt_vertex_count}")
    print(f"Vertex Reduction:        {(1 - opt_vertex_count/raw_vertex_count)*100:.1f}%")
    print(f"DB Blocks Matched:       {len(matched_db_blocks)} / {len(db_blocks)} ({len(matched_db_blocks)/len(db_blocks)*100:.1f}%)")
    print(f"Unseeded Block Features: {len(output_features) - len(matched_db_blocks)}")
    print(f"Output File:             {out_path}")
    print("=" * 60)

    # Check unassigned DB blocks if any
    all_db_ids = set(b['block_id'] for b in db_blocks)
    unmatched_ids = all_db_ids - matched_db_blocks
    if unmatched_ids:
        print(f"\nUnmatched DB block IDs ({len(unmatched_ids)}):")
        for b in db_blocks:
            if b['block_id'] in unmatched_ids:
                print(f"  - ID {b['block_id']}: '{b['block_name']}' in {b['district_name']}")

if __name__ == "__main__":
    build_blocks_geojson()
