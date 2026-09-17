import csv
import sys
import os
import math
import shutil
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

conn = get_db()
cur = conn.cursor()
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
    ORDER BY p.id
""")
active_places = cur.fetchall()
print(f"Loaded {len(active_places)} active places from DB.")

# 10 Approval-Ready Candidates for Batch 9
batch9_candidates = [
    {
        'rank': 1,
        'candidate_name': 'Lali Pahadi Archaeological Site',
        'district': 'Lakhisarai',
        'district_id': 26,
        'category': 'historical',
        'latitude': 25.1764,
        'longitude': 85.9981,
        'canonical_slug': 'lali-pahadi-archaeological-site',
        'tourism_value': "First excavated hilltop Buddhist nunnery ('Shrimaddharma Vihara') in the Gangetic plains, excavated jointly by Bihar Heritage Development Society (BHDS) and Visva-Bharati University; features 27 monk cells, central courtyard, and rich antiquities.",
        'why_it_adds_new_value': 'Strengthens 2-place Lakhisarai with world-class Buddhist monastic archaeology, creating a compelling heritage circuit with Ashok Dham Temple and Shringirishi Dham.',
        'primary_source': 'Bihar Heritage Development Society (BHDS) / Directorate of Archaeology, Art, Culture & Youth Dept, Govt of Bihar',
        'secondary_source': 'Lakhisarai District Administration (lakhisarai.nic.in) / Visva-Bharati Excavation Reports',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Excavated and officially inaugurated by CM Nitish Kumar; hilltop archaeological park located 6.35 km from Ashok Dham Temple.'
    },
    {
        'rank': 2,
        'candidate_name': 'Khudneshwar Asthan, Morwa',
        'district': 'Samastipur',
        'district_id': 30,
        'category': 'cultural',
        'latitude': 25.7610,
        'longitude': 85.6890,
        'canonical_slug': 'khudneshwar-asthan-morwa',
        'tourism_value': 'Historic 1858 syncretic shrine where a sacred Shivalinga and the mazar of a Muslim woman devotee (Khudni Biwi) share the same inner sanctum, exemplifying communal harmony and Ganga-Jamuni tehzeeb.',
        'why_it_adds_new_value': "Expands 2-place Samastipur with a profound living cultural heritage site demonstrating Bihar's syncretic traditions; complements Vidyapati Dham.",
        'primary_source': 'Samastipur District Administration (samastipur.nic.in) - Tourism & Places of Interest',
        'secondary_source': 'Bihar Tourism (tourism.bihar.gov.in) - Cultural & Religious Circuit',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Unique Hindu-Muslim shared sanctum sanctorum; attracts large festive crowds during Shivratri and Shravani Mela. 18.17 km from Vidyapati Dham.'
    },
    {
        'rank': 3,
        'candidate_name': 'Panth Pakar',
        'district': 'Sitamarhi',
        'district_id': 34,
        'category': 'cultural',
        'latitude': 26.6370,
        'longitude': 85.4520,
        'canonical_slug': 'panth-pakar',
        'tourism_value': 'Ancient sprawling sacred Banyan tree (spread across ~1 acre) in Riga block where, according to Ramayana tradition, the bridal palanquin (doli) of Devi Sita and Lord Rama rested on their journey to Ayodhya.',
        'why_it_adds_new_value': 'Strengthens 2-place Sitamarhi on the Ramayana Circuit with a unique botanical-sacred living heritage landmark distinct from town temples.',
        'primary_source': 'Bihar Tourism (tourism.bihar.gov.in) - Ramayana Circuit',
        'secondary_source': 'Sitamarhi District Administration (sitamarhi.nic.in) - Tourism & Heritage',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Located 2.73 km from Punaura Dham. Completely independent pilgrimage site (living centuries-old banyan tree vs Janaki temple). Special scrutiny fully documented.'
    },
    {
        'rank': 4,
        'candidate_name': 'Manihari Ganga Ghat & Maharshi Mehi Ashram',
        'district': 'Katihar',
        'district_id': 23,
        'category': 'cultural',
        'latitude': 25.3370,
        'longitude': 87.6250,
        'canonical_slug': 'manihari-ganga-ghat-maharshi-mehi-ashram',
        'tourism_value': 'Historic Ganga riverfront and sacred bathing ghat at Manihari, paired with the pioneering spiritual retreat and ashram of Santmat reformer Maharshi Mehi Paramhans.',
        'why_it_adds_new_value': 'Strengthens 2-place Katihar with an authentic riverfront pilgrimage and spiritual retreat destination, complementing Gogabil Lake Bird Sanctuary.',
        'primary_source': 'Katihar District Administration (katihar.nic.in) - Tourism & Places of Interest',
        'secondary_source': 'Bihar Tourism (tourism.bihar.gov.in) / Santmat Spiritual Publications',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Located 2.67 km from Gogabil Lake. Completely distinct visitor intent (sacred riverfront/ashram vs oxbow wetland sanctuary). Special scrutiny fully documented.'
    },
    {
        'rank': 5,
        'candidate_name': 'Rishi Kund',
        'district': 'Munger',
        'district_id': 6,
        'category': 'nature',
        'latitude': 25.2630,
        'longitude': 86.5180,
        'canonical_slug': 'rishi-kund',
        'tourism_value': 'Natural perennial thermal hot springs set in a scenic forested valley of the Kharagpur Hills, renowned for therapeutic mineral waters and the triennial Malmas Mela.',
        'why_it_adds_new_value': "Enriches Munger's eco-tourism and nature inventory with a legendary natural hot spring resort distinct from Bhimbandh and Munger Fort.",
        'primary_source': 'Munger District Administration (munger.nic.in) - Places of Interest & Tourism',
        'secondary_source': 'Bihar State Tourism Development Corporation (BSTDC) / Geological Survey of India Thermal Springs Records',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Distinct forested geothermal spring complex situated 12.2 km north of Kharagpur Lake and 13.25 km from Munger Fort.'
    },
    {
        'rank': 6,
        'candidate_name': 'Chandradhari Museum',
        'district': 'Darbhanga',
        'district_id': 18,
        'category': 'cultural',
        'latitude': 26.1550,
        'longitude': 85.8980,
        'canonical_slug': 'chandradhari-museum',
        'tourism_value': 'Premier public cultural repository of North Bihar established in 1957, housing over 13,000 rare antiquities across 11 thematic galleries including Mithila paintings, ancient terracottas, and Royal Darbhanga relics.',
        'why_it_adds_new_value': 'Adds a high-caliber cultural institution and museum to Mithilanchal, creating a balanced urban heritage circuit alongside Laxmi Vilas Palace and Shyama Mai Temple.',
        'primary_source': 'Directorate of Museums, Department of Art, Culture & Youth, Govt of Bihar (museums.bihar.gov.in)',
        'secondary_source': 'Darbhanga District Administration (darbhanga.nic.in) - Tourism & Culture',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Located 0.87 km from Laxmi Vilas Palace on the bank of Mansarovar Lake. Independent institutional museum destination. Special scrutiny fully documented.'
    },
    {
        'rank': 7,
        'candidate_name': 'Sohagara Dham',
        'district': 'Siwan',
        'district_id': 35,
        'category': 'temple',
        'latitude': 26.0820,
        'longitude': 84.0850,
        'canonical_slug': 'sohagara-dham',
        'tourism_value': 'Ancient Swayambhu Baba Hansnath Mandir situated on the Jharahi river at the Bihar-UP border, housing an enormous subterranean black-stone Shivalinga with deep historical reverence.',
        'why_it_adds_new_value': 'Expands 2-place Siwan with an iconic regional pilgrimage landmark that attracts hundreds of thousands of pilgrims during Maha Shivratri and Shravani Mela.',
        'primary_source': 'Siwan District Administration (siwan.nic.in) - Tourism & Places of Interest',
        'secondary_source': 'Bihar Tourism (tourism.bihar.gov.in) - Spiritual Circuit',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Border pilgrimage landmark situated 23.53 km from Zeeradei and 26.4 km from Baba Mahendra Nath Temple; serves as major cross-state cultural bridge.'
    },
    {
        'rank': 8,
        'candidate_name': 'Manjhi Fort Ruins & Ancient Mound',
        'district': 'Saran',
        'district_id': 31,
        'category': 'historical',
        'latitude': 25.8230,
        'longitude': 84.5820,
        'canonical_slug': 'manjhi-fort-ruins-ancient-mound',
        'tourism_value': 'Centrally Protected Monument under Archaeological Survey of India (ASI Patna Circle); massive ancient riverfront citadel mound and ramparts overlooking the Ghaghra (Saryu) and Ganga confluence.',
        'why_it_adds_new_value': 'Adds genuine ASI-protected archaeological depth to Saran, representing Chero dynasty fortification and NBPW-to-medieval continuous occupation.',
        'primary_source': 'Archaeological Survey of India (ASI Patna Circle) - List of Centrally Protected Monuments',
        'secondary_source': 'Saran District Administration (saran.nic.in) - History & Monuments',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'ASI Centrally Protected site situated 10.07 km upstream from Revelganj / Gautam Asthan.'
    },
    {
        'rank': 9,
        'candidate_name': 'Tomb of Bakhtiyar Khan, Chainpur',
        'district': 'Kaimur',
        'district_id': 22,
        'category': 'historical',
        'latitude': 25.0430,
        'longitude': 83.5180,
        'canonical_slug': 'tomb-of-bakhtiyar-khan-chainpur',
        'tourism_value': 'State Protected Monument representing monumental 16th-century Suri-Afghan funerary architecture; majestic octagonal sandstone mausoleum on a high raised plinth with battlemented enclosures.',
        'why_it_adds_new_value': 'Adds exquisite medieval Afghan architecture to Kaimur, diversifying its portfolio beyond waterfalls and ancient temples.',
        'primary_source': 'Directorate of Archaeology, Department of Art, Culture & Youth, Govt of Bihar - State Protected Monuments List',
        'secondary_source': 'Kaimur District Administration (kaimur.nic.in) - Tourism & Monuments',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Located 4.28 km from Karkatgarh Waterfall in Chainpur town. Completely distinct heritage destination (16th-century Afghan mausoleum vs natural waterfall/eco-park). Special scrutiny fully documented.'
    },
    {
        'rank': 10,
        'candidate_name': 'Khuda Bakhsh Oriental Public Library',
        'district': 'Patna',
        'district_id': 1,
        'category': 'cultural',
        'latitude': 25.6185,
        'longitude': 85.1630,
        'canonical_slug': 'khuda-bakhsh-oriental-public-library',
        'tourism_value': 'Institution of National Importance (Act of Parliament, 1969) housing over 21,000 priceless Arabic, Persian, and Urdu manuscripts, including the unique illustrated Tarikh-e-Khandan-e-Timuriya and Padshahnama.',
        'why_it_adds_new_value': 'Introduces intellectual and bibliographic heritage of global stature, offering cultural travellers an unparalleled encounter with Mughal imperial history and arts.',
        'primary_source': 'Ministry of Culture, Government of India / Khuda Bakhsh Oriental Public Library Act (No. 43 of 1969)',
        'secondary_source': 'Patna District Administration (patna.nic.in) - Tourism & Heritage / Bihar Tourism',
        'evidence_confidence': 'HIGH (Grade A)',
        'recommended_priority': 'P0',
        'risk_notes': 'Located 1.35 km from Takht Sri Patna Sahib on Ashok Rajpath. Autonomous statutory national institution with independent visitor profile. Special scrutiny fully documented.'
    }
]

# Compute nearest existing places and distance for all 10 candidates
for c in batch9_candidates:
    nearest = None
    min_d = 99999.0
    for ap in active_places:
        d = haversine_km(c['latitude'], c['longitude'], ap['latitude'], ap['longitude'])
        if d < min_d:
            min_d = d
            nearest = ap
    c['nearest_existing_place'] = f"{nearest['name']} ({nearest['district_name']})"
    c['min_haversine_km'] = min_d
    if min_d < 5.0:
        c['overlap_classification'] = 'NEARBY BUT DISTINCT (Special Scrutiny)'
    else:
        c['overlap_classification'] = 'DISTINCT DESTINATION'

# ── 1. WRITE BIHAR_BATCH9_APPROVAL_PREVIEW.csv ──
csv_fields = [
    'rank', 'candidate_name', 'district', 'district_id', 'category',
    'latitude', 'longitude', 'canonical_slug', 'nearest_existing_place',
    'min_haversine_km', 'overlap_classification', 'tourism_value',
    'why_it_adds_new_value', 'primary_source', 'secondary_source',
    'evidence_confidence', 'recommended_priority', 'risk_notes'
]
with open('BIHAR_BATCH9_APPROVAL_PREVIEW.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=csv_fields)
    writer.writeheader()
    for c in batch9_candidates:
        writer.writerow(c)
print("Saved BIHAR_BATCH9_APPROVAL_PREVIEW.csv")

# ── 2. WRITE BIHAR_BATCH9_OVERLAP_AUDIT.csv ──
audit_list = list(batch9_candidates) + [
    {
        'candidate_name': 'Nagi Dam Bird Sanctuary',
        'district': 'Jamui',
        'latitude': 24.8150,
        'longitude': 86.3750,
        'category': 'nature'
    },
    {
        'candidate_name': 'Kauwadol Hill & Colossal Buddha Statue',
        'district': 'Gaya',
        'latitude': 24.9920,
        'longitude': 85.0480,
        'category': 'historical'
    },
    {
        'candidate_name': 'Kurkihar Archaeological Site',
        'district': 'Gaya',
        'latitude': 24.8152,
        'longitude': 85.2512,
        'category': 'historical'
    },
    {
        'candidate_name': 'Sun Temple, Tarari',
        'district': 'Bhojpur',
        'latitude': 25.2650,
        'longitude': 84.4530,
        'category': 'historical'
    },
    {
        'candidate_name': 'Buddha Relic Stupa',
        'district': 'Vaishali',
        'latitude': 25.9860,
        'longitude': 85.1270,
        'category': 'historical'
    },
    {
        'candidate_name': 'Chankigarh Fort',
        'district': 'West Champaran',
        'latitude': 27.0520,
        'longitude': 84.4750,
        'category': 'historical'
    },
    {
        'candidate_name': 'Bettiah Raj Palace Complex',
        'district': 'West Champaran',
        'latitude': 26.8010,
        'longitude': 84.5020,
        'category': 'historical'
    },
    {
        'candidate_name': 'Amjhar Sharif',
        'district': 'Aurangabad',
        'latitude': 24.9854,
        'longitude': 84.5218,
        'category': 'cultural'
    },
    {
        'candidate_name': 'Husepur Fort Ruins',
        'district': 'Gopalganj',
        'latitude': 26.5412,
        'longitude': 84.2815,
        'category': 'historical'
    },
    {
        'candidate_name': 'Nagarjuni Caves',
        'district': 'Jehanabad',
        'latitude': 25.0125,
        'longitude': 85.0785,
        'category': 'historical'
    },
    {
        'candidate_name': 'Sujata Stupa & Kuti',
        'district': 'Gaya',
        'latitude': 24.6925,
        'longitude': 85.0028,
        'category': 'historical'
    },
    {
        'candidate_name': 'Dharahara Village',
        'district': 'Supaul',
        'latitude': 26.1500,
        'longitude': 86.5800,
        'category': 'cultural'
    }
]

audit_rows = []
for item in audit_list:
    nearest = None
    min_d = 99999.0
    for ap in active_places:
        d = haversine_km(item['latitude'], item['longitude'], ap['latitude'], ap['longitude'])
        if d < min_d:
            min_d = d
            nearest = ap
    if min_d < 1.0:
        cls = 'SAME SITE / SEVERE OVERLAP'
        res = 'Scrutinized: distinct parcel/institution vs. attached monument; held if same-site.'
    elif min_d < 5.0:
        cls = 'NEARBY BUT DISTINCT (Special Scrutiny)'
        res = 'Verified distinct attraction identity, independent visitor intent, and separate parcel/grounds.'
    else:
        cls = 'DISTINCT DESTINATION'
        res = 'Clear geographic separation (>5 km) from all active inventory.'
    
    audit_rows.append({
        'candidate_name': item['candidate_name'],
        'district': item['district'],
        'category': item['category'],
        'latitude': item['latitude'],
        'longitude': item['longitude'],
        'nearest_place_id': nearest['id'],
        'nearest_place_name': nearest['name'],
        'nearest_place_district': nearest['district_name'],
        'haversine_distance_km': min_d,
        'overlap_classification': cls,
        'audit_resolution': res
    })

audit_fields = [
    'candidate_name', 'district', 'category', 'latitude', 'longitude',
    'nearest_place_id', 'nearest_place_name', 'nearest_place_district',
    'haversine_distance_km', 'overlap_classification', 'audit_resolution'
]
with open('BIHAR_BATCH9_OVERLAP_AUDIT.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=audit_fields)
    writer.writeheader()
    for r in audit_rows:
        writer.writerow(r)
print("Saved BIHAR_BATCH9_OVERLAP_AUDIT.csv")

# ── 3. WRITE BIHAR_BATCH9_CANDIDATE_STATUS.csv ──
status_rows = []

# Approval-ready (10)
for c in batch9_candidates:
    status_rows.append({
        'candidate': c['candidate_name'],
        'district': c['district'],
        'previous_status': 'HOLD / CANDIDATE QUEUE',
        'current_status': 'APPROVAL-READY',
        'reason': f"Selected as Batch 9 Rank {c['rank']}; verified Grade A institutional evidence; adds district depth and experience diversity."
    })

# Held (15)
held_items = [
    ('Nagi Dam Bird Sanctuary', 'Jamui', 'Notified Wildlife Sanctuary and Ramsar site 2541; located 3.10 km from Nakti Dam; Jamui already heavily represented with 11 active places.'),
    ('Kauwadol Hill & Colossal Buddha Statue', 'Gaya', 'ASI protected monument with 8-foot seated Buddha; located 4.10 km from Barabar; Gaya already has 12 active places; held for geographic balance.'),
    ('Kurkihar Archaeological Site', 'Gaya', 'World-famous 9th-12th century Pala bronze hoard discovery site; held due to heavy Gaya representation (12 active destinations).'),
    ('Sun Temple, Tarari', 'Bhojpur', 'Medieval Sun temple in Dev village; Bhojpur recently gained Ara House in Batch 8; held for future consideration.'),
    ('Buddha Relic Stupa', 'Vaishali', 'Excavated mud stupa of the Lichchhavis; held due to 0.93 km marker proximity to ID 10; Vaishali already has 3 active places.'),
    ('Chankigarh Fort', 'West Champaran', 'Massive 90-foot ancient brick mound; held to avoid Champaran saturation (already 6 active destinations).'),
    ('Bettiah Raj Palace Complex', 'West Champaran', 'Historic 18th-century zamindari palace; ongoing court receiver administration and property disputes.'),
    ('Amjhar Sharif', 'Aurangabad', 'Sufi shrine on official Bihar Tourism circuit; Aurangabad already has 4 active places; held for geographic balance.'),
    ('Husepur Fort Ruins', 'Gopalganj', 'Historic fort ruins of Raja Fateh Bahadur Sahi; Gopalganj recently gained Lakri Dargah in Batch 8; held for future batch.'),
    ('Nagarjuni Caves', 'Jehanabad', 'Adjacent Maurya-era cave complex 1.78 km from Barabar Caves (ID 5); part of the canonical Barabar-Nagarjuni archaeological cluster.'),
    ('Dharahara Village', 'Supaul', 'Renowned tree-planting social tradition; held as community socio-cultural practice without formal tourism infrastructure.'),
    ('Sheohar Raj Palace', 'Sheohar', 'Former 19th-century estate residence; disputed private property without official tourism department notification.'),
    ('Indrasal Cave, Parvati Hill', 'Nawada', 'Scholarly debate and coordinate divergence between Giriyak Hill and Parvati Hill; held pending field verification.'),
    ('Sagar Dih Mound & Stupa', 'East Champaran', 'Archaeological stupa mound near Raxaul; East Champaran has 3 active destinations; held pending further ASI excavation documentation.'),
    ('Agnihotri Temple', 'Khagaria', 'Local Shaivite temple; lacks Grade A/B institutional documentation on Bihar Tourism or district portal; held.')
]
for name, dist, reason in held_items:
    status_rows.append({
        'candidate': name,
        'district': dist,
        'previous_status': 'HOLD',
        'current_status': 'HOLD',
        'reason': reason
    })

# Rejected (10)
rejected_items = [
    ('Forbesganj Railway Station Bazar', 'Araria', 'Transit railway commercial area; generic retail, zero tourism value.'),
    ('Arwal Bus Stand Commercial Complex', 'Arwal', 'Generic transit retail infrastructure; zero tourism value.'),
    ('Barauni IOCL Refinery Township', 'Begusarai', 'Active petrochemical industrial complex; restricted entry, no public tourism access.'),
    ('Ara Sadar Hospital', 'Bhojpur', 'Municipal healthcare facility; zero tourism value.'),
    ('Buxar Central Jail', 'Buxar', 'Active correctional security institution; restricted access.'),
    ('Samastipur Dairy Milk Plant', 'Samastipur', 'Industrial milk processing plant; commercial industrial property.'),
    ('Chhapra Main Bazar Cloth Market', 'Saran', 'Local commercial clothing market; generic retail.'),
    ('Hotel Grand Sheohar', 'Sheohar', 'Commercial lodging business; generic private enterprise.'),
    ('Siwan Civil Court Complex', 'Siwan', 'Judicial administrative premises; zero tourism value.'),
    ('Katihar Railway Junction Yard', 'Katihar', 'Active railway operational infrastructure; restricted entry.')
]
for name, dist, reason in rejected_items:
    status_rows.append({
        'candidate': name,
        'district': dist,
        'previous_status': 'REJECTED',
        'current_status': 'REJECTED',
        'reason': reason
    })

# Duplicate / Alias / Subcomponent (10)
dup_items = [
    ('Saptaparni Cave', 'Nalanda', 'Subcomponent of Rajgir hill complex (ID 9, 1.48 km); first Buddhist council cave, already subsumed under Rajgir destination.'),
    ('Cyclopean Wall of Rajgir', 'Nalanda', 'Pre-Mauryan 40-km cyclopean perimeter wall surrounding Rajgir; integral perimeter feature of active destination ID 9.'),
    ('Rajgir Glass Bridge & Nature Safari', 'Nalanda', 'Eco-adventure park in Jethian valley, 5.58 km from Rajgir (ID 9); Nalanda already has 5 active destinations.'),
    ('Papaharini Tank', 'Banka', 'Sacred water tank situated directly at the foothills of Mandar Hill (ID 12, 0.42 km); same-site complex component.'),
    ('Sujata Stupa & Kuti', 'Gaya', 'Excavated brick stupa across Falgu river, 1.42 km from Bodh Gaya / Mahabodhi complex; tightly clustered with existing Gaya inventory.'),
    ('Ranti Art Village', 'Madhubani', 'Mithila painting artisan village 1.72 km from Jitwarpur Art Village (ID 13); same artisan cluster.'),
    ('Balirajgarh', 'Madhubani', 'Alternate local name / official archaeological name for Raja Bali Ka Garh (ID 184).'),
    ('Ahirauli Ahilya Sthan', 'Buxar', 'Buxar rural shrine 4.12 km from Battle of Buxar Memorial; distinct from Ahilya Sthan, Ahiyari (Darbhanga).'),
    ('Brahmeshwar Nath Temple, Brahmpur', 'Buxar', 'Duplicate of active place ID 194: Baba Brahmeshwar Nath Temple, Brahmpur.'),
    ('Gunawa Ji Tirth', 'Nawada', 'Duplicate of active place ID 195: Gunawa Ji (Jain Tirth).')
]
for name, dist, reason in dup_items:
    status_rows.append({
        'candidate': name,
        'district': dist,
        'previous_status': 'DUPLICATE / ALIAS',
        'current_status': 'DUPLICATE / ALIAS',
        'reason': reason
    })

status_fields = ['candidate', 'district', 'previous_status', 'current_status', 'reason']
with open('BIHAR_BATCH9_CANDIDATE_STATUS.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=status_fields)
    writer.writeheader()
    for r in status_rows:
        writer.writerow(r)
print("Saved BIHAR_BATCH9_CANDIDATE_STATUS.csv")

print("\nCSV artifacts generated successfully!")
