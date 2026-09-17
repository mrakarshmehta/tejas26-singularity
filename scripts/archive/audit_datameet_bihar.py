"""
Inspect Datameet Sub-District GeoJSON for Bihar to verify feature counts, attributes, and matching.
"""

import urllib.request
import json
import os

def audit_datameet():
    # Datameet Sub-district data URL (Bihar extract or full repo)
    # Datameet provides state-wise files or full India shapefiles/GeoJSONs
    print("Testing Datameet repository URL...")
    # Check if there is a direct raw geojson URL or git info
    test_urls = [
        "https://raw.githubusercontent.com/datameet/maps/master/Sub-District/bihar_subdistrict.geojson",
        "https://raw.githubusercontent.com/datameet/maps/master/Sub-District/Bihar_SubDistrict.geojson",
        "https://api.github.com/repos/datameet/maps/contents/Sub-District"
    ]
    
    for url in test_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Audit/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                content_type = r.headers.get('Content-Type', '')
                print(f"URL: {url} -> Status: {r.status}, Content-Type: {content_type}")
                if 'json' in content_type and 'api.github.com' in url:
                    data = json.loads(r.read().decode('utf-8'))
                    print("Files in Datameet Sub-District repo:")
                    for item in data:
                        print(f"  - {item.get('name')} ({item.get('size')} bytes)")
        except Exception as e:
            print(f"URL: {url} -> Error: {e}")

if __name__ == "__main__":
    audit_datameet()
