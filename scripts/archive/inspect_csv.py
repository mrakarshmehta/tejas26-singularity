import csv

with open('d:/HiddenYatra/PHASE6_TOP30_FACTCHECK.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    verdicts = {}
    for r in rows:
        v = r['final_verdict']
        verdicts[v] = verdicts.get(v, 0) + 1
        print(f"{r['rank']:>2}. {r['place_name']} ({r['district']}) | Lat: {r['latitude']}, Lng: {r['longitude']} | {r['final_verdict']}")
    print("\nVerdict summary:", verdicts)
