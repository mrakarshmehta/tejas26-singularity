"""
Compare local database vs live Render for Jamui and Gaya.
"""
import os, sys
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from models.connection import get_cursor

def list_all_districts():
    with get_cursor() as cur:
        cur.execute("SELECT id, name, slug, cover_image FROM districts ORDER BY id")
        districts = cur.fetchall()
        print(f"Total districts in local DB: {len(districts)}")
        for d in districts:
            cur.execute("SELECT count(*) as cnt FROM places WHERE district_id=%s", (d['id'],))
            cnt = cur.fetchone()['cnt']
            print(f"  - ID {d['id']:2d}: {d['name']:15s} (slug: {d['slug']:15s}, places: {cnt:2d}, img: {d['cover_image']})")

if __name__ == '__main__':
    list_all_districts()
