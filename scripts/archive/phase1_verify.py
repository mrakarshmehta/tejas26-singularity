"""
Phase 1 & Phase 2 verification script - 100% READ ONLY.
Verifies backup integrity and extracts full database state.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

backup_path = r"D:\HiddenYatra\scratch\backup_hiddenyatra_20260814_1934.sql"
print("=== PHASE 1: BACKUP VERIFICATION ===")
if os.path.exists(backup_path):
    size = os.path.getsize(backup_path)
    print(f"Backup file exists: {backup_path}")
    print(f"Backup size: {size:,} bytes ({size/1024:.2f} KB)")
    with open(backup_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    table_creates = [l.strip() for l in lines if l.startswith("CREATE TABLE")]
    print(f"Total lines in backup: {len(lines):,}")
    print(f"Total tables backed up: {len(table_creates)}")
else:
    print(f"ERROR: Backup file not found at {backup_path}")

print("\n=== CURRENT LIVE DATABASE CONNECTION & STATS ===")
conn = get_db()
cur = conn.cursor()

cur.execute("SELECT DATABASE() AS db, USER() AS user, VERSION() AS ver")
info = cur.fetchone()
print(f"Database: {info['db']} | User: {info['user']} | Version: {info['ver']}")

cur.execute("SHOW TABLES")
tables = [list(r.values())[0] for r in cur.fetchall()]
print(f"Total tables in live DB: {len(tables)}")

table_counts = {}
for t in tables:
    cur.execute(f"SELECT COUNT(*) AS c FROM `{t}`")
    table_counts[t] = cur.fetchone()['c']

print("Table row counts:")
for t, c in sorted(table_counts.items()):
    print(f"  - {t:25s}: {c:5d} rows")

cur.close()
conn.close()
