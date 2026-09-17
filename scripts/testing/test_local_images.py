import urllib.request
import re

pages = [
    'http://127.0.0.1:5000/',
    'http://127.0.0.1:5000/state/bihar',
    'http://127.0.0.1:5000/state/bihar/patna',
    'http://127.0.0.1:5000/place/golghar',
    'http://127.0.0.1:5000/admin/login'
]

print("=" * 60)
print("  FULL END-TO-END FRONTEND STATIC IMAGE RENDERING CHECK")
print("=" * 60)

for url in pages:
    print(f"\nTesting page: {url}")
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        img_srcs = re.findall(r'src=["\']([^"\']+)["\']', html)
        css_urls = re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', html)
        all_sources = list(set(img_srcs + css_urls))

        local_images = [s for s in all_sources if s.startswith('/static/')]
        print(f"  Found {len(local_images)} local static image references.")

        failed = []
        for img in local_images:
            full_url = f"http://127.0.0.1:5000{img}"
            try:
                res = urllib.request.urlopen(full_url, timeout=2)
                if res.getcode() != 200:
                    failed.append((img, res.getcode()))
            except Exception as e:
                failed.append((img, str(e)))

        if failed:
            print(f"  [FAILED LOCAL IMAGES]: {len(failed)}")
            for f, err in failed:
                print(f"    - {f}: {err}")
        else:
            print(f"  [PASSED] All {len(local_images)} local static images returned HTTP 200 OK.")
    except Exception as e:
        print(f"  [ERROR] Page failed: {e}")

print("=" * 60)
