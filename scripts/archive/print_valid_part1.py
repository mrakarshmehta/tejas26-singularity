import sys
sys.path.insert(0, 'scratch')
import reconcile_candidates as rc

valid = [r for r in rc.results if r['status'] == 'VALID_CANDIDATE']
print(f"Total VALID_CANDIDATEs: {len(valid)}")
by_dist = {}
for v in valid:
    d = v['district']
    by_dist.setdefault(d, []).append(v)

for d in sorted(by_dist.keys())[:12]:
    print(f"\n=== {d} ({len(by_dist[d])}) ===")
    for c in by_dist[d]:
        coords_str = f"{c['lat']:.4f}, {c['lng']:.4f}" if c['lat'] else "No coords"
        print(f"  - {c['name']} | Cat: {c['category']} | Coords: {coords_str} | Nearest: {c['nearest']} ({c['dist']:.1f} km)")
