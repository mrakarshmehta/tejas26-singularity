import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

batch4_candidates = [
    {
        "name": "Rampurva Ashokan Pillars",
        "district": "West Champaran",
        "district_id": 9,
        "category": "historical",
        "latitude": 27.2685,
        "longitude": 84.5012,
        "slug": "rampurva-ashokan-pillars-west-champaran",
        "description": "Rampurva Ashokan Pillars is an ancient Mauryan archaeological monument situated in Gaunaha block of West Champaran district. Excavated in 1876 by archaeologist A.C.L. Carlleyle, the site features two monumental Ashokan pillar bases and mounds, and is world-renowned as the original provenance of the celebrated Rampurva Bull Capital, preserved under the central dome of Rashtrapati Bhavan, and the Rampurva Lion Capital, now in the Indian Museum, Kolkata. The site is a Centrally Protected Monument under the Archaeological Survey of India.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Phanishwar Nath Renu Smarak & Birthplace",
        "district": "Araria",
        "district_id": 11,
        "category": "cultural",
        "latitude": 26.2486,
        "longitude": 87.2842,
        "slug": "phanishwar-nath-renu-smarak-and-birthplace-araria",
        "description": "Phanishwar Nath Renu Smarak and Birthplace is the ancestral village home and official State literary memorial of Padma Shri Phanishwar Nath 'Renu', the legendary pioneer of regional Hindi literature (Aanchalik Upanyas) and author of the immortal novel 'Maila Anchal'. Located in Aurahi Hingna village of Forbesganj block in Araria district, the memorial complex preserves the author's original handwritten manuscripts, typewriter, library, personal artifacts, and ethnographic glimpses of rural Seemanchal life.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Shergarh Fort",
        "district": "Rohtas",
        "district_id": 8,
        "category": "historical",
        "latitude": 24.8415,
        "longitude": 83.7812,
        "slug": "shergarh-fort-rohtas",
        "description": "Shergarh Fort is an impregnable medieval hill fortress built by Sher Shah Suri between 1540 and 1545 AD, dramatically situated on a high forested summit of the Kaimur plateau above the Durgawati river in Rohtas district. Renowned for its ingenious military architecture, the fort features formidable stone battlements, multi-level subterranean chambers (tehkhanas), cavernous water reservoirs, and an extensive network of secret escape tunnels, making it one of Bihar's most fascinating offbeat heritage destinations.",
        "best_time_to_visit": "October to March (dry winter season for hill trekking)",
        "entry_fee": "Free",
        "family_friendly": 0,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Daud Khan Fort",
        "district": "Aurangabad",
        "district_id": 13,
        "category": "historical",
        "latitude": 25.0315,
        "longitude": 84.4024,
        "slug": "daud-khan-fort-aurangabad",
        "description": "Daud Khan Fort is a historic 17th-century Mughal river fortress and fortified sarai situated on the eastern bank of the Son river in Daudnagar, Aurangabad district. Constructed circa 1660 AD by Daud Khan Quraishi, the Subahdar (Governor) of Bihar under Emperor Aurangzeb, the fort served as a key military garrison and river checkpoint along the historic Patna-Rohtas route. Its massive stone riverfront battlements, peripheral ramparts, and imposing arched entrance gateway remain standing monuments to Mughal defensive architecture.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Lauriya Nandangarh",
        "district": "West Champaran",
        "district_id": 9,
        "category": "historical",
        "latitude": 26.9954,
        "longitude": 84.4124,
        "slug": "lauriya-nandangarh-west-champaran",
        "description": "Lauriya Nandangarh is a monumental ancient archaeological complex situated near the Burhi Gandak river in West Champaran district. The site features a colossal 26-meter-high (80-foot) polygonal terraced brick Buddhist stupa (Nandangarh) dating from the 3rd century BC through the Sunga era, alongside an intact 35-foot polished Chunar sandstone Ashokan monolithic column crowned by a seated lion capital with an abacus depicting flying geese. Protected by the Archaeological Survey of India, it is one of India's most impressive ancient structural landscapes.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Rajnagar Palace Complex",
        "district": "Madhubani",
        "district_id": 20,
        "category": "historical",
        "latitude": 26.3912,
        "longitude": 86.1485,
        "slug": "rajnagar-palace-complex-madhubani",
        "description": "Rajnagar Palace Complex is a monumental palatial ruin and temple heritage site situated on the Kamla river in Rajnagar block of Madhubani district. Built between 1884 and 1929 by Maharaja Rameshwar Singh of Darbhanga Raj, the complex showcases Indo-Saracenic and tantric architectural styles. Key features include the dramatic ruins of the Navlakha Palace, an intact monumental white marble temple dedicated to Goddess Kali (Girija Mandir), ornate royal gates, and sacred ponds, creating Mithila's foremost architectural photography and heritage destination.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Kaimur Wildlife Sanctuary & Adhaura Hills",
        "district": "Kaimur",
        "district_id": 22,
        "category": "nature",
        "latitude": 24.8125,
        "longitude": 83.6125,
        "slug": "kaimur-wildlife-sanctuary-and-adhaura-hills-kaimur",
        "description": "Kaimur Wildlife Sanctuary is the largest wildlife sanctuary in Bihar, spanning over 1,504 square kilometers across the rugged Kaimur plateau. Established under the Wildlife Protection Act 1972 and granted in-principle approval by the NTCA to become Bihar's second Tiger Reserve, the sanctuary encompasses dense dry deciduous sal and teak forests, scenic sandstone river gorges, and waterfalls. Centered around the scenic hill station of Adhaura, the sanctuary also houses prehistoric rock shelters adorned with ancient mesolithic and neolithic rock paintings.",
        "best_time_to_visit": "October to April",
        "entry_fee": "Nominal forest entry fee at checkpost (~Rs. 30)",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Simaria Ghat & Dinkar Memorial",
        "district": "Begusarai",
        "district_id": 15,
        "category": "cultural",
        "latitude": 25.4382,
        "longitude": 85.9921,
        "slug": "simaria-ghat-and-dinkar-memorial-begusarai",
        "description": "Simaria Ghat and Dinkar Memorial is a celebrated cultural, riverfront, and literary destination situated on the northern bank of the sacred River Ganga adjacent to Rajendra Setu in Begusarai district. Revered as an ancient pilgrimage bathing ghat hosting the month-long Kalpwas Mela recognized as an official State Fair, the site is undergoing major riverfront promenade transformation. Simaria is also the birthplace of Rashtrakavi Ramdhari Singh 'Dinkar', featuring his ancestral home, a memorial library, and museum honoring the national poet.",
        "best_time_to_visit": "October to March; Kalpwas Mela period (Kartik month)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Jal Mandir, Pawapuri",
        "district": "Nalanda",
        "district_id": 3,
        "category": "temple",
        "latitude": 25.0925,
        "longitude": 85.5385,
        "slug": "jal-mandir-pawapuri-nalanda",
        "description": "Jal Mandir at Pawapuri is the supreme world pilgrimage destination of Jainism, marking the holy site of Nirvana (Moksha) and cremation of Lord Mahavira, the 24th Tirthankara, in 527 BC. Located approximately 16 km east of Rajgir in Nalanda district, the exquisite temple is constructed entirely of white marble and sits serenely in the middle of a massive 84-acre blooming lotus water reservoir. Devotees access the central island shrine via a 600-foot red sandstone footbridge, creating an architectural and spiritual masterpiece.",
        "best_time_to_visit": "October to March; Diwali / Mahavira Nirvana Mahotsav",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Gupta Dham (Gupteshwar Mahadev Cave)",
        "district": "Rohtas",
        "district_id": 8,
        "category": "nature",
        "latitude": 24.7512,
        "longitude": 83.7912,
        "slug": "gupta-dham-gupteshwar-mahadev-cave-rohtas",
        "description": "Gupta Dham (Gupteshwar Mahadev Cave) is an extraordinary subterranean geological marvel and revered pilgrimage shrine nestled deep inside the forested limestone gorges of the Kaimur hills in Rohtas district. The natural karst cave extends for hundreds of meters into the mountain, showcasing spectacular stalactite and stalagmite dripstone rock formations, underground water streams, and an ancient natural Shiva lingam that draws hundreds of thousands of pilgrims during Mahashivratri and the holy month of Shravan.",
        "best_time_to_visit": "October to March; Mahashivratri and Shravan",
        "entry_fee": "Free",
        "family_friendly": 0,
        "is_hidden_gem": 1,
        "best_season": "winter"
    }
]

