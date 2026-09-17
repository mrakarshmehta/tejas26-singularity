import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:5000'

def check_url(path):
    url = BASE_URL + path
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AuditScript/1.0'})
        res = urllib.request.urlopen(req)
        body = res.read().decode('utf-8', errors='replace')
        print(f"[HTTP {res.status}] {path} (length: {len(body)})")
        return body
    except Exception as e:
        print(f"[ERROR] {path}: {e}")
        return ""

print("=== CHECKING ENDPOINTS ===")
home_html = check_url('/')
districts_html = check_url('/state/bihar')
jamui_html = check_url('/state/bihar/jamui')
nalanda_html = check_url('/state/bihar/nalanda')
kaimur_html = check_url('/state/bihar/kaimur')
instant_search_json = check_url('/api/search/instant?q=jamui')
search_page_html = check_url('/search?q=jamui')
explore_html = check_url('/explore')
itinerary_html = check_url('/itinerary')

print("\n=== INSTANT SEARCH API FOR 'jamui' ===")
try:
    data = json.loads(instant_search_json)
    print(f"Results Count: {len(data.get('results', []))}")
    for item in data.get('results', []):
        print(f"  Type: {item.get('type'):10s} | Name: {item.get('name'):35s} | URL: {item.get('url')}")
except Exception as e:
    print("Could not parse search JSON:", e)

def print_page_info(name, html):
    import re
    print(f"\n=== PAGE INFO FOR {name} ===")
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    print("  H1:", [re.sub(r'<[^>]+>', '', x).strip() for x in h1])
    h2 = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    print("  H2 sample:", [re.sub(r'<[^>]+>', '', x).strip() for x in h2[:5]])

print_page_info("Jamui (/state/bihar/jamui)", jamui_html)
print_page_info("Nalanda (/state/bihar/nalanda)", nalanda_html)
print_page_info("Kaimur (/state/bihar/kaimur)", kaimur_html)
