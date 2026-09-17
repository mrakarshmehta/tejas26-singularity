import urllib.request
import json

queries = ['Patna', 'Tutla', 'Ghora', 'Chirand', 'Barabar', 'Bateshwar', 'Kusiargaon']
for q in queries:
    url = f"http://127.0.0.1:5000/api/search/instant?q={q}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Test'})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read().decode('utf-8'))
        res = data.get('results', [])
        print(f"q={q:12}: {len(res)} results -> {[x.get('name') for x in res[:2]]}")
