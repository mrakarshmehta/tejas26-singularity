import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor
from models.database import PLACE_CATEGORIES

batch5_candidates = [
    {
        "name": "Umga Sun Temple & Rock Complex",
        "district": "Aurangabad",
        "category": "historical",
        "latitude": 24.6312,
        "longitude": 84.5518,
        "slug": "umga-sun-temple-and-rock-complex-aurangabad",
        "description": "Umga Sun Temple & Rock Complex is a monumental 15th-century granite stone temple and rock-cut archaeological site situated atop the rugged Umga hill in Madanpur block of Aurangabad district. Constructed entirely of interlocking square granite blocks without mortar by King Bhairavendra of the Chero dynasty, the site features an ancient 1442 AD Sanskrit stone inscription, 52 rock-cut shrines, ancient Shaivite and Vaishnavite caves, and monolithic rock sculptures, making it one of southern Bihar's most extraordinary megalithic architectural marvels.",
        "best_time_to_visit": "October to March; morning and late afternoon for hill climb",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Ashokan Pillar & Ananda Stupa, Kolhua",
        "district": "Vaishali",
        "category": "historical",
        "latitude": 26.0125,
        "longitude": 85.1124,
        "slug": "ashokan-pillar-and-ananda-stupa-kolhua-vaishali",
        "description": "Ashokan Pillar and Ananda Stupa at Kolhua is an internationally renowned Centrally Protected archaeological monument of the Archaeological Survey of India located near Vaishali. The site features India's most completely preserved monolithic polished Chunar sandstone Ashokan column, standing 18.3 meters high crowned by an intact single seated lion capital facing north toward Buddha's final journey. It encompasses the ancient Ananda Stupa containing sacred relics, the brick Kutagarasala monastery, and the sacred Markata-hrada (Monkey Tank) where Lord Buddha delivered his final sermon.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Nominal ASI entry fee (~Rs. 25 for Indians, Rs. 300 for foreigners)",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Punaura Dham",
        "district": "Sitamarhi",
        "category": "cultural",
        "latitude": 26.6125,
        "longitude": 85.4512,
        "slug": "punaura-dham-sitamarhi",
        "why_add": "Sacred Mata Sita Janmabhoomi pilgrimage site under National PRASHAD scheme",
        "description": "Punaura Dham is one of the supreme pilgrimage centers of Mithila and the officially designated holy birthplace of Goddess Sita (Mata Sita Janmabhoomi) under the Government of India's National PRASHAD Scheme and the Ramayana Circuit. Located 5 km west of Sitamarhi town in Punaura village, the sacred sanctuary marks the spot where King Janaka ploughed the field and discovered baby Sita. The complex features an ancient temple, the sacred Pundarik Sarovar (holy pond) where devotees take ritual dips, and landscaped pilgrim amenities.",
        "best_time_to_visit": "October to March; Janaki Navami and Vivaha Panchami",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Udaipur Wildlife Sanctuary",
        "district": "West Champaran",
        "category": "nature",
        "latitude": 26.8512,
        "longitude": 84.4812,
        "slug": "udaipur-wildlife-sanctuary-west-champaran",
        "description": "Udaipur Wildlife Sanctuary is a premier statutory wetland nature reserve established in 1978 under the Wildlife Protection Act 1972, located near Bettiah in West Champaran district. Spanning 8.74 square kilometers, the sanctuary is centered around Sarayaman Lake, an expansive oxbow lake formed by the meandering Gandak river. The sanctuary provides a vital protected habitat for thousands of resident and migratory waterbirds, spotted deer, barking deer, wild boar, and rich aquatic flora.",
        "best_time_to_visit": "November to March (peak migratory bird migration season)",
        "entry_fee": "Nominal forest checkpost fee (~Rs. 20)",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Chandan Dam",
        "district": "Banka",
        "category": "lake",
        "latitude": 24.7812,
        "longitude": 86.8125,
        "slug": "chandan-dam-banka",
        "description": "Chandan Dam is a monumental multi-embankment earthen reservoir and scenic hill water-tourism destination constructed across the Chandan river in Banka district. Nestled between the rolling forested hills of Chakai and the Banka ranges, this expansive freshwater lake features scenic island knolls, motorboat and paddleboat rides, panoramic reservoir viewpoints, and serene picnic banks, establishing it as eastern Bihar's premier lake eco-tourism hub.",
        "best_time_to_visit": "October to March; post-monsoon for full reservoir views",
        "entry_fee": "Free (boating charges separate)",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary",
        "district": "Vaishali",
        "category": "nature",
        "latitude": 25.7512,
        "longitude": 85.4512,
        "slug": "baraila-lake-salim-ali-bird-sanctuary-vaishali",
        "description": "Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary is a statutory 196-hectare freshwater wetland sanctuary notified in 1997 under Section 18 of the Wildlife Protection Act 1972, situated across Jandaha and Mahnar blocks of eastern Vaishali district. Named in honor of India's renowned ornithologist Dr. Salim Ali, this expansive natural lake (chaur) supports rich biodiversity and serves as a major winter haven for over 59 species of migratory waterfowl, winter raptors, and local aquatic birdlife.",
        "best_time_to_visit": "November to March (peak winter birdwatching season)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "George Orwell Birthplace & Memorial",
        "district": "East Champaran",
        "category": "historical",
        "latitude": 26.6452,
        "longitude": 84.9085,
        "slug": "george-orwell-birthplace-and-memorial-east-champaran",
        "description": "George Orwell Birthplace & Memorial is the historic colonial bungalow in Motihari, East Champaran district, where world-renowned author Eric Arthur Blair (globally celebrated by his pen name George Orwell, author of '1984' and 'Animal Farm') was born on 25 June 1903. Officially designated as a protected State Heritage Monument by the Department of Art, Culture & Youth, Government of Bihar, the site features a restored colonial estate, memorial gallery, and museum celebrating Orwell's literary legacy.",
        "best_time_to_visit": "October to March; 10:00 AM to 5:00 PM",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Kharagpur Lake (Haveli Kharagpur)",
        "district": "Munger",
        "category": "lake",
        "latitude": 25.1215,
        "longitude": 86.5124,
        "slug": "kharagpur-lake-haveli-kharagpur-munger",
        "description": "Kharagpur Lake (Haveli Kharagpur) is a historic scenic water reservoir and hill gorge destination constructed in 1876 by Maharaja Rameswar Singh of Darbhanga Raj across the Man river gorge amidst the Kharagpur hills of Munger district. The lake is framed by dense deciduous sal forests, scenic rocky cliffs, and a natural waterfall gorge, offering visitors peaceful boating, trekking, and nature photography along the forested Bhimbandh hill corridor.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free (boating charges separate)",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Sarvodaya Ashram, Shekhodeora",
        "district": "Nawada",
        "category": "cultural",
        "latitude": 24.8125,
        "longitude": 85.8412,
        "slug": "sarvodaya-ashram-shekhodeora-nawada",
        "description": "Sarvodaya Ashram at Shekhodeora is a historic national freedom sanctuary and social reconstruction center established in 1952 by Bharat Ratna Loknayak Jayaprakash Narayan (JP) and his wife Prabhavati Devi amidst the forested Govindpur hills in Kawakol block of Nawada district. The peaceful 65-acre sanctuary preserves JP's authentic living quarters, historical library, khadi spinning and weaving units, and an organic agriculture training institute, standing as a living monument to India's Sarvodaya movement.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Sujani Embroidery Craft Cluster",
        "district": "Muzaffarpur",
        "category": "cultural",
        "latitude": 26.1512,
        "longitude": 85.4812,
        "slug": "sujani-embroidery-craft-cluster-muzaffarpur",
        "description": "Sujani Embroidery Craft Cluster is an internationally acclaimed living artisan village and traditional needlework craft center located in Bhusura village of Gaighat block in Muzaffarpur district. Honored with the UNESCO Seal of Excellence in 2019 and registered as a statutory Geographical Indication (GI Tag No. 74), Sujani is an ancient textile art where rural women stitch layered narrative quilts depicting social folklore, village life, and women's empowerment. The cluster offers authentic artisan workshops and direct handloom craft tourism.",
        "best_time_to_visit": "October to March; artisan workshops open on weekdays",
        "entry_fee": "Free (artisan products available for direct purchase)",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    }
]

