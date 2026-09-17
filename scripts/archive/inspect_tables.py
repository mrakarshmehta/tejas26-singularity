import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

tables = ['stay_requests']
with get_cursor() as cur:
    for tbl in tables:
        cur.execute(f"DESCRIBE {tbl};")
        cols = cur.fetchall()
        print(f"\n=== {tbl} ===")
        for c in cols:
            print(f"  {c['Field']:25s} {c['Type']:35s} Null={c['Null']:3s} Default={str(c['Default']):10s}")
