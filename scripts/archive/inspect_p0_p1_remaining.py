import csv, sys, os, pymysql, dotenv
dotenv.load_dotenv()

conn = pymysql.connect(
    host=os.getenv('DB_HOST','127.0.0.1'),
    port=int(os.getenv('DB_PORT',3307)),
    user=os.getenv('DB_USER','root'),
    password=os.getenv('DB_PASSWORD',''),
    database=os.getenv('DB_NAME','hiddenyatra'),
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()
cur.execute("SELECT id, name, slug, category, latitude, longitude, district_id FROM places WHERE deleted_at IS NULL")
active = cur.fetchall()
active_names = {p['name'].lower().strip(): p for p in active}

with open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', 'r', encoding='utf-8', errors='ignore') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in PHASE5_MASTER: {len(rows)}")

p0_p1 = [r for r in rows if r.get('recommended_priority') in ['P0', 'P1']]
print(f"Total P0/P1 candidates in PHASE5_MASTER: {len(p0_p1)}")

uninserted_p0_p1 = []
for r in p0_p1:
    name = r.get('place_name', '').strip()
    name_l = name.lower()
    
    # check if in active
    match = None
    for p in active:
        if name_l == p['name'].lower().strip() or (name_l in p['name'].lower()) or (p['name'].lower() in name_l and len(name_l) > 10):
            match = p
            break
            
    if not match:
        uninserted_p0_p1.append(r)

print(f"Uninserted P0/P1 candidates: {len(uninserted_p0_p1)}")
print("-" * 80)
for r in uninserted_p0_p1:
    print(f"[{r.get('recommended_priority')}] [{r.get('district')}] {r.get('place_name')} | Cat: {r.get('category')} | Coords: {r.get('coordinates')}")
    print(f"   Primary: {r.get('primary_source')}")
    print(f"   Secondary: {r.get('secondary_source')}")
    print(f"   Reason: {r.get('reason')}")
    print()
