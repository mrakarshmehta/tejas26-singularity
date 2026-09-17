import urllib.request
import re

pages = [
    'http://127.0.0.1:5000/',
    'http://127.0.0.1:5000/state/bihar',
    'http://127.0.0.1:5000/district/patna',
    'http://127.0.0.1:5000/place/golghar'
]

print("=" * 60)
print("  FRONTEND IMAGE RENDERING & HTTP STATUS CHECK")
print("=" * 60)

for url in pages:
    print(f"\nTesting page: {url}")
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        # Find img src and css url()
        img_srcs = re.findall(r'src=["\']([^"\']+)["\']', html)
        css_urls = re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', html)
        all_sources = list(set(img_srcs + css_urls))

        image_urls = [s for s in all_sources if 'upload' in s or 'static' in s or 'unsplash' in s or 'wikimedia' in s]
        print(f"  Found {len(image_urls)} image references.")

        failed = []
        for img in image_urls:
            full_url = img if img.startswith('http') else f"http://127.0.0.1:5000{img if img.startswith('/') else '/' + img}"
            try:
                req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
                res = urllib.request.urlopen(req, timeout=3)
                if res.getcode() != 200:
                    failed.append((img, res.getcode()))
            except Exception as e:
                failed.append((img, str(e)))

        if failed:
            print(f"  [FAILED IMAGES]: {len(failed)}")
            for f, err in failed:
                print(f"    - {f}: {err}")
        else:
            print(f"  [PASSED] All {len(image_urls)} images returned HTTP 200 OK.")
    except Exception as e:
        print(f"  [ERROR] Page failed: {e}")

print("=" * 60)
