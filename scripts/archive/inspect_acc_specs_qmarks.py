import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor() as cur:
    cur.execute("SELECT id, name, price_range, description FROM accommodations WHERE price_range LIKE '%?%' OR description LIKE '%?%'")
    accs = cur.fetchall()
    print(f"Accommodations with '???': {len(accs)}")
    for a in accs[:10]:
        print(f"  Acc #{a['id']} {a['name']}: price={repr(a['price_range'])}, desc={repr(a['description'][:60])}")

with get_cursor() as cur:
    cur.execute("SELECT id, name, price_range, description FROM specialties WHERE price_range LIKE '%?%' OR description LIKE '%?%'")
    specs = cur.fetchall()
    print(f"Specialties with '???': {len(specs)}")
    for s in specs[:10]:
        print(f"  Spec #{s['id']} {s['name']}: price={repr(s['price_range'])}, desc={repr(s['description'][:60])}")
