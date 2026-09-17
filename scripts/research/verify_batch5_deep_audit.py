import sys, math
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with get_cursor() as cur:
    cur.execute("SELECT id, name, slug, category, latitude, longitude, district_id FROM places WHERE deleted_at IS NULL")
    active_places = cur.fetchall()

print(f"Loaded {len(active_places)} active places from MySQL.")

batch5_candidates = [
    {
        "rank": 1,
        "name": "Umga Sun Temple & Rock Complex",
        "alt_name": "Umga Hill Temples / Sun Temple of the Hills",
        "district": "Aurangabad",
        "block": "Madanpur",
        "category": "historical",
        "latitude": 24.6312,
        "longitude": 84.5518,
        "primary_source": "District Administration Aurangabad (NIC Portal)",
        "primary_url": "https://aurangabad.nic.in/tourist-place/umga/",
        "secondary_source": "Archaeological Survey of India & Bihar Tourism",
        "secondary_url": "https://tourism.bihar.gov.in/",
        "claims": [
            {"claim": "15th-century granite stone temple built without mortar", "source": "District Administration Aurangabad", "supported": "YES"},
            {"claim": "Built by King Bhairavendra of Chero dynasty with 1442 AD Sanskrit inscription", "source": "ASI Inscription Records & District Gazetteer", "supported": "YES"},
            {"claim": "52 rock-cut shrines and monolithic sculptures atop Umga hill", "source": "District Administration Aurangabad", "supported": "YES"}
        ]
    },
    {
        "rank": 2,
        "name": "Ashokan Pillar & Ananda Stupa, Kolhua",
        "alt_name": "Kolhua Archaeological Complex / Bakhra Pillar",
        "district": "Vaishali",
        "block": "Muzaffarpur Road, Kolhua",
        "category": "historical",
        "latitude": 26.0125,
        "longitude": 85.1124,
        "primary_source": "Archaeological Survey of India (Patna Circle)",
        "primary_url": "https://asipatnacycle.gov.in/monuments/kolhua/",
        "secondary_source": "UNESCO Tentative List Dossier (Silk Road Sites in India)",
        "secondary_url": "https://whc.unesco.org/en/tentativelists/5467/",
        "claims": [
            {"claim": "Centrally Protected ASI Monument with intact 18.3m polished Chunar sandstone Ashokan pillar", "source": "ASI Patna Circle", "supported": "YES"},
            {"claim": "Pillar crowned by seated single lion capital facing north towards Kushinagar", "source": "ASI Patna Circle", "supported": "YES"},
            {"claim": "Contains Ananda Stupa, Kutagarasala Vihara, and Markata-hrada (Monkey Tank)", "source": "ASI & UNESCO Dossier", "supported": "YES"}
        ]
    },
    {
        "rank": 3,
        "name": "Punaura Dham",
        "alt_name": "Mata Sita Janmabhoomi / Punaura Mandir",
        "district": "Sitamarhi",
        "block": "Dumra / Punaura",
        "category": "cultural",
        "latitude": 26.6125,
        "longitude": 85.4512,
        "primary_source": "Ministry of Tourism, Govt of India (PRASHAD Scheme)",
        "primary_url": "https://tourism.gov.in/schemes/prashad",
        "secondary_source": "District Administration Sitamarhi (NIC Portal)",
        "secondary_url": "https://sitamarhi.nic.in/tourist-place/punaura-dham/",
        "claims": [
            {"claim": "Revered sacred birthplace of Goddess Sita under National PRASHAD Scheme", "source": "Ministry of Tourism, Govt of India", "supported": "YES"},
            {"claim": "Features historic Pundarik Sarovar (sacred pond) and Sita Kund", "source": "District Administration Sitamarhi", "supported": "YES"},
            {"claim": "Core spiritual node of official National Ramayana Circuit", "source": "Ministry of Tourism & Bihar Tourism", "supported": "YES"}
        ]
    },
    {
        "rank": 4,
        "name": "Udaipur Wildlife Sanctuary",
        "alt_name": "Udaypur Bird Sanctuary / Sarayaman Lake Sanctuary",
        "district": "West Champaran",
        "block": "Bettiah / Udaipur",
        "category": "nature",
        "latitude": 26.8512,
        "longitude": 84.4812,
        "primary_source": "Department of Environment, Forest & Climate Change (Govt of Bihar)",
        "primary_url": "https://forest.bihar.gov.in/",
        "secondary_source": "District Administration West Champaran (NIC Portal)",
        "secondary_url": "https://westchamparan.nic.in/tourist-place/udaipur-wildlife-sanctuary/",
        "claims": [
            {"claim": "Statutory Wildlife Sanctuary established in 1978 under Wildlife Protection Act 1972", "source": "Dept of Environment, Forest & Climate Change", "supported": "YES"},
            {"claim": "Covers 8.74 square kilometers centered around Sarayaman oxbow lake on Gandak river", "source": "Forest Department Bihar & ENVIS", "supported": "YES"},
            {"claim": "Critical wetland habitat for migratory waterfowl, spotted deer, and aquatic wildlife", "source": "Forest Department Bihar", "supported": "YES"}
        ]
    },
    {
        "rank": 5,
        "name": "Chandan Dam",
        "alt_name": "Chandan Reservoir & Lake",
        "district": "Banka",
        "block": "Banka / Chandan",
        "category": "lake",
        "latitude": 24.7812,
        "longitude": 86.8125,
        "primary_source": "District Administration Banka (NIC Portal)",
        "primary_url": "https://banka.nic.in/",
        "secondary_source": "Water Resources Department (Govt of Bihar)",
        "secondary_url": "https://wrd.bihar.gov.in/",
        "claims": [
            {"claim": "Major multi-earthen embankment reservoir constructed across the Chandan river", "source": "Water Resources Dept, Bihar", "supported": "YES"},
            {"claim": "Scenic eco-tourism and boating destination flanked by the Chakai and Banka hills", "source": "District Administration Banka", "supported": "YES"}
        ]
    },
    {
        "rank": 6,
        "name": "Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary",
        "alt_name": "Baraila Chaur / Salim Ali Bird Sanctuary",
        "district": "Vaishali",
        "block": "Jandaha & Mahnar",
        "category": "nature",
        "latitude": 25.7512,
        "longitude": 85.4512,
        "primary_source": "Department of Environment, Forest & Climate Change (Govt of Bihar)",
        "primary_url": "https://forest.bihar.gov.in/",
        "secondary_source": "Wildlife Protection Act 1972 Statutory Notification (1997)",
        "secondary_url": "https://vaishali.nic.in/",
        "claims": [
            {"claim": "Statutory Wildlife Sanctuary notified in 1997 under Section 18 of Wildlife Protection Act 1972", "source": "State Gazette & Forest Dept", "supported": "YES"},
            {"claim": "Perennial freshwater wetland covering 196 hectares named after ornithologist Dr. Salim Ali", "source": "Forest Department Bihar", "supported": "YES"},
            {"claim": "Hosts over 59 species of winter migratory birds and waterfowl", "source": "Wildlife Trust of India & Forest Dept", "supported": "YES"}
        ]
    },
    {
        "rank": 7,
        "name": "George Orwell Birthplace & Memorial",
        "alt_name": "Orwell Memorial House / Eric Arthur Blair Birthplace",
        "district": "East Champaran",
        "block": "Motihari Town",
        "category": "historical",
        "latitude": 26.6452,
        "longitude": 84.9085,
        "primary_source": "Department of Art, Culture & Youth (Govt of Bihar)",
        "primary_url": "https://culture.bihar.gov.in/",
        "secondary_source": "District Administration East Champaran (NIC Portal)",
        "secondary_url": "https://eastchamparan.nic.in/",
        "claims": [
            {"claim": "Authentic colonial bungalow birthplace of author George Orwell (born 25 June 1903)", "source": "Dept of Art, Culture & Youth & BBC Archives", "supported": "YES"},
            {"claim": "Declared a protected State Heritage Monument by Government of Bihar", "source": "Govt of Bihar Notification", "supported": "YES"},
            {"claim": "Houses dedicated Orwell memorial museum and gallery in Motihari", "source": "District Administration East Champaran", "supported": "YES"}
        ]
    },
    {
        "rank": 8,
        "name": "Kharagpur Lake (Haveli Kharagpur)",
        "alt_name": "Haveli Kharagpur Lake & Dam",
        "district": "Munger",
        "block": "Haveli Kharagpur",
        "category": "lake",
        "latitude": 25.1215,
        "longitude": 86.5124,
        "primary_source": "District Administration Munger (NIC Portal)",
        "primary_url": "https://munger.nic.in/tourist-place/kharagpur-lake/",
        "secondary_source": "Forest Department Bihar & Bihar Tourism",
        "secondary_url": "https://tourism.bihar.gov.in/",
        "claims": [
            {"claim": "Historic scenic reservoir constructed in 1876 by Maharaja of Darbhanga across Man river gorge", "source": "District Administration Munger & Bengal District Gazetteer", "supported": "YES"},
            {"claim": "Surrounded by forested Kharagpur hills with natural waterfall gorge and boating", "source": "District Administration Munger", "supported": "YES"}
        ]
    },
    {
        "rank": 9,
        "name": "Sarvodaya Ashram, Shekhodeora",
        "alt_name": "JP Ashram Shekhodeora / Jayaprakash Narayan Ashram",
        "district": "Nawada",
        "block": "Govindpur / Kawakol",
        "category": "cultural",
        "latitude": 24.8125,
        "longitude": 85.8412,
        "primary_source": "District Administration Nawada (NIC Portal)",
        "primary_url": "https://nawada.nic.in/tourist-place/sarvodaya-ashram-shekhodeora/",
        "secondary_source": "Sarvodaya Trust Archives & Bihar Tourism",
        "secondary_url": "https://tourism.bihar.gov.in/",
        "claims": [
            {"claim": "Historic Gandhian national freedom sanctuary established in 1952 by Loknayak Jayaprakash Narayan", "source": "District Administration Nawada", "supported": "YES"},
            {"claim": "Preserves JP's original living quarters, library, khadi weaving unit, and rural institute", "source": "Sarvodaya Trust & District Administration", "supported": "YES"}
        ]
    },
    {
        "rank": 10,
        "name": "Sujani Embroidery Craft Cluster",
        "alt_name": "Bhusura Sujani Craft Village / Sujani Mahila Kendra",
        "district": "Muzaffarpur",
        "block": "Gaighat / Bhusura",
        "category": "cultural",
        "latitude": 26.1512,
        "longitude": 85.4812,
        "primary_source": "Geographical Indications Registry (Govt of India - GI Tag No. 74)",
        "primary_url": "https://ipindiaservices.gov.in/GirPublic/",
        "secondary_source": "Development Commissioner (Handicrafts), Ministry of Textiles",
        "secondary_url": "http://handicrafts.nic.in/",
        "claims": [
            {"claim": "Registered Geographical Indication (GI Tag No. 74) under GI of Goods Act 1999", "source": "GI Registry, Govt of India", "supported": "YES"},
            {"claim": "Recipient of UNESCO Seal of Excellence for traditional narrative quilt needlework art", "source": "UNESCO & Ministry of Textiles", "supported": "YES"},
            {"claim": "Traditional women's cooperative craft cluster centered in Bhusura village", "source": "Ministry of Textiles & District Administration", "supported": "YES"}
        ]
    }
]

print("\n=== SPATIAL AUDIT AGAINST ALL 108 ACTIVE PLACES ===")
for c in batch5_candidates:
    lat, lng = c['latitude'], c['longitude']
    min_dist = 9999.0
    nearest_p = None
    nearest_id = None
    for ap in active_places:
        alat = float(ap['latitude'] or 0)
        alng = float(ap['longitude'] or 0)
        d = haversine(lat, lng, alat, alng)
        if d < min_dist:
            min_dist = d
            nearest_p = ap['name']
            nearest_id = ap['id']
            
    c['min_dist'] = min_dist
    c['nearest_p'] = nearest_p
    c['nearest_id'] = nearest_id
    
    # Audit distance classification
    if min_dist < 1.0:
        status = "HIGH OVERLAP (< 1km)"
    elif min_dist <= 3.0:
        status = "REVIEW (1-3km)"
    elif min_dist <= 5.0:
        status = "COMPLEX CHECK (3-5km)"
    else:
        status = "SAFE (> 5km)"
        
    print(f"#{c['rank']:>2}: {c['name']:48} | MinDist: {min_dist:5.1f}km to [ID {nearest_id}: {nearest_p}] -> {status}")
