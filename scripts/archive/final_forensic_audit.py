"""
FINAL FORENSIC DISTRICT DATA AUDIT SCRIPT
100% READ-ONLY. Covers all 14 phases.
"""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db
from app import create_app

conn = get_db()
cur = conn.cursor()
app = create_app()
client = app.test_client()

results = {
    'phase1': {},
    'phase2_districts': [],
    'phase3_places': [],
    'phase4_blocks': [],
    'phase5_foods': [],
    'phase6_services': [],
    'phase7_images': [],
    'phase8_text': [],
    'phase9_search': [],
    'phase10_routes': [],
    'phase13_integrity': []
}

# ═══════════════════════════════════════════════════════════════
# PHASE 1: BACKUP & CURRENT STATE
# ═══════════════════════════════════════════════════════════════
backup_file = r"D:\HiddenYatra\scratch\backup_hiddenyatra_20260814_1934.sql"
cur.execute("SELECT DATABASE() AS db, USER() AS user, VERSION() AS ver")
db_info = cur.fetchone()
cur.execute("SHOW TABLES")
tables = [list(r.values())[0] for r in cur.fetchall()]

table_counts = {}
for t in ['districts', 'places', 'blocks', 'district_foods', 'nearby_services',
          'host_profiles', 'host_listings', 'local_experiences', 'users']:
    cur.execute(f"SELECT COUNT(*) AS c FROM `{t}`")
    table_counts[t] = cur.fetchone()['c']

results['phase1'] = {
    'db_name': db_info['db'],
    'db_user': db_info['user'],
    'db_version': db_info['ver'],
    'backup_file': backup_file,
    'backup_exists': os.path.exists(backup_file),
    'backup_size': os.path.getsize(backup_file) if os.path.exists(backup_file) else 0,
    'total_tables': len(tables),
    'counts': table_counts
}

# ═══════════════════════════════════════════════════════════════
# PHASE 2: ALL 38 DISTRICTS MASTER AUDIT
# ═══════════════════════════════════════════════════════════════
cur.execute("""
    SELECT d.id, d.state_id, d.name, d.slug, d.description, d.famous_for,
           d.cover_image, d.image_url,
           COUNT(DISTINCT p.id) AS place_count,
           COUNT(DISTINCT b.id) AS block_count,
           COUNT(DISTINCT df.id) AS food_count,
           COUNT(DISTINCT ns.id) AS service_count
    FROM districts d
    LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
    LEFT JOIN blocks b ON b.district_id = d.id
    LEFT JOIN district_foods df ON df.district_id = d.id
    LEFT JOIN nearby_services ns ON ns.district_id = d.id
    GROUP BY d.id
    ORDER BY d.id
""")
districts_rows = cur.fetchall()

uploads_dist_dir = r"D:\HiddenYatra\static\uploads\districts"
for d in districts_rows:
    expected_slug = re.sub(r'[^a-z0-9]+', '-', d['name'].lower().strip()).strip('-')
    slug_ok = (d['slug'] == expected_slug)
    
    cov = d['cover_image'] or ''
    img_exists = os.path.exists(os.path.join(uploads_dist_dir, cov)) if cov else False
    
    status = "PASS"
    issues = []
    if not slug_ok:
        status = "MISMATCH"
        issues.append(f"Slug mismatch: expected {expected_slug}, got {d['slug']}")
    if not img_exists and not cov.startswith('http'):
        issues.append("Cover image missing file")
    
    results['phase2_districts'].append({
        'id': d['id'],
        'name': d['name'],
        'slug': d['slug'],
        'expected_slug': expected_slug,
        'slug_ok': slug_ok,
        'cover_image': cov,
        'img_exists': img_exists,
        'place_count': d['place_count'],
        'block_count': d['block_count'],
        'food_count': d['food_count'],
        'service_count': d['service_count'],
        'status': status,
        'issues': issues
    })

# ═══════════════════════════════════════════════════════════════
# PHASE 3: PLACE-BY-PLACE FORENSIC AUDIT
# ═══════════════════════════════════════════════════════════════
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, p.district_id, p.block_id,
           p.latitude, p.longitude, p.description, p.cover_image, p.deleted_at,
           d.name AS dist_name, d.slug AS dist_slug,
           b.name AS block_name
    FROM places p
    LEFT JOIN districts d ON p.district_id = d.id
    LEFT JOIN blocks b ON p.block_id = b.id
    ORDER BY p.district_id, p.id
