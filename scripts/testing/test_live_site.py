import urllib.request
import urllib.error
import re
import json

BASE_URL = "https://hiddenyatra.onrender.com"

endpoints_to_test = [
    "/",
    "/places",
    "/map",
    "/stays",
    "/host",
    "/login",
    "/signup",
    "/community",
    "/itinerary",
    "/wishlist",
    "/health",
    "/api/places",
    "/api/categories",
    "/api/districts",
    "/api/search?q=bihar",
    "/api/stays",
    "/api/community/posts",
]

def check_url(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            content = resp.read()
            return status, content, resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), {}
    except Exception as e:
        return 0, str(e).encode(), {}

print("=== TESTING MAIN ENDPOINTS ===")
all_html = {}
for ep in endpoints_to_test:
    url = BASE_URL + ep
    status, body, headers = check_url(url)
    print(f"[{status}] {ep} (size: {len(body)} bytes)")
    if status == 200 and 'text/html' in headers.get('Content-Type', ''):
        all_html[ep] = body.decode('utf-8', errors='ignore')

print("\n=== EXTRACTING & TESTING ASSETS (CSS/JS/IMAGES) ===")
asset_urls = set()
for ep, html in all_html.items():
    # css
    for m in re.finditer(r'<link[^>]+href=["\']([^"\']+)["\']', html):
        href = m.group(1)
        if not href.startswith(('http:', 'https:', '//', 'data:')):
            asset_urls.add(href)
    # js
    for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html):
        src = m.group(1)
        if not src.startswith(('http:', 'https:', '//', 'data:')):
            asset_urls.add(src)
    # img
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html):
        src = m.group(1)
        if not src.startswith(('http:', 'https:', '//', 'data:')):
            asset_urls.add(src)
    # place cards links
    for m in re.finditer(r'href=["\'](/places/[^"\']+)["\']', html):
        endpoints_to_test.append(m.group(1))

print(f"Found {len(asset_urls)} unique internal assets. Testing a sample/all...")
broken_assets = []
for asset in sorted(asset_urls):
    if asset.startswith('/'):
        url = BASE_URL + asset
    else:
        url = BASE_URL + '/' + asset
    status, body, _ = check_url(url)
    if status != 200:
        print(f"❌ BROKEN ASSET: [{status}] {asset}")
        broken_assets.append((asset, status))
    else:
        # print(f"✓ [{status}] {asset}")
        pass

print(f"Tested {len(asset_urls)} assets. Broken: {len(broken_assets)}")

print("\n=== TESTING DETAIL PAGES FOUND ===")
detail_pages = set([ep for ep in endpoints_to_test if ep.startswith('/places/')])
print(f"Testing {len(detail_pages)} place detail pages...")
for dp in list(detail_pages)[:15]:
    status, body, _ = check_url(BASE_URL + dp)
    if status != 200:
        print(f"❌ BROKEN DETAIL PAGE: [{status}] {dp}")
    else:
        print(f"✓ [{status}] {dp}")
