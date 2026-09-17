"""Quick schema check for districts table."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("SHOW CREATE TABLE districts")
row = cur.fetchone()
print(row['Create Table'])

print("\n--- SHOW INDEX FROM districts ---")
cur.execute("SHOW INDEX FROM districts")
for idx in cur.fetchall():
    print(f"  Key={idx['Key_name']:30s} | Column={idx['Column_name']:15s} | Unique={not idx['Non_unique']}")

cur.close()
conn.close()