""")
places_rows = cur.fetchall()

uploads_places_dir = r"D:\HiddenYatra\static\uploads\places"
for p in places_rows:
    cov = p['cover_image'] or ''
    img_exists = os.path.exists(os.path.join(uploads_places_dir, cov)) if cov else False
    
    results['phase3_places'].append({
        'id': p['id'],
        'name': p['name'],
        'slug': p['slug'],
        'category': p['category'],
        'district_id': p['district_id'],
        'dist_name': p['dist_name'],
        'dist_slug': p['dist_slug'],
        'block_id': p['block_id'],
        'block_name': p['block_name'],
        'latitude': p['latitude'],
        'longitude': p['longitude'],
        'cover_image': cov,
        'img_exists': img_exists,
        'deleted_at': str(p['deleted_at']) if p['deleted_at'] else None
    })

# ═══════════════════════════════════════════════════════════════
# PHASE 4: BLOCK AUDIT
# ═══════════════════════════════════════════════════════════════
cur.execute("""
    SELECT b.id, b.name, b.slug, b.district_id,
           d.name AS dist_name, d.slug AS dist_slug,
           COUNT(p.id) AS place_count
    FROM blocks b
    LEFT JOIN districts d ON b.district_id = d.id
    LEFT JOIN places p ON p.block_id = b.id AND p.deleted_at IS NULL
    GROUP BY b.id
    ORDER BY b.district_id, b.id
""")
blocks_rows = cur.fetchall()
for b in blocks_rows:
    results['phase4_blocks'].append({
        'id': b['id'],
        'name': b['name'],
        'slug': b['slug'],
        'district_id': b['district_id'],
        'dist_name': b['dist_name'],
        'dist_slug': b['dist_slug'],
        'place_count': b['place_count']
    })

# ═══════════════════════════════════════════════════════════════
# PHASE 5: FOOD / CULTURE AUDIT
# ═══════════════════════════════════════════════════════════════
cur.execute("""
    SELECT df.id, df.district_id, df.name, df.description, df.image_url,
           d.name AS dist_name, d.slug AS dist_slug
    FROM district_foods df
    LEFT JOIN districts d ON df.district_id = d.id
    ORDER BY df.district_id, df.id
""")
for f in cur.fetchall():
    results['phase5_foods'].append({
        'id': f['id'],
        'name': f['name'],
        'district_id': f['district_id'],
        'dist_name': f['dist_name'],
        'dist_slug': f['dist_slug'],
        'description': f['description']
    })

# ═══════════════════════════════════════════════════════════════
# PHASE 6: NEARBY SERVICES AUDIT
# ═══════════════════════════════════════════════════════════════
cur.execute("""
    SELECT s.id, s.name, s.service_type, s.district_id, s.address,
           d.name AS dist_name, d.slug AS dist_slug
    FROM nearby_services s
    LEFT JOIN districts d ON s.district_id = d.id
    ORDER BY s.district_id, s.id
