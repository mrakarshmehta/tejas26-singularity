import os
import urllib.request
import hashlib
from dotenv import load_dotenv

load_dotenv()

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db

PLACES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads', 'places')

def main():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, cover_image FROM places WHERE cover_image LIKE 'http%'")
    remote_places = cur.fetchall()
    print(f"Found {len(remote_places)} places with remote URLs. Converting to local cached JPGs...")

    headers = {
        'User-Agent': 'HiddenYatraBot/1.0 (https://hiddenyatra.onrender.com; info@hiddenyatra.in) python-urllib/3.13',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    }

    converted = 0
    for p in remote_places:
        pid = p['id']
        name = p['name']
        url = p['cover_image']
        fname = f"{pid}_{hashlib.md5(name.encode()).hexdigest()[:8]}.jpg"
        fpath = os.path.join(PLACES_DIR, fname)

        # Download with proper Wikimedia user-agent
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                if len(data) > 1000:
                    with open(fpath, 'wb') as f:
                        f.write(data)
                    cur.execute("UPDATE places SET cover_image = %s WHERE id = %s", (fname, pid))
                    converted += 1
                    print(f"  [SAVED LOCAL] Place {pid} ({name}) -> {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"  [RETRYING UNSPLASH FALLBACK] Place {pid} ({name}): {e}")
            fallback_url = "https://images.unsplash.com/photo-1548013146-72479768bbaa?auto=format&fit=crop&w=1200&q=80"
            try:
                req = urllib.request.Request(fallback_url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read()
                    with open(fpath, 'wb') as f:
                        f.write(data)
                    cur.execute("UPDATE places SET cover_image = %s WHERE id = %s", (fname, pid))
                    converted += 1
                    print(f"  [SAVED FALLBACK] Place {pid} ({name}) -> {fname}")
            except Exception as e2:
                print(f"  [ERROR] Place {pid}: {e2}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\nAll done! Successfully saved {converted} local place images.")

if __name__ == '__main__':
    main()
