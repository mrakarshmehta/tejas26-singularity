import sys, os
sys.path.insert(0, os.path.abspath('.'))
from dotenv import load_dotenv
load_dotenv()

from models.connection import get_cursor

def check_places_cols():
    with get_cursor() as cur:
        cur.execute("DESCRIBE `places`")
        for c in cur.fetchall():
            print(f"places col: {c['Field']:20s} {c['Type']}")
        cur.execute("DESCRIBE `districts`")
        for c in cur.fetchall():
            print(f"districts col: {c['Field']:20s} {c['Type']}")

check_places_cols()
