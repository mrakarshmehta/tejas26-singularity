"""Check other district-dependent tables."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

for tbl in ['host_listings', 'host_profiles', 'local_experiences']:
    cur.execute(f"SELECT COUNT(*) AS cnt FROM {tbl}")
    cnt = cur.fetchone()['cnt']
    print(f"Table: {tbl} -> {cnt} rows")
    if cnt > 0:
        cur.execute(f"SELECT * FROM {tbl} LIMIT 5")
        for r in cur.fetchall():
            print(f"  {r}")

cur.close()
conn.close()
