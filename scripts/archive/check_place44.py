import sys, os
sys.path.insert(0, os.path.abspath('.'))
from dotenv import load_dotenv
load_dotenv()

from models.connection import get_cursor

def check_place44():
    with get_cursor() as cur:
        cur.execute("SELECT * FROM places WHERE id = 44")
        row = cur.fetchone()
        print("=== PLACE ID 44 DETAILS ===")
        print(row)

check_place44()
