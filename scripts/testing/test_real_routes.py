import urllib.request
import urllib.error
import time

BASE_URL = "https://hiddenyatra.onrender.com"

actual_routes = [
    "/health",
    "/",
    "/browse",
    "/state/bihar",
    "/explore",
    "/explore/map",
    "/food-culture",
    "/search",
    "/stays",
    "/host",
    "/community",
    "/itinerary",
    "/wishlist",
    "/login",
    "/signup",
    "/api/search/instant?q=patna",
    "/api/smart-nearby?lat=25.5941&lng=85.1376",
    "/sitemap.xml",
    "/robots.txt",
    "/sw.js",
]

print("=== TESTING REAL APPLICATION ROUTES ===")
for ep in actual_routes:
    url = BASE_URL + ep
    start = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            dur = time.time() - start
            data = resp.read()
            print(f"✓ [{resp.status}] {ep} -> {len(data)} bytes in {dur:.2f}s", flush=True)
    except urllib.error.HTTPError as e:
        dur = time.time() - start
        body = e.read()
        print(f"❌ [HTTP {e.code}] {ep} -> {len(body)} bytes in {dur:.2f}s", flush=True)
    except Exception as e:
        dur = time.time() - start
        print(f"⚠️ [ERROR {type(e).__name__}] {ep} -> in {dur:.2f}s: {e}", flush=True)
