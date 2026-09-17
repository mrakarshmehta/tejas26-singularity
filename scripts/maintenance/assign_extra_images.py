import os
import sys
import urllib.request
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from models.database import get_db

PLACES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads', 'places')

EXTRA_IMAGES = {
    7: {
        "name": "Great Buddha Statue",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Great_Buddha_Statue%2C_Bodh_Gaya_at_Sunset.jpg/1280px-Great_Buddha_Statue%2C_Bodh_Gaya_at_Sunset.jpg"
    },
    95: {
        "name": "Maner Sharif",
        "url": "https://images.unsplash.com/photo-1548013146-72479768bbaa?auto=format&fit=crop&w=1200&q=80"
    },
    96: {
        "name": "Patna Planetarium",
        "url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80"
    },
    97: {
        "name": "Padri Ki Haveli",
        "url": "https://images.unsplash.com/photo-1542385151-efd9000785a0?auto=format&fit=crop&w=1200&q=80"
    },
    102: {
        "name": "Royal Thai Monastery",
        "url": "https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=1200&q=80"
    }
}

def main():
    conn = get_db()
    cur = conn.cursor()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for pid, data in EXTRA_IMAGES.items():
        fname = f"{pid}_{hashlib.md5(data['name'].encode()).hexdigest()[:8]}.jpg"
        fpath = os.path.join(PLACES_DIR, fname)
        try:
            req = urllib.request.Request(data['url'], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
                with open(fpath, 'wb') as f:
                    f.write(content)
                cur.execute("UPDATE places SET cover_image = %s WHERE id = %s", (fname, pid))
                print(f"[SAVED] Place {pid} ({data['name']}) -> {fname}")
        except Exception as e:
            print(f"[ERROR] Place {pid}: {e}")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
