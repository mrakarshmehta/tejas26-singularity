import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

with get_cursor() as cursor:
    cursor.execute("SELECT id, name FROM districts ORDER BY id")
    for r in cursor.fetchall():
        print(f"{r['id']:2d}: {r['name']}")