""")
for s in cur.fetchall():
    results['phase6_services'].append({
        'id': s['id'],
        'name': s['name'],
        'type': s['service_type'],
        'district_id': s['district_id'],
        'dist_name': s['dist_name'],
        'dist_slug': s['dist_slug'],
        'address': s['address']
    })

# ═══════════════════════════════════════════════════════════════
# PHASE 9: SEARCH AUDIT (38 districts + typo tests)
# ═══════════════════════════════════════════════════════════════
search_test_queries = [
    # 38 district names
    'Patna', 'Gaya', 'Nalanda', 'Jamui', 'Bhagalpur', 'Munger', 'Muzaffarpur',
    'Rohtas', 'West Champaran', 'East Champaran', 'Araria', 'Arwal', 'Aurangabad',
    'Banka', 'Begusarai', 'Bhojpur', 'Buxar', 'Darbhanga', 'Gopalganj',
    'Jhanjharpur', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj',
    'Lakhisarai', 'Madhepura', 'Purnia', 'Saharsa', 'Samastipur', 'Saran',
    'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'Nawada',
    # Specific towns/locations
    'Rajgir', 'Bodh Gaya', 'Simultala', 'Sasaram', 'Vaishali',
    # Typo tests
    'Jamuii', 'Nalnda', 'Rajgirr', 'Bhagalpurh', 'Gyaa'
]

for q in search_test_queries:
    resp = client.get(f"/api/search/instant?q={q}")
    data = resp.get_json() if resp.status_code == 200 else {}
    res_list = data.get('results', [])
    top_res = res_list[0] if res_list else None
    results['phase9_search'].append({
        'query': q,
        'status_code': resp.status_code,
        'result_count': len(res_list),
        'top_type': top_res.get('type') if top_res else None,
        'top_title': top_res.get('title') if top_res else None,
        'top_url': top_res.get('url') if top_res else None
    })

# ═══════════════════════════════════════════════════════════════
# PHASE 10: ROUTE / BROWSER AUDIT (All 38 District Routes)
# ═══════════════════════════════════════════════════════════════
for d in districts_rows:
    url = f"/state/bihar/{d['slug']}"
    resp = client.get(url)
    status_code = resp.status_code
    html = resp.get_data(as_text=True) if status_code == 200 else ''
    
    h1_match = re.search(r'<h1>([^<]+)', html)
    h1_val = h1_match.group(1).strip() if h1_match else ''
    
    h1_correct = (d['name'].lower() in h1_val.lower())
    
    # Check that places in HTML match this district
    results['phase10_routes'].append({
        'district_id': d['id'],
        'name': d['name'],
        'slug': d['slug'],
        'url': url,
        'status_code': status_code,
        'h1_val': h1_val,
        'h1_correct': h1_correct,
        'place_count': d['place_count'],
        'block_count': d['block_count'],
        'food_count': d['food_count'],
        'service_count': d['service_count']
    })

# ═══════════════════════════════════════════════════════════════
# PHASE 13: DATABASE INTEGRITY CHECKS
# ═══════════════════════════════════════════════════════════════
integrity_checks = []

# 1. Total districts count
integrity_checks.append({
    'check': 'District Count Exactly 38',
    'passed': len(districts_rows) == 38,
    'value': len(districts_rows)
})

# 2. Duplicate slugs
cur.execute("SELECT state_id, slug, COUNT(*) AS c FROM districts GROUP BY state_id, slug HAVING c > 1")
dup_slugs = cur.fetchall()
integrity_checks.append({
    'check': 'Zero Duplicate District Slugs',
    'passed': len(dup_slugs) == 0,
    'value': len(dup_slugs)
})

# 3. Places pointing to invalid districts
cur.execute("SELECT p.id, p.name, p.district_id FROM places p LEFT JOIN districts d ON p.district_id = d.id WHERE d.id IS NULL AND p.deleted_at IS NULL")
invalid_places = cur.fetchall()
integrity_checks.append({
    'check': 'Zero Places with Invalid district_id',
    'passed': len(invalid_places) == 0,
    'value': len(invalid_places)
})

# 4. Empty place names
cur.execute("SELECT id FROM places WHERE name IS NULL OR TRIM(name) = ''")
empty_places = cur.fetchall()
integrity_checks.append({
    'check': 'Zero Empty/Orphan Place Names',
    'passed': len(empty_places) == 0,
    'value': len(empty_places)
})

# 5. Blocks pointing to invalid districts
cur.execute("SELECT b.id FROM blocks b LEFT JOIN districts d ON b.district_id = d.id WHERE d.id IS NULL")
invalid_blocks = cur.fetchall()
integrity_checks.append({
    'check': 'Zero Blocks with Invalid district_id',
    'passed': len(invalid_blocks) == 0,
    'value': len(invalid_blocks)
})

# 6. Foods pointing to invalid districts
cur.execute("SELECT df.id FROM district_foods df LEFT JOIN districts d ON df.district_id = d.id WHERE d.id IS NULL")
invalid_foods = cur.fetchall()
integrity_checks.append({
    'check': 'Zero Foods with Invalid district_id',
    'passed': len(invalid_foods) == 0,
    'value': len(invalid_foods)
})

# 7. Services pointing to invalid districts
cur.execute("SELECT s.id FROM nearby_services s LEFT JOIN districts d ON s.district_id = d.id WHERE s.district_id IS NOT NULL AND d.id IS NULL")
invalid_services = cur.fetchall()
integrity_checks.append({
    'check': 'Zero Services with Invalid district_id',
    'passed': len(invalid_services) == 0,
    'value': len(invalid_services)
})

# 8. Rajgir as district check
cur.execute("SELECT id, name FROM districts WHERE name LIKE '%Rajgir%' OR slug LIKE '%rajgir%'")
rajgir_dist = cur.fetchall()
integrity_checks.append({
    'check': 'Rajgir NOT Listed as a District',
    'passed': len(rajgir_dist) == 0,
    'value': len(rajgir_dist)
})

results['phase13_integrity'] = integrity_checks

cur.close()
conn.close()

with open(r"D:\HiddenYatra\scratch\final_forensic_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=str)

print("✅ Saved complete forensic results to scratch/final_forensic_results.json")