def main():
    print("=== PRE-INSERT VALIDATION FOR BATCH 5 ===")
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        active_count = cur.fetchone()['cnt']
        print(f"1. Current active count: {active_count} (Expected: 108)")
        assert active_count == 108, f"Pre-insert failed: Expected 108, found {active_count}"

        cur.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        covered_districts = cur.fetchone()['cnt']
        print(f"2. Current covered districts: {covered_districts} (Expected: 38)")
        assert covered_districts == 38, f"Pre-insert failed: Expected 38, found {covered_districts}"

        cur.execute("SELECT MAX(id) as max_id FROM places")
        max_id = cur.fetchone()['max_id']
        print(f"3. Current MAX(id): {max_id} (Expected: 158)")
        assert max_id == 158, f"Pre-insert failed: Expected 158, found {max_id}"

        cur.execute("SELECT id, name, slug FROM districts")
        dist_rows = cur.fetchall()
        dist_name_to_id = {}
        for r in dist_rows:
            dist_name_to_id[r['name'].lower()] = r['id']
            # Special case for Jhanjharpur (Madhubani)
            if 'madhubani' in r['name'].lower():
                dist_name_to_id['madhubani'] = r['id']
            if 'west champaran' in r['name'].lower():
                dist_name_to_id['west champaran'] = r['id']
            if 'east champaran' in r['name'].lower():
                dist_name_to_id['east champaran'] = r['id']

        cur.execute("SELECT name, slug, latitude, longitude FROM places WHERE deleted_at IS NULL")
        existing_places = cur.fetchall()
        existing_slugs = set(p['slug'] for p in existing_places)
        existing_names = set(p['name'].lower() for p in existing_places)
        existing_coords = set((round(float(p['latitude']), 4), round(float(p['longitude']), 4)) for p in existing_places if p['latitude'] and p['longitude'])

        valid_cat_keys = set(k for k, _ in PLACE_CATEGORIES) | {'tourist_spot', 'historical', 'temple', 'cultural', 'nature', 'waterfall', 'mountain', 'wildlife', 'lake'}

        print("\n4. Validating 10 Approved Batch 5 Candidates:")
        batch_slugs = set()
        batch_names = set()
        batch_coords = set()

        for idx, c in enumerate(batch5_candidates, 1):
            name = c['name']
            slug = c['slug']
            dist_name = c['district']
            cat = c['category']
            lat = c['latitude']
            lng = c['longitude']

            # District check
            dist_id = dist_name_to_id.get(dist_name.lower())
            assert dist_id is not None, f"District '{dist_name}' not found in database!"
            c['district_id'] = dist_id

            # Name uniqueness
            assert name.lower() not in existing_names, f"Name '{name}' already active in MySQL!"
            assert name.lower() not in batch_names, f"Name '{name}' duplicated in batch!"
            batch_names.add(name.lower())

            # Slug uniqueness
            assert slug not in existing_slugs, f"Slug '{slug}' already active in MySQL!"
            assert slug not in batch_slugs, f"Slug '{slug}' duplicated in batch!"
            batch_slugs.add(slug)

            # Coordinate uniqueness
            coord_tuple = (round(lat, 4), round(lng, 4))
            assert coord_tuple not in existing_coords, f"Coordinates {coord_tuple} already active in MySQL!"
            assert coord_tuple not in batch_coords, f"Coordinates {coord_tuple} duplicated in batch!"
            batch_coords.add(coord_tuple)

            # Category validity
            assert cat in valid_cat_keys, f"Category '{cat}' not valid!"

            print(f"  #{idx:>2}: {name:48} | Dist: {dist_name:15} (ID: {dist_id:>2}) | Cat: {cat:10} | ({lat:.4f}, {lng:.4f}) | Slug: {slug} -> VALID [OK]")

    print("\nPRE-INSERT VALIDATION 100% PASSED! Ready for atomic transaction execution.")

if __name__ == "__main__":
    main()
