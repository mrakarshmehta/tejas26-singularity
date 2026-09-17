import urllib.request
import re
import json

url = 'https://hiddenyatra.onrender.com/state/bihar/gaya'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        print(f"Gaya page length: {len(html)} bytes")
        print("Contains district-map:", 'id="district-map"' in html)
        print("Contains No places listed:", 'No places listed in Gaya' in html)
        
        m = re.search(r'data-places=\'([^\']+)\'', html)
        if m:
            places = json.loads(m.group(1))
            print(f"Gaya has {len(places)} places in data-places on LIVE!")
            for p in places:
                print(f"  - [{p.get('id')}] {p.get('name')} (cat={p.get('category')}, coords={p.get('latitude')},{p.get('longitude')})")
        else:
            print("data-places NOT FOUND in HTML! Checking page content:")
            # Find title / error
            title_m = re.search(r'<title>(.*?)</title>', html)
            print("Title:", title_m.group(1) if title_m else "None")
            h1_m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
            print("H1:", h1_m.group(1).strip() if h1_m else "None")
except Exception as e:
    print('Error fetching Gaya:', e)
