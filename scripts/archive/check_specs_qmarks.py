import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute("DESCRIBE specialties")
    for c in cur.fetchall():
        print(f"  {c['Field']:25s} | {c['Type']}")
    
    cur.execute("SELECT * FROM specialties")
    specs = cur.fetchall()
    print(f"\nTotal specialties: {len(specs)}")
    for s in specs:
        for k, v in s.items():
            if isinstance(v, str) and '???' in v:
                print(f"  Spec #{s['id']} {s['name']} [{k}]: {repr(v)}")
