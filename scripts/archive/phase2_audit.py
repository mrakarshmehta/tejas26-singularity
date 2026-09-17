"""
PHASE 2+3: Complete read-only audit + canonical mapping.
Shows all FK constraints, all district_id references, and builds the canonical fix plan.
"""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

# ──────────────────────────────────────────────
# A. Foreign Key constraints referencing districts
# ──────────────────────────────────────────────
print("=" * 90)
print("A. ALL FOREIGN KEY CONSTRAINTS REFERENCING districts TABLE")
print("=" * 90)
cur.execute("""
    SELECT kcu.TABLE_NAME, kcu.COLUMN_NAME, kcu.CONSTRAINT_NAME,
           kcu.REFERENCED_TABLE_NAME, kcu.REFERENCED_COLUMN_NAME,
           rc.DELETE_RULE, rc.UPDATE_RULE
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
    JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
         ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
         AND kcu.CONSTRAINT_SCHEMA = rc.CONSTRAINT_SCHEMA
    WHERE kcu.REFERENCED_TABLE_NAME = 'districts'
      AND kcu.CONSTRAINT_SCHEMA = 'hiddenyatra'
""")
fk_rows = cur.fetchall()
for fk in fk_rows:
    print(f"  Table={fk['TABLE_NAME']:25s} Col={fk['COLUMN_NAME']:15s} "
          f"FK={fk['CONSTRAINT_NAME']:35s} "
          f"OnDelete={fk.get('DELETE_RULE','?'):10s} OnUpdate={fk.get('UPDATE_RULE','?')}")

# ──────────────────────────────────────────────
# B. All tables with a district_id column
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("B. ALL TABLES WITH district_id COLUMN")
print("=" * 90)
cur.execute("""
    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE COLUMN_NAME = 'district_id'
      AND TABLE_SCHEMA = 'hiddenyatra'
""")
for col in cur.fetchall():
    print(f"  Table={col['TABLE_NAME']:25s} Type={col['DATA_TYPE']:10s} Nullable={col['IS_NULLABLE']}")

# ──────────────────────────────────────────────
# C. Record counts per table with district_id
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("C. RECORD COUNTS IN DISTRICT-DEPENDENT TABLES")
print("=" * 90)
district_tables = ['places', 'blocks', 'district_foods', 'nearby_services',
                   'accommodations', 'specialties', 'photos', 'reviews',
                   'trending_places', 'local_experiences']
for t in district_tables:
    try:
        cur.execute(f"SELECT COUNT(*) AS cnt FROM `{t}`")
        cnt = cur.fetchone()['cnt']
        cur.execute(f"SELECT COUNT(DISTINCT district_id) AS dc FROM `{t}` WHERE district_id IS NOT NULL")
        dc = cur.fetchone()['dc']
        print(f"  {t:25s} → {cnt:5d} rows, {dc:3d} distinct district_ids")
    except Exception as e:
        print(f"  {t:25s} → (error or no district_id: {e})")

# ──────────────────────────────────────────────
# D. COMPLETE DISTRICT TABLE
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("D. COMPLETE DISTRICTS TABLE (PRE-FIX STATE)")
print("=" * 90)
cur.execute("SELECT * FROM districts ORDER BY id")
districts = cur.fetchall()
for d in districts:
    print(f"  ID={d['id']:3d} | Name={d['name']:25s} | Slug={d['slug']:25s} | "
          f"Desc={str(d.get('description',''))[:50]}...")

