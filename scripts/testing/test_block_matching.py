"""
Test join/matching between 92 HiddenYatra database blocks and 534 Census/LGD GeoJSON subdistricts.
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

def test_matching():
    # 1. Fetch 92 DB blocks
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT b.id as block_id, b.name as block_name, b.slug as block_slug,
                   d.id as district_id, d.name as district_name, d.slug as district_slug
            FROM blocks b
            JOIN districts d ON b.district_id = d.id
            ORDER BY d.name, b.name
        """)
        db_blocks = cursor.fetchall()

    print(f"Total DB blocks to match: {len(db_blocks)}")

    # 2. Fetch GeoJSON from memory
    url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson"
    req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Audit/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        geojson = json.loads(r.read().decode('utf-8'))

    features = geojson.get('features', [])
    print(f"Total GeoJSON features: {len(features)}")

    # Build lookup table from GeoJSON: (norm_district, norm_subdist) -> feature
    # Also index by district
    district_aliases = {
        'pashchim champaran': 'west champaran',
        'purba champaran': 'east champaran',
        'kaimur (bhabua)': 'kaimur',
        'jhanjharpur (madhubani)': 'madhubani',
    }

    geo_by_district = {}
    for f in features:
        props = f.get('properties', {})
        dt = normalize(props.get('dtname', ''))
        # Map alias
        dt_mapped = district_aliases.get(dt, dt)
        sdt = normalize(props.get('sdtname', ''))
        
        if dt_mapped not in geo_by_district:
            geo_by_district[dt_mapped] = {}
        geo_by_district[dt_mapped][sdt] = f

    matched = 0
    unmatched_db = []

    for b in db_blocks:
        d_norm = normalize(b['district_name'])
        d_norm = district_aliases.get(d_norm, d_norm)
        b_norm = normalize(b['block_name'])

        district_features = geo_by_district.get(d_norm, {})
        
        # Try direct match
        found = district_features.get(b_norm)
        
        # Try substring / word match
        if not found:
            for sdt_key, feat in district_features.items():
                if b_norm in sdt_key or sdt_key in b_norm:
                    found = feat
                    break

        if found:
            matched += 1
        else:
            unmatched_db.append((b, list(district_features.keys())))

    print(f"\nMatching Results:")
    print(f"  Matched: {matched} / {len(db_blocks)} ({matched/len(db_blocks)*100:.1f}%)")
    print(f"  Unmatched: {len(unmatched_db)}")
    if unmatched_db:
        print("\nUnmatched DB blocks:")
        for b, candidates in unmatched_db[:10]:
            print(f"   DB Block: '{b['block_name']}' in District '{b['district_name']}'")
            print(f"     Candidates in GeoJSON: {candidates[:5]}")

if __name__ == "__main__":
    test_matching()
