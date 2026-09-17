import sys
import os
sys.path.insert(0, '.')
import scripts.research.reconcile_candidates as rc

sys.stdout.reconfigure(encoding='utf-8')

print("\n" + "="*80)
print(f"TOTAL RECONCILED CANDIDATES: {len(rc.results)}")
print("="*80)

# Group by status
by_status = {}
for r in rc.results:
    by_status.setdefault(r['status'], []).append(r)

for status, cands in by_status.items():
    print(f"\n--- {status} ({len(cands)}) ---")
    for c in sorted(cands, key=lambda x: (x['district'], x['name'])):
        dist_str = f"{c['dist']:.2f} km" if c['lat'] else "N/A"
        coords = f"({c['lat']:.4f}, {c['lng']:.4f})" if c['lat'] else "No coords"
        print(f"[{c['district']}] {c['name']} | Cat: {c['category']} | Coords: {coords} | Nearest: {c['nearest']} ({dist_str}) | Reason: {c['reason']}")
