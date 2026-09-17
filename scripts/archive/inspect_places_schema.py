import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cursor:
    
    print("--- PLACES TABLE SCHEMA ---")
    cursor.execute("DESCRIBE places")
    for r in cursor.fetchall():
        print(f"{r['Field']:25} {r['Type']:20} Null={r['Null']:4} Key={r['Key']:4} Default={r['Default']}")
        
    print("\n--- SAMPLE RECENT PLACES (IDs 136, 137, 138) ---")
    cursor.execute("SELECT * FROM places WHERE id IN (136, 137, 138)")
    for p in cursor.fetchall():
        print(f"\nID: {p['id']}, Name: {p['name']}, Slug: {p['slug']}, District ID: {p['district_id']}, Category: {p['category']}")
        for k, v in p.items():
            if k not in ['id', 'name', 'slug', 'district_id', 'category']:
                print(f"  {k}: {repr(v)[:80]}")
    
    pass
