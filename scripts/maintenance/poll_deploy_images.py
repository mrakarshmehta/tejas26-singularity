"""
Poll Render until commit 104435c deployment is complete and images return HTTP 200.
"""
import urllib.request
import time

test_url = "https://hiddenyatra.onrender.com/static/uploads/places/57_3edc98f203.png"

print("Waiting for Render to finish building and deploying commit 104435c...")
for attempt in range(1, 30):
    try:
        req = urllib.request.Request(test_url + f"?cache_bust={time.time()}", headers={'User-Agent': 'Verifier/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print(f"\n>>> SUCCESS! Deploy completed. Image returned HTTP 200 OK (size: {len(resp.read())} bytes)")
                break
    except urllib.error.HTTPError as e:
        print(f"Attempt {attempt:2d}: HTTP {e.code} (deploy in progress...)")
    except Exception as e:
        print(f"Attempt {attempt:2d}: {e}")
    time.sleep(10)
