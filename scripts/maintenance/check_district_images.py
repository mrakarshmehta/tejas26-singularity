import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute('SELECT id, name, slug, cover_image, image_url FROM districts')
    dists = cur.fetchall()
    print('Districts count:', len(dists))
    for d in dists:
        print(f"{d['id']:2d} | {d['name']:20s} | cover: {str(d['cover_image']):30s} | url: {str(d['image_url'])[:40]}")
