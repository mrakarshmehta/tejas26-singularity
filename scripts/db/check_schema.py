import sys, os
sys.path.insert(0, os.path.abspath('.'))
from dotenv import load_dotenv
load_dotenv()

from models.connection import get_cursor

def check_schema():
    with get_cursor() as cur:
        cur.execute("SHOW TABLES")
        tables = [list(row.values())[0] for row in cur.fetchall()]
        print("=== DATABASE TABLES ===")
        for t in tables:
            print(f"Table: {t}")
            cur.execute(f"DESCRIBE `{t}`")
            cols = cur.fetchall()
            for c in cols:
                print(f"   {c['Field']:20s} {c['Type']:20s} Null={c['Null']} Key={c['Key']}")

check_schema()
