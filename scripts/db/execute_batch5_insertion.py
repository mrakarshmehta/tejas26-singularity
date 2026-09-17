import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_db

batch5_data = [
    {
        "name": "Umga Sun Temple & Rock Complex",
        "district": "Aurangabad",
        "district_id": 13,
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
        "district_id": 37,
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
        "district_id": 34,
        "category": "cultural",
        "latitude": 26.6125,
        "longitude": 85.4512,
        "slug": "punaura-dham-sitamarhi",
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
        "district_id": 9,
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
        "district_id": 14,
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
        "district_id": 37,
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
        "district_id": 10,
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
        "district_id": 6,
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
        "district_id": 38,
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
        "district_id": 7,
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
    conn = get_db()
    conn.autocommit = False
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_count = row['COUNT(*)'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert active count: {pre_count}")
        if pre_count != 108:
            raise RuntimeError(f"Expected 108 active places before insert, found {pre_count}")
            
        inserted_ids = []
        
        insert_query = """
            INSERT INTO places (
                state_id, district_id, name, slug, description, category,
                latitude, longitude, maps_link, cover_image, is_featured,
                is_hidden_gem, family_friendly, best_time_to_visit, entry_fee,
                best_season
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s
            )
        """
        
        for p in batch5_data:
            maps_link = f"https://www.google.com/maps?q={p['latitude']:.4f},{p['longitude']:.4f}"
            values = (
                1, # state_id: Bihar
                p['district_id'],
                p['name'],
                p['slug'],
                p['description'],
                p['category'],
                p['latitude'],
                p['longitude'],
                maps_link,
                "", # cover_image
                0,  # is_featured
                p['is_hidden_gem'],
                p['family_friendly'],
                p['best_time_to_visit'],
                p['entry_fee'],
                p['best_season']
            )
            cursor.execute(insert_query, values)
            new_id = cursor.lastrowid
            inserted_ids.append((new_id, p['name'], p['district_id'], p['category'], p['slug'], p['latitude'], p['longitude']))
            print(f"  Inserted ID {new_id}: {p['name']} (District ID: {p['district_id']}, Category: {p['category']})")
        
        if len(inserted_ids) != 10:
            raise RuntimeError(f"Expected exactly 10 inserts, but got {len(inserted_ids)}")
            
        # Post-check count within transaction
        cursor.execute("SELECT COUNT(*) FROM places WHERE deleted_at IS NULL")
        post_count = cursor.fetchone()
        post_count_val = post_count['COUNT(*)'] if isinstance(post_count, dict) else post_count[0]
        print(f"Post-insert active count in transaction: {post_count_val}")
        if post_count_val != 118:
            raise RuntimeError(f"Expected 118 active places, found {post_count_val}")
            
        # All 10 succeeded -> COMMIT!
        conn.commit()
        print("\nTRANSACTION COMMITTED SUCCESSFULLY! All 10 places inserted atomically.")
        print("Inserted IDs:", [x[0] for x in inserted_ids])
        
    except Exception as e:
        conn.rollback()
        print(f"\nERROR: Insertion failed, TRANSACTION ROLLED BACK! Error: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
