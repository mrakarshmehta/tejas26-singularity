import sys
import math
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon1 - lon2)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

conn = get_db()
cur = conn.cursor()
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
""")
active_places = cur.fetchall()

candidates = [
    {
        'name': 'Ara House',
        'district': 'Bhojpur',
        'district_id': 16,
        'category': 'historical',
        'lat': 25.5539,
        'lng': 84.6680,
        'slug': 'ara-house-bhojpur',
        'source_primary': 'bihar.gov.in (Heritage Site: Ara House, Maharaja College Arrah)',
        'source_secondary': 'Bhojpur District Administration / Veer Kunwar Singh 1857 records',
        'tourism_value': 'Historical 1857 uprising fortified site of the famous Siege of Arrah by Babu Veer Kunwar Singh; two-storeyed heritage structure with defensive embrasures on raised plinth.'
    },
    {
        'name': 'Chandradhari Museum',
        'district': 'Darbhanga',
        'district_id': 18,
        'category': 'historical',
        'lat': 26.1550,
        'lng': 85.8980,
        'slug': 'chandradhari-museum-darbhanga',
        'source_primary': 'darbhanga.nic.in (Places of Interest: Chandradhari Museum, Mansarovar Lake)',
        'source_secondary': 'bihar.gov.in / Directorate of Museums, Dept of Art, Culture & Youth, Bihar',
        'tourism_value': 'Premier 11-gallery museum of North Bihar established in 1957; houses priceless collections of Mithila art, ancient terracotta, Mauryan to Mughal coins, ivory carvings, and manuscripts.'
    },
    {
        'name': 'Baba Garibnath Temple',
        'district': 'Muzaffarpur',
        'district_id': 7,
        'category': 'temple',
        'lat': 26.1205,
        'lng': 85.3912,
        'slug': 'baba-garibnath-temple-muzaffarpur',
        'source_primary': 'tourism.bihar.gov.in (Baba Garibnath Temple & BSTDC Corridor Project)',
        'source_secondary': 'muzaffarpur.nic.in (Places of Interest: Baba Garibnath Mandir)',
        'tourism_value': 'Revered as the "Deoghar of North Bihar"; historic 300-year-old Shiva pilgrimage center drawing millions of Kanwariyas during the holy Shravani Mela.'
    },
    {
        'name': 'Surya Mandir, Kandaha',
        'district': 'Saharsa',
        'district_id': 29,
        'category': 'historical',
        'lat': 25.8820,
        'lng': 86.4670,
        'slug': 'surya-mandir-kandaha-saharsa',
        'source_primary': 'saharsa.nic.in (Places of Interest: Surya Mandir, Kandaha)',
        'source_secondary': 'Archaeological Survey of India (ASI) / bihar.gov.in',
        'tourism_value': 'Ancient Sun Temple featuring an authentic 14th-century Oinwar dynasty Sanskrit inscription (King Narasimha Deva) and a masterfully sculpted granite idol of Sun God on a 7-horse chariot.'
    },
    {
        'name': 'Mata Puran Devi Temple',
        'district': 'Purnia',
        'district_id': 28,
        'category': 'cultural',
        'lat': 25.7725,
        'lng': 87.4580,
        'slug': 'mata-puran-devi-temple-purnia',
        'source_primary': 'purnea.nic.in (Tourist Places: Puran Devi Mandir)',
        'source_secondary': 'bihar.gov.in / BSTDC Tourist Facility Development Scheme',
        'tourism_value': 'Historic titular shrine from which the district of Purnea derives its name; ancient cultural center of faith located 5 km from main city with ongoing state tourism infrastructure.'
    },
    {
        'name': 'Baba Brahmeshwar Nath Temple, Brahmpur',
        'district': 'Buxar',
        'district_id': 17,
        'category': 'temple',
        'lat': 25.5992,
        'lng': 84.2882,
        'slug': 'baba-brahmeshwar-nath-temple-brahmpur-buxar',
        'source_primary': 'tourism.bihar.gov.in (Brahmeshwar Nath Temple, Brahmapur)',
        'source_secondary': 'buxar.nic.in (Tourist Places: Brahmeshwar Nath Mandir)',
        'tourism_value': 'Ancient west-facing swayambhu Shivalinga temple traditionally called "Mini Kashi"; famous venue for the historic annual cattle fair and major Mahashivratri/Sawan pilgrimage hub.'
    },
    {
        'name': 'Gunawa Ji (Jain Tirth)',
        'district': 'Nawada',
        'district_id': 38,
        'category': 'cultural',
        'lat': 24.8944,
        'lng': 85.5312,
        'slug': 'gunawa-ji-jain-tirth-nawada',
        'source_primary': 'tourism.bihar.gov.in (Jain Circuit: Gunawa Ji Tirth, Nawada)',
        'source_secondary': 'nawada.nic.in (Places of Interest: Gunawa/Gunnawan Jain Mandir)',
        'tourism_value': 'Sacred Jain Jal Mandir situated in the middle of a scenic water reservoir; site where Indrabhuti Gautama Swami (chief disciple of Bhagwan Mahavira) attained Kevala Jnana.'
    },
    {
        'name': 'Ambika Sthan, Aami',
        'district': 'Saran',
        'district_id': 31,
        'category': 'cultural',
        'lat': 25.6881,
        'lng': 85.0062,
        'slug': 'ambika-sthan-aami-saran',
        'source_primary': 'tourism.bihar.gov.in (Ambika Sthan, Aami, Dighwara)',
        'source_secondary': 'saran.nic.in (Tourist Places: Maa Ambika Bhawani, Aami)',
        'tourism_value': 'Ancient Shaktipeeth fort-like temple complex situated on an elevated archaeological mound on the north bank of the Ganga at Dighwara; venue of grand Navratri fairs.'
    },
    {
        'name': 'Lakri Dargah',
        'district': 'Gopalganj',
        'district_id': 19,
        'category': 'cultural',
        'lat': 26.3150,
        'lng': 84.4720,
        'slug': 'lakri-dargah-gopalganj',
        'source_primary': 'gopalganj.nic.in (Places of Interest: Lakri Dargah)',
        'source_secondary': 'bihar.gov.in / Bihar State Waqf Board / Imperial Gazetteer records',
        'tourism_value': 'Prominent 16th-century Sufi pilgrimage shrine of saint Shah Arzan, endowed by Mughal Emperor Aurangzeb; notable for intricate woodwork, historic tomb, and annual Urs fair.'
    },
    {
        'name': 'Lali Pahadi Archaeological Site',
        'district': 'Lakhisarai',
        'district_id': 26,
        'category': 'historical',
        'lat': 25.1764,
        'lng': 85.9981,
        'slug': 'lali-pahadi-archaeological-site-lakhisarai',
        'source_primary': 'lakhisarai.nic.in (Places of Interest: Lali Pahadi, Shrimaddharma Vihara)',
        'source_secondary': 'Bihar Heritage Development Society (BHDS) / Dept of Art, Culture & Youth, Bihar',
        'tourism_value': 'Groundbreaking excavated hilltop Buddhist monastery ("Shrimaddharma Vihara") featuring 27 monastic cells and identified as the first epigraphically confirmed Buddhist nunnery in India.'
    }
]

print("=" * 90)
print(f"BATCH 8 CANDIDATE OVERLAP AUDIT AGAINST ALL {len(active_places)} ACTIVE DESTINATIONS")
print("=" * 90)

for idx, c in enumerate(candidates, 1):
    nearest_p = None
    min_d = 99999.0
    for ap in active_places:
        d = haversine_km(c['lat'], c['lng'], ap['latitude'], ap['longitude'])
        if d < min_d:
            min_d = d
            nearest_p = ap
    
    # Overlap classification
    if min_d < 1.0:
        cls = "SAME SITE / SEVERE OVERLAP"
    elif min_d < 5.0:
        cls = "NEARBY BUT DISTINCT"
    else:
        cls = "DISTINCT DESTINATION"
        
    print(f"\n{idx}. {c['name']} ({c['district']}, {c['category']})")
    print(f"   Coords: {c['lat']:.4f}, {c['lng']:.4f} | Canonical Slug: {c['slug']}")
    print(f"   Nearest Existing: ID {nearest_p['id']} - {nearest_p['name']} ({nearest_p['district_name']})")
    print(f"   Haversine Distance: {min_d:.2f} km | Classification: {cls}")
    print(f"   Primary Source: {c['source_primary']}")
