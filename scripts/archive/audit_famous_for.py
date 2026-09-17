"""
Inspect descriptions, famous_for, and cover images across all 38 districts.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("SELECT id, name, slug, description, famous_for, cover_image FROM districts ORDER BY id")
districts = cur.fetchall()

print("=" * 120)
print("DISTRICT DESCRIPTIONS & FAMOUS_FOR AUDIT")
print("=" * 120)
for d in districts:
    print(f"ID {d['id']:2d} | Name: {d['name']:25s} | Slug: {d['slug']:20s} | Famous: {str(d['famous_for']):40s} | Desc: {str(d['description'])[:50]}")

cur.close()
conn.close()
