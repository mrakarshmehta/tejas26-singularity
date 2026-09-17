import sys, os, csv, pymysql, dotenv
dotenv.load_dotenv()

# Let's inspect the exact candidates in PHASE5_MASTER_CANDIDATE_QUEUE.csv and BIHAR_PRIORITY_APPROVAL_QUEUE.csv
# for the underrepresented districts:
# Siwan, Buxar, Begusarai, Arwal, Samastipur, Kishanganj, Madhepura, Saran, West Champaran, Madhubani, Bhojpur, Nawada

target_districts = [
    'Siwan', 'Buxar', 'Begusarai', 'Arwal', 'Samastipur', 
    'Kishanganj', 'Madhepura', 'Saran', 'West Champaran', 
    'Madhubani', 'Bhojpur', 'Nawada', 'Khagaria', 'Sheohar'
]

with open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in PHASE5_MASTER: {len(rows)}")
print("\n--- Filtered candidates for target districts ---")
for r in rows:
    dist = r.get('district', '').strip()
    if dist in target_districts:
        print(f"[{dist}] {r.get('place_name')} | Cat: {r.get('category')} | Prio: {r.get('recommended_priority')} | Coords: {r.get('coordinates')} | Verif: {r.get('verification_level')}")
        print(f"   Primary: {r.get('primary_source')}")
        print(f"   Secondary: {r.get('secondary_source')}")
        print(f"   Why: {r.get('tourism_value')[:100]}...")
        print()
