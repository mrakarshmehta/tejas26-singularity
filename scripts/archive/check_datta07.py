"""
Check datta07/INDIAN-SHAPEFILES repository for Bihar Sub-districts / Blocks.
"""

import urllib.request
import json

def check_repo():
    urls = [
        "https://api.github.com/repos/datta07/INDIAN-SHAPEFILES/contents",
        "https://api.github.com/repos/datta07/INDIAN-SHAPEFILES/contents/STATES",
        "https://api.github.com/repos/datta07/INDIAN-SHAPEFILES/contents/STATES/BIHAR"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'HiddenYatra-Audit/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode('utf-8'))
                print(f"Contents of {url}:")
                for item in data:
                    print(f"  - {item.get('name')} ({item.get('type')})")
        except Exception as e:
            print(f"Error {url}: {e}")

if __name__ == "__main__":
    check_repo()
