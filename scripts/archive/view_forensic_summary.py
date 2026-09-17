"""
Print full summary of the forensic audit JSON.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')

with open(r"D:\HiddenYatra\scratch\final_forensic_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print("PHASE 1: STATE & BACKUP")
print("=" * 80)
p1 = data['phase1']
print(f"DB: {p1['db_name']} ({p1['db_version']}) | User: {p1['db_user']}")
print(f"Backup: {p1['backup_file']} (Exists: {p1['backup_exists']}, Size: {p1['backup_size']:,} bytes)")
print("Row Counts:")
for k, v in p1['counts'].items():
    print(f"  {k:20s}: {v}")

print("\n" + "=" * 80)
print("PHASE 2: 38 DISTRICTS MASTER TABLE")
print("=" * 80)
print(f"{'ID':2s} | {'Name':25s} | {'Slug':22s} | {'Image':25s} | {'Places':6s} | {'Blocks':6s} | {'Food':4s} | {'Svcs':4s} | {'Status'}")
print("-" * 120)
for d in data['phase2_districts']:
    img_status = "✅" if d['img_exists'] else "❌"
    print(f"{d['id']:2d} | {d['name']:25s} | {d['slug']:22s} | {d['cover_image'][:20]:20s} {img_status} | {d['place_count']:6d} | {d['block_count']:6d} | {d['food_count']:4d} | {d['service_count']:4d} | {d['status']}")

print("\n" + "=" * 80)
print("PHASE 9: SEARCH TEST RESULTS")
print("=" * 80)
for s in data['phase9_search']:
    top = f"{s['top_type']}: {s['top_title']} -> {s['top_url']}" if s['top_type'] else "No results"
    print(f"Query: {s['query']:15s} | Status: {s['status_code']} | Count: {s['result_count']:2d} | Top: {top}")

print("\n" + "=" * 80)
print("PHASE 10: 38 DISTRICT ROUTE RENDERING TEST")
print("=" * 80)
route_fails = 0
for r in data['phase10_routes']:
    status = "✅ PASS" if (r['status_code'] == 200 and r['h1_correct']) else "❌ FAIL"
    if status != "✅ PASS":
        route_fails += 1
        print(f"Route: {r['url']:30s} | Status: {r['status_code']} | H1: '{r['h1_val']}' | {status}")
print(f"All 38 Routes Result: {38 - route_fails}/38 Passed ({route_fails} failed)")

print("\n" + "=" * 80)
print("PHASE 13: DATABASE INTEGRITY ASSERTIONS")
print("=" * 80)
for ic in data['phase13_integrity']:
    print(f"  [{'✅ PASS' if ic['passed'] else '❌ FAIL'}] {ic['check']} (Value: {ic['value']})")
