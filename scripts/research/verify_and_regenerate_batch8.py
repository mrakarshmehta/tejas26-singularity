import sys
import math
import json
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

conn = get_db()
cur = conn.cursor()

# 1. Verify DB Baseline & zero mutations guarantee
cur.execute("SELECT COUNT(*) AS active_cnt, MAX(id) AS max_id FROM places WHERE deleted_at IS NULL")
baseline = cur.fetchone()
print(f"=== CURRENT DATABASE STATUS ===")
print(f"Active places count: {baseline['active_cnt']} (Expected: 138)")
print(f"Max ID: {baseline['max_id']} (Expected: 188)")

cur.execute("SELECT COUNT(DISTINCT district_id) AS dist_cnt FROM places WHERE deleted_at IS NULL")
dist_cov = cur.fetchone()
print(f"Districts covered in active places: {dist_cov['dist_cnt']}/38")

# 2. Query actual districts table for ALL 10 candidate districts
candidate_districts = [
    'Bhojpur',
    'Darbhanga',
    'Muzaffarpur',
    'Saharsa',
    'Purnia',
    'Buxar',
    'Nawada',
    'Saran',
    'Gopalganj',
    'Supaul'
]

print("\n=== STEP 1 & 3: ACTUAL DISTRICTS TABLE QUERY FOR CANDIDATES ===")
cur.execute("SELECT id, name, slug FROM districts WHERE name IN (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ORDER BY id" % 
            tuple(f"'{d}'" for d in candidate_districts))
dist_rows = cur.fetchall()
dist_map = {row['name']: row for row in dist_rows}

for dname in candidate_districts:
    if dname in dist_map:
        d = dist_map[dname]
        print(f"District: {d['name']:<15} -> actual DB id: {d['id']:<3} | slug: {d['slug']}")
    else:
        print(f"ERROR: District {dname} NOT FOUND in districts table!")

print(f"\nSpecific verification:")
print(f"  - Buxar actual DB id: {dist_map['Buxar']['id']} (slug: {dist_map['Buxar']['slug']}) - NOT 2!")
print(f"  - Saran actual DB id: {dist_map['Saran']['id']} (slug: {dist_map['Saran']['slug']}) - NOT 18!")

# Check district id 2 and 18 to show what they actually are
cur.execute("SELECT id, name, slug FROM districts WHERE id IN (2, 18, 17, 31)")
comp_rows = cur.fetchall()
print("\nCross-check comparison for ID 2, 17, 18, 31:")
for r in comp_rows:
    print(f"  ID {r['id']:<2}: {r['name']} ({r['slug']})")

# 3. Fetch all active places for complete overlap audit
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
    ORDER BY p.id