# ──────────────────────────────────────────────
# E. ALL PLACES (PRE-FIX) with district assignment
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("E. ALL PLACES WITH CURRENT DISTRICT ASSIGNMENT")
print("=" * 90)
cur.execute("""
    SELECT p.id, p.name, p.slug AS place_slug, p.district_id, p.category,
           p.deleted_at,
           d.name AS dist_name, d.slug AS dist_slug
    FROM places p
    LEFT JOIN districts d ON p.district_id = d.id
    ORDER BY p.id
""")
places = cur.fetchall()
for p in places:
    flag = ""
    if p['district_id'] is None: flag += " ⚠️NULL_DIST"
    if not p['name'] or p['name'].strip() == '': flag += " ⚠️EMPTY_NAME"
    if p['deleted_at']: flag += " 🗑️DEL"
    print(f"  PID={p['id']:4d} | DID={str(p['district_id']):5s} | "
          f"DistName={str(p.get('dist_name','')):25s} | DistSlug={str(p.get('dist_slug','')):20s} | "
          f"PlaceName={str(p['name']):45s} | Cat={str(p['category']):15s}{flag}")

# ──────────────────────────────────────────────
# F. ALL BLOCKS (PRE-FIX)
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("F. ALL BLOCKS WITH CURRENT DISTRICT ASSIGNMENT")
print("=" * 90)
cur.execute("""
    SELECT b.id, b.name, b.slug, b.district_id,
           d.name AS dist_name, d.slug AS dist_slug
    FROM blocks b
    LEFT JOIN districts d ON b.district_id = d.id
    ORDER BY b.district_id, b.id
""")
for b in cur.fetchall():
    print(f"  BID={b['id']:4d} | DID={b['district_id']:3d} | "
          f"DistName={str(b.get('dist_name','')):25s} | DistSlug={str(b.get('dist_slug','')):20s} | "
          f"Block={b['name']}")

# ──────────────────────────────────────────────
# G. DISTRICT FOODS (PRE-FIX)
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("G. DISTRICT FOODS WITH CURRENT ASSIGNMENT")
print("=" * 90)
cur.execute("""
    SELECT df.id, df.district_id, d.name AS dist_name, d.slug AS dist_slug,
           df.name AS food_name
    FROM district_foods df
    LEFT JOIN districts d ON df.district_id = d.id
    ORDER BY df.district_id, df.id
""")
for f in cur.fetchall():
    print(f"  FID={f['id']:4d} | DID={f['district_id']:3d} | "
          f"DistName={str(f.get('dist_name','')):25s} | Food={f['food_name']}")

# ──────────────────────────────────────────────
# H. NEARBY SERVICES (PRE-FIX)
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("H. NEARBY SERVICES WITH CURRENT ASSIGNMENT (by district)")
print("=" * 90)
cur.execute("""
    SELECT ns.district_id, d.name AS dist_name, d.slug AS dist_slug,
           COUNT(*) AS cnt,
           GROUP_CONCAT(ns.name SEPARATOR ', ') AS svc_names
    FROM nearby_services ns
    LEFT JOIN districts d ON ns.district_id = d.id
    GROUP BY ns.district_id
    ORDER BY ns.district_id
""")
for row in cur.fetchall():
    print(f"  DID={row['district_id']:3d} | DistName={str(row.get('dist_name','')):25s} | "
          f"Count={row['cnt']:3d} | Services={str(row['svc_names'])[:80]}...")

# ──────────────────────────────────────────────
# I. ACCOMMODATIONS (PRE-FIX)
# ──────────────────────────────────────────────
print("\n" + "=" * 90)
print("I. ACCOMMODATIONS WITH DISTRICT ASSIGNMENT")
print("=" * 90)
try:
    cur.execute("""
        SELECT a.id, a.name, a.district_id, d.name AS dist_name
        FROM accommodations a
        LEFT JOIN districts d ON a.district_id = d.id
        ORDER BY a.district_id, a.id
    """)
    for a in cur.fetchall():
        print(f"  AID={a['id']:4d} | DID={str(a.get('district_id','')):5s} | "
              f"DistName={str(a.get('dist_name','')):25s} | Name={a['name']}")
except Exception as e:
    print(f"  (error: {e})")

cur.close()
conn.close()
print("\n" + "=" * 90)
print("PHASE 2 AUDIT COMPLETE — ALL READ-ONLY")
print("=" * 90)
