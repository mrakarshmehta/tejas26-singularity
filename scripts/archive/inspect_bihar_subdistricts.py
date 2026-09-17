"""
Inspect BIHAR_SUBDISTRICTS.geojson from datta07/INDIAN-SHAPEFILES (READ-ONLY).
Analyzes properties, feature count, district groupings, and matching with HiddenYatra DB.
"""

import urllib.request
import json
import os

def inspect_subdistricts():
    url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson"
    print(f"Inspecting {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Audit/1.0'})
    
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read().decode('utf-8')
        size_kb = len(content) / 1024
        print(f"File downloaded into memory: {size_kb:.2f} KB ({len(content)} bytes)")
        
        data = json.loads(content)
        features = data.get('features', [])
        print(f"Total features: {len(features)}")
        
        if features:
            print("\nSample feature properties:")
            print(json.dumps(features[0].get('properties', {}), indent=2))
            
            # Aggregate by district
            districts_map = {}
            for f in features:
                props = f.get('properties', {})
                # Look for district key (e.g. DISTRICT, District, dtname, etc.)
                dist = props.get('DISTRICT') or props.get('District') or props.get('dtname') or props.get('district') or 'Unknown'
                subdist = props.get('SUB_DIST') or props.get('Sub_District') or props.get('sdtname') or props.get('subdistrict') or props.get('NAME') or props.get('name')
                
                if dist not in districts_map:
                    districts_map[dist] = []
                districts_map[dist].append(subdist)
                
            print(f"\nDistricts represented in dataset: {len(districts_map)}")
            total_blocks_found = 0
            for dist, blocks in sorted(districts_map.items()):
                print(f"  - {dist}: {len(blocks)} blocks (Sample: {blocks[:3]})")
                total_blocks_found += len(blocks)
            print(f"Total block features: {total_blocks_found}")
            
            # Inspect geometry types
            geom_types = {}
            for f in features:
                gtype = f.get('geometry', {}).get('type', 'None')
                geom_types[gtype] = geom_types.get(gtype, 0) + 1
            print(f"\nGeometry types: {geom_types}")

if __name__ == "__main__":
    inspect_subdistricts()
