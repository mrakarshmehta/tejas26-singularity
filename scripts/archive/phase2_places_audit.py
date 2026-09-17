"""
Detailed places mapping analysis:
For every place:
- id, name, slug, category, district_id
- current district row (id, name, slug)
- true expected district (based on name, location keywords, seed sources)
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("""
    SELECT p.id, p.name, p.slug AS place_slug, p.category, p.district_id, p.deleted_at,
           d.name AS cur_dist_name, d.slug AS cur_dist_slug
    FROM places p
    LEFT JOIN districts d ON p.district_id = d.id
    ORDER BY p.id
""")
places = cur.fetchall()

print(f"Total Places in DB: {len(places)}")

# Canonical district names
canonical_districts = [
    "Patna", "Gaya", "Nalanda", "Vaishali", "Muzaffarpur", "Bhagalpur",
    "Munger", "Rohtas", "Madhubani", "Darbhanga", "Sitamarhi",
    "West Champaran", "East Champaran", "Saran", "Siwan", "Gopalganj",
    "Nawada", "Aurangabad", "Jehanabad", "Arwal", "Jamui", "Lakhisarai",
    "Sheikhpura", "Begusarai", "Samastipur", "Khagaria", "Katihar",
    "Purnia", "Kishanganj", "Araria", "Supaul", "Madhepura", "Saharsa",
    "Banka", "Buxar", "Bhojpur", "Kaimur", "Sheohar"
]

def determine_expected_district(p):
    name = (p['name'] or '').lower()
    pslug = (p['place_slug'] or '').lower()
    
    # Jamui places (IDs 57-73 or jamui in name/slug)
    if 'jamui' in pslug or 'giddheswar' in name or 'patneshwar' in name or 'simultala' in name or \
       'malaypur' in name or 'gidhaur' in name or 'netula' in name or 'lachhuar' in name or \
       'nagi dam' in name or 'nakti dam' in name or 'kshatriya kund' in name or 'garhi reservoir' in name or \
       'indrape' in name or 'dharhara waterfall' in name or 'laka ring' in name or 'chateshwar' in name:
        return "Jamui"
    
    # Gaya / Bodh Gaya
    if 'bodh gaya' in name or 'mahabodhi' in name or 'vishnupad' in name or 'gaya' in name or \
       'pretshila' in name or 'mangla gauri' in name or 'dungeshwari' in name or 'barabar' in name or \
       'falgu' in name or 'metta buddharam' in name or 'brahmayoni' in name or 'gehlaur' in name or \
       'dashrath manjhi' in name or 'thai monastery' in name or 'indosan' in name or 'royal thai' in name:
        return "Gaya"
    
    # Nalanda / Rajgir
    if 'nalanda' in name or 'rajgir' in name or 'rajagriha' in name:
        return "Nalanda"
        
    # Patna
    if 'patna' in name or 'golghar' in name or 'gandhi maidan' in name:
        return "Patna"
        
    # Vaishali
    if 'vaishali' in name:
        return "Vaishali"
        
    # Muzaffarpur
    if 'litchi' in name or 'jubba sahni' in name or 'muzaffarpur' in name:
        return "Muzaffarpur"
        
    # Bhagalpur
    if 'vikramshila' in name or 'mandar hill' in name or 'bhagalpur' in name:
        # Note: Mandar Hill is on the border of Banka/Bhagalpur, seeded in Bhagalpur/Banka
        if 'mandar' in name:
            return "Banka" # or Bhagalpur
        return "Bhagalpur"
        
    # Munger
    if 'munger' in name:
        return "Munger"
        
    # Rohtas
    if 'sher shah' in name or 'sasaram' in name or 'rohtas' in name:
        return "Rohtas"
        
    # Madhubani
    if 'madhubani' in name or 'jitwarpur' in name:
        return "Madhubani"
        
    # Darbhanga
    if 'darbhanga' in name:
        return "Darbhanga"
        
    # Sitamarhi
    if 'janaki' in name or 'sitamarhi' in name:
        return "Sitamarhi"
        
    # West Champaran
    if 'valmiki' in name:
        return "West Champaran"
        
    # East Champaran
    if 'kesariya' in name:
        return "East Champaran"
        
    # Nawada
    if 'kakolat' in name or 'nawada' in name:
        return "Nawada"
        
    # Aurangabad
    if 'deo sun' in name or 'aurangabad' in name:
        return "Aurangabad"
        
    # Begusarai
    if 'kanwar lake' in name or 'begusarai' in name:
        return "Begusarai"
        
    # Banka
    if 'bhimbandh' in name or 'bhim bandh' in name:
        return "Munger" # Bhimbandh is in Munger district
        
    # Buxar
    if 'buxar' in name:
        return "Buxar"
        
    # Bhojpur
    if 'veer kunwar' in name or 'jagdishpur' in name:
        return "Bhojpur"
        
    # Kaimur
    if 'mundeshwari' in name or 'kaimur' in name:
        return "Kaimur"
        
    return "UNKNOWN"

print("\n--- ALL PLACES AUDIT ---")
for p in places:
    exp = determine_expected_district(p)
    cur_name = p['cur_dist_name'] or 'None'
    match_status = "✅ MATCH" if exp == cur_name else f"❌ MISMATCH (Current: {cur_name} vs Expected: {exp})"
    print(f"ID={p['id']:3d} | Place: {p['name']:40s} | DID={str(p['district_id']):4s} | {match_status}")

cur.close()
conn.close()
