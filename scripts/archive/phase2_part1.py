"""
Extract specific Phase 2 details:
- FK constraints
- Districts complete list
- Specific districts deep dive
- All places with expected vs current district
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

print("--- 1. FK CONSTRAINTS REFERENCING DISTRICTS ---")
cur.execute("""
    SELECT kcu.TABLE_NAME, kcu.COLUMN_NAME, kcu.CONSTRAINT_NAME,
           rc.DELETE_RULE, rc.UPDATE_RULE
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
    JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
         ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
         AND kcu.CONSTRAINT_SCHEMA = rc.CONSTRAINT_SCHEMA
    WHERE kcu.REFERENCED_TABLE_NAME = 'districts'
      AND kcu.CONSTRAINT_SCHEMA = 'hiddenyatra'
""")
for r in cur.fetchall():
    print(f"  Table: {r['TABLE_NAME']:20s} | Col: {r['COLUMN_NAME']:15s} | FK: {r['CONSTRAINT_NAME']:30s} | OnDel: {r['DELETE_RULE']:10s} | OnUpd: {r['UPDATE_RULE']}")

print("\n--- 2. ALL TABLES WITH district_id ---")
cur.execute("""
    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE COLUMN_NAME = 'district_id' AND TABLE_SCHEMA = 'hiddenyatra'
""")
for r in cur.fetchall():
    print(f"  Table: {r['TABLE_NAME']:20s} | Type: {r['DATA_TYPE']:10s} | Nullable: {r['IS_NULLABLE']}")

print("\n--- 3. ALL DISTRICTS IN DB (39 rows) ---")
cur.execute("SELECT id, state_id, name, slug, cover_image, image_url FROM districts ORDER BY id")
for d in cur.fetchall():
    print(f"  ID: {d['id']:2d} | StateID: {d['state_id']} | Name: {d['name']:25s} | Slug: {d['slug']:25s} | CoverImg: {str(d.get('cover_image',''))[:30]}")

cur.close()
conn.close()