print("=== PRE-INSERT VALIDATION ===")
with get_cursor() as cursor:
    cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
    active_places = cursor.fetchone()['cnt']
    print(f"Current active count: {active_places} (Expected: 98)")
    assert active_places == 98, f"Pre-check failed: Expected 98 active places, found {active_places}"

    cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
    covered_districts = cursor.fetchone()['cnt']
    print(f"Current covered districts: {covered_districts} (Expected: 38)")
    assert covered_districts == 38, f"Pre-check failed: Expected 38 districts, found {covered_districts}"

    cursor.execute("SELECT MAX(id) as max_id FROM places")
    max_id = cursor.fetchone()['max_id']
    print(f"Current MAX(id): {max_id} (Expected: 148)")
    assert max_id == 148, f"Pre-check failed: Expected MAX(id) 148, found {max_id}"

    cursor.execute("SELECT name, slug, latitude, longitude FROM places WHERE deleted_at IS NULL")
    existing_places = cursor.fetchall()
    existing_slugs = set(p['slug'] for p in existing_places)
    existing_names = set(p['name'].lower() for p in existing_places)
    existing_coords = set((round(float(p['latitude']), 4), round(float(p['longitude']), 4)) for p in existing_places)

    print("\nValidating 10 Approved Batch 4 Candidates:")
    for idx, c in enumerate(batch4_candidates, 1):
        name = c['name']
        dist = c['district']
        dist_id = c['district_id']
        cat = c['category']
        lat = c['latitude']
        lng = c['longitude']
        slug = c['slug']

        # 1. Not already active
        assert name.lower() not in existing_names, f"Validation failure: Name '{name}' already exists in active database!"
        
        # 2. Slug uniqueness
        assert slug not in existing_slugs, f"Validation failure: Slug '{slug}' already exists in active database!"
        
        # 3. Coordinate uniqueness
        c_coord = (round(lat, 4), round(lng, 4))
        assert c_coord not in existing_coords, f"Validation failure: Coordinate pair {c_coord} already exists in active database!"
        
        # 4. Valid category
        from models.database import PLACE_CATEGORIES
        valid_cat_keys = set(k for k, _ in PLACE_CATEGORIES) | {'tourist_spot', 'historical', 'temple', 'cultural', 'nature', 'waterfall', 'mountain', 'wildlife', 'lake'}
        assert cat in valid_cat_keys, f"Validation failure: Category '{cat}' is not in valid categories!"
        
        print(f"  #{idx:>2}: {name:42} | Dist: {dist} (ID: {dist_id}) | Cat: {cat:10} | ({lat:.4f}, {lng:.4f}) | Slug: {slug} -> VALID [OK]")

print("\nPRE-INSERT VALIDATION 100% PASSED! Ready for atomic transaction execution.")
