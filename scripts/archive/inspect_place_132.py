import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cursor:
    cursor.execute("SELECT * FROM places WHERE id = 132")
    row = cursor.fetchone()
    for k, v in row.items():
        print(f"{k:20}: {repr(v)}")
