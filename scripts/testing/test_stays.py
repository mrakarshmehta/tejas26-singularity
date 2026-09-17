import requests
for page in [1, 2, 3]:
    r = requests.get(f"http://127.0.0.1:5000/stays?page={page}", timeout=15)
    print(f"Page {page}: {r.status_code}")