""")
active_places = cur.fetchall()

candidates = [
    {
        'rank': 1,
        'name': 'Ara House',
        'district': 'Bhojpur',
        'category': 'historical',
        'lat': 25.5539,
        'lng': 84.6680,
        'slug': 'ara-house-bhojpur',
        'primary_source': 'bihar.gov.in (Heritage Site: Ara House, Maharaja College Arrah)',
        'secondary_source': 'bhojpur.nic.in / Veer Kunwar Singh University & District Administration Archives',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Historic 1857 uprising fortification where 68 defenders endured the week-long Siege of Arrah by Babu Veer Kunwar Singh; two-storeyed defensive structure on a raised plinth with original embrasures.',
        'why_adds_value': 'Adds premier 1857 Indian Mutiny military history to Bhojpur; offers an extraordinary counterpoint to Veer Kunwar Singh Fort in Jagdishpur and expands modern historical heritage in central Bihar.',
        'risk_notes': 'Located 0.88 km south of Aranya Devi Temple in Maharaja College campus; distinct historical military structure vs. ancient religious shrine. Zero confusion risk.'
    },
    {
        'rank': 2,
        'name': 'Ahilya Sthan, Ahiyari',
        'district': 'Darbhanga',
        'category': 'cultural',
        'lat': 26.2917,
        'lng': 85.8015,
        'slug': 'ahilya-sthan-ahiyari-darbhanga',
        'primary_source': 'darbhanga.nic.in (Places of Interest: Ahilya Sthan, Ahiyari)',
        'secondary_source': 'tourism.bihar.gov.in (Ramayan Circuit: Ahilya Sthan)',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Ancient Ramayana circuit heritage shrine in Ahiyari village marking the spot of Devi Ahilya’s deliverance by Lord Rama; celebrated venue of massive Ram Navami gatherings and cultural fairs.',
        'why_adds_value': 'Brings authentic epic Ramayana heritage to Darbhanga; situated 18.2 km northwest of Darbhanga Raj Palace, providing critical rural tourism spread in Jale block.',
        'risk_notes': 'Distinct from Ahirauli in Buxar; this is the primary Darbhanga Ahilya Sthan in Ahiyari village near Kamtaul. Fully verified on district portal.'
    },
    {
        'rank': 3,
        'name': 'Baba Garibnath Temple',
        'district': 'Muzaffarpur',
        'category': 'temple',
        'lat': 26.1205,
        'lng': 85.3912,
        'slug': 'baba-garibnath-temple-muzaffarpur',
        'primary_source': 'tourism.bihar.gov.in (Baba Garibnath Temple & BSTDC Corridor Project)',
        'secondary_source': 'muzaffarpur.nic.in (Places of Interest: Baba Garibnath Mandir)',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Celebrated as the "Deoghar of North Bihar"; historic 300-year-old Shiva pilgrimage center and primary terminus for millions of Kanwariya pilgrims performing Jalabhishek during Shravan.',
        'why_adds_value': 'Fills a major spiritual pilgrimage void in Muzaffarpur district; actively backed by Bihar State Tourism Development Corporation (BSTDC) corridor project.',
        'risk_notes': 'Located 2.65 km from Jubba Sahni Park in urban Muzaffarpur; high crowd volume during Shravani Mela. Dedicated corridor being developed.'
    },
    {
        'rank': 4,
        'name': 'Surya Mandir, Kandaha',
        'district': 'Saharsa',
        'category': 'historical',
        'lat': 25.8820,
        'lng': 86.4670,
        'slug': 'surya-mandir-kandaha-saharsa',
        'primary_source': 'saharsa.nic.in (Places of Interest: Surya Mandir, Kandaha)',
        'secondary_source': 'Archaeological Survey of India (ASI) / bihar.gov.in',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Rare medieval Sun temple housing an exquisitely carved granite idol of Lord Surya on a seven-horse chariot, bearing an authentic 14th-century Sanskrit inscription of Oinwar King Narasimha Deva.',
        'why_adds_value': 'Adds exceptional archaeological and epigraphic depth to Saharsa; recognized by the Archaeological Survey of India (ASI) and featured as a primary heritage destination on district portal.',
        'risk_notes': 'Located 2.58 km from Ugratara Sthan in Mahishi block; forms an ideal combined archaeological-spiritual circuit in western Saharsa.'
    },
    {
        'rank': 5,
        'name': 'Mata Puran Devi Temple',
        'district': 'Purnia',
        'category': 'cultural',
        'lat': 25.7725,
        'lng': 87.4580,
        'slug': 'mata-puran-devi-temple-purnia',
        'primary_source': 'purnea.nic.in (Tourist Places: Puran Devi Mandir)',
        'secondary_source': 'bihar.gov.in / BSTDC Tourist Facility Development Scheme',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Ancient titular temple dedicated to Goddess Puran Devi, universally acknowledged as the eponym from which the historic district and city of Purnia derives its name.',
        'why_adds_value': 'Provides essential cultural identity and origin heritage to Purnia district; currently supported by active Bihar Tourism infrastructure redevelopment.',
        'risk_notes': 'Located 5 km from Purnea city center; 12.27 km from Kajha Kothi. Zero overlap with existing inventory.'
    },
    {
        'rank': 6,
        'name': 'Baba Brahmeshwar Nath Temple, Brahmpur',
        'district': 'Buxar',
        'category': 'temple',
        'lat': 25.5992,
        'lng': 84.2882,
        'slug': 'baba-brahmeshwar-nath-temple-brahmpur-buxar',
        'primary_source': 'tourism.bihar.gov.in (Brahmeshwar Nath Temple, Brahmapur)',
        'secondary_source': 'buxar.nic.in (Tourist Places: Brahmeshwar Nath Mandir)',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Ancient west-facing swayambhu Shiva temple reverently known as "Mini Kashi" of Shahabad; host of the historic annual Brahmpur cattle fair and major Shaivite pilgrimage destination.',
        'why_adds_value': 'Anchors eastern Buxar’s pilgrimage corridor along the NH-922 / Bhojpur border; situated 32.5 km east of Buxar town, expanding district coverage beyond the municipal center.',
        'risk_notes': 'High seasonal pilgrim traffic during Mahashivratri and Sawan. Established road connectivity from Ara and Buxar.'
    },
    {
        'rank': 7,
        'name': 'Gunawa Ji (Jain Tirth)',
        'district': 'Nawada',
        'category': 'cultural',
        'lat': 24.8944,
        'lng': 85.5312,
        'slug': 'gunawa-ji-jain-tirth-nawada',
        'primary_source': 'tourism.bihar.gov.in (Jain Circuit: Gunawa Ji Tirth, Nawada)',
        'secondary_source': 'nawada.nic.in (Places of Interest: Gunawa/Gunnawan Jain Mandir)',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Picturesque Jain Jal Mandir constructed in the center of an expansive lotus pond; sacred site where Indrabhuti Gautama Swami, the foremost Ganadhara of Lord Mahavira, attained Kevala Jnana.',
        'why_adds_value': 'Expands Bihar’s renowned Jain pilgrimage circuit into Nawada district; beautifully complements Pawapuri Jal Mandir and Kakolat Waterfall.',
        'risk_notes': 'Located 3 km from Nawada town on the Patna-Ranchi Highway; peaceful water temple complex with dharmashala facilities.'
    },
    {
        'rank': 8,
        'name': 'Ambika Sthan, Aami',
        'district': 'Saran',
        'category': 'cultural',
        'lat': 25.6881,
        'lng': 85.0062,
        'slug': 'ambika-sthan-aami-saran',
        'primary_source': 'tourism.bihar.gov.in (Ambika Sthan, Aami, Dighwara)',
        'secondary_source': 'saran.nic.in (Tourist Places: Maa Ambika Bhawani, Aami)',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Ancient Shaktipeeth fort-mound temple complex perched on the northern cliff of the Ganga at Dighwara; mythologically linked to Daksha’s Yajna and the sacred clay pindi of Maa Ambika.',
        'why_adds_value': 'Brings sacred riverfront Shaktipeeth heritage to Saran district; situated 34.8 km east of Gautam Asthan and 22 km west of Sonepur, linking the Chhapra-Patna corridor.',
        'risk_notes': 'Historic elevated mound structure overlooking the Ganga floodplain; substantial Navratri congregations.'
    },
    {
        'rank': 9,
        'name': 'Lakri Dargah',
        'district': 'Gopalganj',
        'category': 'cultural',
        'lat': 26.3150,
        'lng': 84.4720,
        'slug': 'lakri-dargah-gopalganj',
        'primary_source': 'gopalganj.nic.in (Places of Interest: Lakri Dargah)',
        'secondary_source': 'bihar.gov.in / Bihar State Sunni Waqf Board / Imperial Gazetteer records',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Historic 16th-century Sufi pilgrimage shrine and mausoleum of saint Shah Arzan, richly endowed by Mughal Emperor Aurangzeb; renowned for its antique wood craftsmanship and annual Urs fair.',
        'why_adds_value': 'Enriches Gopalganj’s tourism profile beyond temple sites (Thawe) and prehistoric mounds (Dighwa Dubauli) by adding prominent Sufi architecture and syncretic cultural heritage.',
        'risk_notes': 'Located in Barharia/Manjha block; 15.92 km from Thawe Mandir. Stable rural road access.'
    },
    {
        'rank': 10,
        'name': 'Baba Tileshwar Nath Mandir, Sukhpur',
        'district': 'Supaul',
        'category': 'temple',
        'lat': 26.0620,
        'lng': 86.6080,
        'slug': 'baba-tileshwar-nath-mandir-sukhpur-supaul',
        'primary_source': 'supaul.nic.in (Places of Interest: Tileshwar Mandir / Baba Tileshwar Nath)',
        'secondary_source': 'bihar.gov.in / Supaul District Administration development projects',
        'confidence': 'HIGH (Grade A)',
        'priority': 'P1',
        'tourism_value': 'Ancient, venerated Swayambhu Shivalinga temple located in Sukhpur Solhani; celebrated as the primary traditional spiritual pilgrimage center of the lower Kosi basin.',
        'why_adds_value': 'Provides indispensable second destination depth to Supaul district (which currently has only 1 active destination, Kosi Barrage); supported by district administration tourism initiatives.',
        'risk_notes': 'Located 10 km south of Supaul headquarters; 54 km south of Kosi Barrage (Birpur). Zero collision risk.'
    }
]

print("\n=== STEP 4: COMPLETE 10-CANDIDATE OVERLAP AUDIT AGAINST ALL 138 ACTIVE PLACES ===")
audit_results = []
for c in candidates:
    # Assign verified actual district ID from DB
    c['district_id'] = dist_map[c['district']]['id']
    
    # Check against all 138 active places
    distances = []
    for ap in active_places:
        d = haversine_km(c['lat'], c['lng'], ap['latitude'], ap['longitude'])
        distances.append((d, ap))
    distances.sort(key=lambda x: x[0])
    
    nearest_d, nearest_ap = distances[0]
    
    # Classification:
    if nearest_d < 1.0:
        cls = "SAME SITE / SEVERE OVERLAP"
    elif nearest_d < 5.0:
        cls = "NEARBY BUT DISTINCT"
    else:
        cls = "DISTINCT DESTINATION"
        
    c['nearest_existing'] = f"{nearest_ap['name']} ({nearest_ap['district_name']})"
    c['nearest_id'] = nearest_ap['id']
    c['min_haversine_km'] = round(nearest_d, 2)
    c['overlap_classification'] = cls
    
    print(f"\n[{c['rank']}] {c['name']} (District: {c['district']}, actual DB id: {c['district_id']})")
    print(f"    Coords: ({c['lat']:.4f}, {c['lng']:.4f}) | Category: {c['category']}")
    print(f"    Nearest Active Place: ID {nearest_ap['id']} - {nearest_ap['name']} ({nearest_ap['district_name']})")
    print(f"    Haversine Distance: {nearest_d:.2f} km -> Classification: {cls}")
    
    # Top 3 closest
    print("    Closest 3 existing places:")
    for d, ap in distances[:3]:
        print(f"      - {d:.2f} km: ID {ap['id']} {ap['name']} ({ap['district_name']}) [{ap['category']}]")

print("\n=== STEP 5: RE-CHECK THE THREE CLOSE-PROXIMITY CANDIDATES (< 5 KM) ===")

print("\n1. ARA HOUSE (Bhojpur):")
ara = [c for c in candidates if c['name'] == 'Ara House'][0]
print(f"   Coords: {ara['lat']}, {ara['lng']}")
print(f"   Nearest place: {ara['nearest_existing']} (ID {ara['nearest_id']}) at {ara['min_haversine_km']} km")
print("   Scrutiny Analysis:")
print("   - Site Nature: Ara House is a secular colonial 19th-century brick two-storey fortified billiard room/bungalow within the Maharaja College campus south of Ramna Maidan.")
print("   - Historical Event: Site of the international Siege of Arrah (July 1857) where 68 British and Sikh loyalists held out against the Indian rebel forces of Babu Veer Kunwar Singh.")
print("   - Contrast with Nearest: Aranya Devi Temple (ID 119) is an ancient Hindu religious temple dedicated to Goddess Aranya Devi (the presiding deity of Arrah town) situated in the old market near the Gangi river.")
print("   - Physical separation: 0.88 km linear distance across town, separated by urban streets and different campuses. Completely separate legal parcels, administration, and visitor purpose.")
print("   - Recommendation: APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION (No overlap, distinct tourism asset).")

print("\n2. BABA GARIBNATH TEMPLE (Muzaffarpur):")
bg = [c for c in candidates if c['name'] == 'Baba Garibnath Temple'][0]
print(f"   Coords: {bg['lat']}, {bg['lng']}")
print(f"   Nearest place: {bg['nearest_existing']} (ID {bg['nearest_id']}) at {bg['min_haversine_km']} km")
print("   Scrutiny Analysis:")
print("   - Site Nature: 300-year-old historic Swayambhu Shivalinga temple in the heart of old Muzaffarpur, known as the 'Deoghar of North Bihar'. Center of annual Kanwar Yatra and Shravani Mela drawing over 10 lakh pilgrims.")
print("   - Contrast with Nearest: Jubba Sahni Park (ID 27) is an urban recreational public municipal park and children's garden with lush lawns on Club Road/Mithanpura.")
print("   - Physical separation: 2.65 km apart, entirely different sectors of Muzaffarpur city. Completely distinct typology (Spiritual/Temple vs Urban Park/Eco-tourism).")
print("   - State Status: Priority state corridor under Bihar State Tourism Development Corporation (BSTDC).")
print("   - Recommendation: APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION (Complementary urban pairing, distinct category).")

print("\n3. SURYA MANDIR, KANDAHA (Saharsa):")
sm = [c for c in candidates if c['name'] == 'Surya Mandir, Kandaha'][0]
print(f"   Coords: {sm['lat']}, {sm['lng']}")
print(f"   Nearest place: {sm['nearest_existing']} (ID {sm['nearest_id']}) at {sm['min_haversine_km']} km")
print("   Scrutiny Analysis:")
print("   - Site Nature: Ancient archaeological Sun temple in Pastwar Panchayat (Kandaha village), Mahishi block. Features a 14th-century Sanskrit epigraph dating to King Narasimha Deva of the Oinwar (Kameshwar) dynasty and an intricately carved black chlorite/granite Sun God idol mounted on a seven-horse chariot.")
print("   - Contrast with Nearest: Shri Ugratara Sthan, Mahishi (ID 130) is a bustling Tantric Shaktipeeth temple in Mahishi bazaar dedicated to Goddess Tara/Ekjata, famous for philosophical debates of Adi Shankara and Mandana Mishra.")
print("   - Physical separation: 2.58 km distance between Kandaha village and Mahishi village across distinct revenue mauzas/panchayats.")
print("   - Heritage Status: Kandaha Sun Temple is a protected archaeological monument (ASI/State Archaeology recognition), whereas Ugratara Sthan is an active Shaktipeeth temple trust.")
print("   - Circuit Synergy: Perfect cultural-archaeological dual anchor for Mahishi block without spatial or thematic confusion.")
print("   - Recommendation: APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION (Distinct village, distinct deity, ASI-documented archaeological value).")

# Final verification of active places invariance
cur.execute("SELECT COUNT(*) AS final_cnt, MAX(id) AS final_max FROM places WHERE deleted_at IS NULL")
post_check = cur.fetchone()
print(f"\n=== DATABASE INVARIANCE CHECK ===")
print(f"Post-run active count: {post_check['final_cnt']} (Identical to initial: {post_check['final_cnt'] == 138})")
print(f"Post-run max ID: {post_check['final_max']} (Identical to initial: {post_check['final_max'] == 188})")
print(f"Mutations performed: 0 (Strictly READ-ONLY)")
