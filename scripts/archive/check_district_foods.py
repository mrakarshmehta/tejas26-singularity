import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute("DESCRIBE district_foods")
    print("district_foods schema:")
    for col in cur.fetchall():
        print(f"  {col['Field']:20s} | {col['Type']}")
    
    cur.execute("SELECT * FROM district_foods LIMIT 5")
    rows = cur.fetchall()
    print("\nSample rows:")
    for r in rows:
        print(f"#{r['id']} {r['name']} | desc: {repr(r['description'][:60])} | best_place: {repr(r.get('best_place', ''))}")
