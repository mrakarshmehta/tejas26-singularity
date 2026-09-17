"""
Audit places 1-28 for name/slug consistency.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("SELECT id, name, slug, district_id, category FROM places WHERE id <= 30 ORDER BY id")
for p in cur.fetchall():
    print(f"ID {p['id']:2d} | Name: {p['name']:42s} | Slug: {p['slug']:35s} | DID: {p['district_id']}")

cur.close()
conn.close()
