import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute("DESCRIBE places")
    print("places columns:")
    for c in cur.fetchall():
        print(f"  {c['Field']:25s} | {c['Type']}")
