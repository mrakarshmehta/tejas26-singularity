import urllib.request
import urllib.error
import time
import sys

BASE_URL = "https://hiddenyatra.onrender.com"

endpoints = [
    "/health",
    "/api/categories",
    "/api/districts",
    "/login",
    "/signup",
    "/places",
    "/map",
    "/stays",
    "/host",
    "/community",
    "/itinerary",
    "/wishlist",
    "/",
]

for ep in endpoints:
    url = BASE_URL + ep
    start = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    print(f"Testing {ep}...", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            dur = time.time() - start
            data = resp.read()
            print(f"  -> [SUCCESS {resp.status}] {ep} ({len(data)} bytes in {dur:.2f}s)", flush=True)
    except urllib.error.HTTPError as e:
        dur = time.time() - start
        body = e.read()
        print(f"  -> [HTTP {e.code}] {ep} ({len(body)} bytes in {dur:.2f}s): {body[:80]}", flush=True)
    except Exception as e:
        dur = time.time() - start
        print(f"  -> [ERROR {type(e).__name__}] {ep} (in {dur:.2f}s): {e}", flush=True)

print("Done testing!", flush=True)
