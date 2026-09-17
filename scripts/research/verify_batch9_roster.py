import sys
import os
import math
import pymysql
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

conn = pymysql.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    port=int(os.getenv('DB_PORT', 3307)),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'hiddenyatra'),
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()

# 1. Fetch active places
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name
    FROM places p
    JOIN districts d ON p.district_id = d.id
    WHERE p.deleted_at IS NULL
    ORDER BY p.id ASC
""")
active_places = cur.fetchall()
print(f"Total active places: {len(active_places)}")

# 2. Fetch districts
cur.execute("SELECT id, name FROM districts")
districts_db = {d['name'].lower(): d['id'] for d in cur.fetchall()}

# Batch 9 Candidate Definitions
candidates = [
    {
        "rank": 1,
        "name": "Lali Pahadi Archaeological Site",
        "district": "Lakhisarai",
        "category": "historical",
        "lat": 25.1764,
        "lng": 85.9981,
        "slug": "lali-pahadi-archaeological-site",
        "tourism_value": "First excavated hilltop Buddhist nunnery ('Shrimaddharma Vihara') in the Gangetic plains, excavated by BHDS & Visva-Bharati, featuring 27 cells, central shrine, and ancient monk quarters.",
        "why_new_value": "Strengthens 2-place Lakhisarai with world-class Buddhist monastic archaeology, complementing Ashok Dham and Shringirishi Dham.",
        "primary_source": "Bihar Heritage Development Society (BHDS) / Directorate of Archaeology, Art, Culture & Youth Dept, Govt of Bihar",
        "secondary_source": "Lakhisarai District Administration (lakhisarai.nic.in) / Visva-Bharati University Excavation Reports",
        "confidence": "A",
        "priority": "P0",
        "notes": "Officially excavated and inaugurated by CM Nitish Kumar; clear geographic coordinates on Lali Pahadi hillock."
    },
    {
        "rank": 2,
        "name": "Khudneshwar Asthan, Morwa",
        "district": "Samastipur",
        "category": "cultural",
        "lat": 25.7610,
        "lng": 85.6890,
        "slug": "khudneshwar-asthan-morwa",
        "tourism_value": "Historic 1858 syncretic shrine where a sacred Shivalinga and the mazar of a Muslim devotee (Khudni Biwi) share the same inner sanctum, exemplifying communal harmony.",
        "why_new_value": "Expands 2-place Samastipur with a profound living cultural heritage site demonstrating Bihar's syncretic traditions.",
        "primary_source": "Samastipur District Administration (samastipur.nic.in) - Tourism / Places of Interest",
        "secondary_source": "Bihar Tourism (tourism.bihar.gov.in) - Cultural & Religious Circuit",
        "confidence": "A",
        "priority": "P0",
        "notes": "Unique Hindu-Muslim shared sanctum sanctorum; attracts large festive crowds during Shivratri and Shravani Mela."
    },
    {
        "rank": 3,
        "name": "Panth Pakar",
        "district": "Sitamarhi",
        "category": "cultural",
        "lat": 26.6370,
        "lng": 85.4520,
        "slug": "panth-pakar",
        "tourism_value": "Ancient sprawling sacred Banyan tree (spread across ~1 acre) in Riga block where, according to the Ramayana tradition, the bridal palanquin of Devi Sita and Lord Rama rested on their journey to Ayodhya.",
        "why_new_value": "Strengthens 2-place Sitamarhi on the Ramayana Circuit with a unique botanical-sacred living heritage landmark distinct from town temples.",
        "primary_source": "Bihar Tourism (tourism.bihar.gov.in) - Ramayana Circuit",
        "secondary_source": "Sitamarhi District Administration (sitamarhi.nic.in) - Tourism & Heritage",
        "confidence": "A",
        "priority": "P0",
        "notes": "Located 2.72 km from Punaura Dham. Completely independent pilgrimage site (living centuries-old banyan tree vs Janaki temple)."
    },
    {
        "rank": 4,
        "name": "Manihari Ganga Ghat & Maharshi Mehi Ashram",
        "district": "Katihar",
        "category": "cultural",
        "lat": 25.3370,
        "lng": 87.6250,
        "slug": "manihari-ganga-ghat-maharshi-mehi-ashram",
        "tourism_value": "Historic Ganga riverfront and sacred bathing ghat at Manihari, paired with the pioneering spiritual ashram of Santmat reformer Maharshi Mehi Paramhans.",
        "why_new_value": "Strengthens 2-place Katihar with an authentic riverfront pilgrimage and spiritual retreat destination, complementing Gogabil Lake Bird Sanctuary.",
        "primary_source": "Katihar District Administration (katihar.nic.in) - Tourism & Places of Interest",
        "secondary_source": "Bihar Tourism (tourism.bihar.gov.in) / Santmat Spiritual Publications",
        "confidence": "A",
        "priority": "P0",
        "notes": "Located 2.67 km from Gogabil Lake. Completely distinct visitor intent (sacred riverfront/ashram vs oxbow wetland sanctuary)."
    },
    {
        "rank": 5,
        "name": "Rishi Kund",
        "district": "Munger",
        "category": "nature",
        "lat": 25.2630,
        "lng": 86.5180,
        "slug": "rishi-kund",
        "tourism_value": "Natural perennial thermal hot springs set in a scenic forested valley of the Kharagpur Hills, renowned for therapeutic mineral waters and the triennial Malmas Mela.",
        "why_new_value": "Enriches Munger's eco-tourism and nature inventory with a legendary natural hot spring resort distinct from Bhimbandh and Munger Fort.",
        "primary_source": "Munger District Administration (munger.nic.in) - Places of Interest & Tourism",
        "secondary_source": "Bihar State Tourism Development Corporation (BSTDC) / Geological Survey of India Thermal Springs Records",
        "confidence": "A",
        "priority": "P0",
        "notes": "Distinct forested geothermal spring complex situated ~12.2 km north of Kharagpur Lake."
    },
    {
        "rank": 6,
        "name": "Chandradhari Museum",
        "district": "Darbhanga",
        "category": "cultural",
        "lat": 26.1550,
        "lng": 85.8980,
        "slug": "chandradhari-museum",
        "tourism_value": "Premier public cultural repository of North Bihar established in 1957, housing over 13,000 rare antiquities across 11 thematic galleries including Mithila paintings, ancient terracottas, and Royal Darbhanga relics.",
        "why_new_value": "Adds a high-caliber cultural institution and museum to Mithilanchal, creating a balanced urban heritage circuit alongside Laxmi Vilas Palace and Shyama Mai Temple.",
        "primary_source": "Directorate of Museums, Department of Art, Culture & Youth, Govt of Bihar (museums.bihar.gov.in)",
        "secondary_source": "Darbhanga District Administration (darbhanga.nic.in) - Tourism & Culture",
        "confidence": "A",
        "priority": "P0",
        "notes": "Located 0.87 km from Laxmi Vilas Palace. Independent institutional museum destination on the bank of Mansarovar Lake."
    },
    {
        "rank": 7,
        "name": "Sohagara Dham",
        "district": "Siwan",
        "category": "temple",
        "lat": 26.0820,
        "lng": 84.0850,
        "slug": "sohagara-dham",
        "tourism_value": "Ancient Swayambhu Baba Hansnath Mandir situated on the Jharahi river at the Bihar-UP border, housing an enormous subterranean black-stone Shivalinga with deep historical reverence.",
        "why_new_value": "Expands 2-place Siwan with an iconic regional pilgrimage landmark that attracts hundreds of thousands of pilgrims during Maha Shivratri and Shravani Mela.",
        "primary_source": "Siwan District Administration (siwan.nic.in) - Tourism & Places of Interest",
        "secondary_source": "Bihar Tourism (tourism.bihar.gov.in) - Spiritual Circuit",
        "confidence": "A",
        "priority": "P0",
        "notes": "Border pilgrimage landmark ~26.4 km from Baba Mahendra Nath Temple; serves as major cross-state cultural bridge."
    },
    {
        "rank": 8,
        "name": "Manjhi Fort Ruins & Ancient Mound",
        "district": "Saran",
        "category": "historical",
        "lat": 25.8230,
        "lng": 84.5820,
        "slug": "manjhi-fort-ruins-ancient-mound",
        "tourism_value": "Centrally Protected Monument under Archaeological Survey of India (ASI Patna Circle); massive ancient riverfront citadel mound and ramparts overlooking the Ghaghra (Saryu) and Ganga confluence.",
        "why_new_value": "Adds genuine ASI-protected archaeological depth to Saran, representing Chero dynasty fortification and NBPW-to-medieval continuous occupation.",
        "primary_source": "Archaeological Survey of India (ASI Patna Circle) - List of Centrally Protected Monuments",
        "secondary_source": "Saran District Administration (saran.nic.in) - History & Monuments",
        "confidence": "A",
        "priority": "P0",
        "notes": "ASI Protected site ~14.5 km upstream from Revelganj / Gautam Asthan."
    },
    {
        "rank": 9,
        "name": "Tomb of Bakhtiyar Khan, Chainpur",
        "district": "Kaimur",
        "category": "historical",
        "lat": 25.0430,
        "lng": 83.5180,
        "slug": "tomb-of-bakhtiyar-khan-chainpur",
        "tourism_value": "State Protected Monument representing monumental 16th-century Suri-Afghan funerary architecture; majestic octagonal sandstone mausoleum on a high raised plinth with battlemented enclosures.",
        "why_new_value": "Adds exquisite medieval Afghan architecture to Kaimur, diversifying its portfolio beyond waterfalls and ancient temples.",
        "primary_source": "Directorate of Archaeology, Department of Art, Culture & Youth, Govt of Bihar - State Protected Monuments List",
        "secondary_source": "Kaimur District Administration (kaimur.nic.in) - Tourism & Monuments",
        "confidence": "A",
        "priority": "P0",
        "notes": "Located 4.28 km from Karkatgarh Waterfall. Completely distinct heritage destination (16th-century Afghan mausoleum vs natural waterfall/eco-park)."
    },
    {
        "rank": 10,
        "name": "Khuda Bakhsh Oriental Public Library",
        "district": "Patna",
        "category": "cultural",
        "lat": 25.6185,
        "lng": 85.1630,
        "slug": "khuda-bakhsh-oriental-public-library",
        "tourism_value": "Institution of National Importance (Act of Parliament, 1969) housing over 21,000 priceless Arabic, Persian, and Urdu manuscripts, including the unique illustrated Tarikh-e-Khandan-e-Timuriya and Padshahnama.",
        "why_new_value": "Introduces intellectual and bibliographic heritage of global stature, offering cultural travellers an unparalleled encounter with Mughal imperial history and arts.",
        "primary_source": "Ministry of Culture, Government of India / Khuda Bakhsh Oriental Public Library Act (No. 43 of 1969)",
        "secondary_source": "Patna District Administration (patna.nic.in) - Tourism & Heritage / Bihar Tourism",
        "confidence": "A",
        "priority": "P0",
        "notes": "Located 2.29 km from Golghar. Autonomous statutory national institution with independent visitor profile."
    }
]

print("\n" + "=" * 100)
print("BATCH 9 CANDIDATE AUDIT & NEAREST EXISTING PLACE CALCULATIONS")
print("=" * 100)

for c in candidates:
    d_name = c['district']
    d_id = districts_db.get(d_name.lower())
    c['district_id'] = d_id
    
    # Calculate nearest active place
    min_dist = float('inf')
    nearest_p = None
    for p in active_places:
        plat, plon = float(p['latitude']), float(p['longitude'])
        dist = haversine(c['lat'], c['lng'], plat, plon)
        if dist < min_dist:
            min_dist = dist
            nearest_p = p
            
    c['nearest_place'] = nearest_p['name']
    c['nearest_place_id'] = nearest_p['id']
    c['min_distance'] = min_dist
    c['overlap_classification'] = "NEARBY BUT DISTINCT" if min_dist < 5.0 else "DISTINCT DESTINATION"
    
    print(f"Rank {c['rank']}: {c['name']}")
    print(f"  District: {c['district']} (ID: {c['district_id']}) | Category: {c['category']}")
    print(f"  Coords: ({c['lat']:.4f}, {c['lng']:.4f}) | Slug: {c['slug']}")
    print(f"  Nearest Place: {nearest_p['name']} (ID: {nearest_p['id']}) @ {min_dist:.2f} km")
    print(f"  Overlap Class: {c['overlap_classification']}")
    print(f"  Sources: [Primary: {c['primary_source']}] [Confidence: {c['confidence']}]")
    print("-" * 100)

# Check slug uniqueness against active places
existing_slugs = {p['slug'].lower() for p in active_places}
existing_names = {p['name'].lower() for p in active_places}

print("\nChecking collision against 148 active places:")
collisions = 0
for c in candidates:
    if c['slug'].lower() in existing_slugs:
        print(f"  COLLISION: Slug '{c['slug']}' already exists!")
        collisions += 1
    if c['name'].lower() in existing_names:
        print(f"  COLLISION: Name '{c['name']}' already exists!")
        collisions += 1
if collisions == 0:
    print("  ALL 10 CANDIDATE SLUGS AND NAMES ARE 100% UNIQUE! NO COLLISIONS.")
