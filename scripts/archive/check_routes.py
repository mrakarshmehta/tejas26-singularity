import requests
urls = ['/stays', '/suggest', '/suggest-place']
for u in urls:
    r = requests.get(f"http://127.0.0.1:5000{u}", timeout=5)
    print(f"{u}: {r.status_code}")
