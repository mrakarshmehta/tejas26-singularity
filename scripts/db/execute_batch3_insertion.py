import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_db

batch3_data = [
    {
        "name": "Saurath Sabha Gachhi",
        "district_id": 20, # Jhanjharpur (Madhubani)
        "category": "cultural",
        "latitude": 26.4125,
        "longitude": 86.0954,
        "slug": "saurath-sabha-gachhi-madhubani",
        "description": "Saurath Sabha Gachhi is a globally unique living anthropological and cultural heritage site situated in Saurath village of Madhubani district. Spanning a sacred banyan grove dating back over seven centuries to the Karnat dynasty, this historic assembly ground hosts an annual congregation where Maithil Brahmin families and certified genealogists (Panjikars) gather to consult palm-leaf genealogical records (Panji Prabandha) and negotiate marital alliances. The site is a revered living monument to Mithila's rich intellectual and social heritage.",
        "best_time_to_visit": "May to July (during annual Sabha season) and October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Tutla Bhawani Waterfall & Hanging Bridge",
        "district_id": 8, # Rohtas
        "category": "waterfall",
        "latitude": 24.7815,
        "longitude": 84.0125,
        "slug": "tutla-bhawani-waterfall-and-hanging-bridge-rohtas",
        "description": "Tutla Bhawani Waterfall and Hanging Bridge is a premier eco-tourism destination located in the picturesque Kachhuar canyon of the Kaimur hills in Rohtas district. The site features a spectacular natural waterfall plunging down red sandstone cliffs, an ancient 12th-century Nayadatta rock inscription dating to Vikram Samvat 1214 (1158 AD), an active rock-cut shrine dedicated to Goddess Jagaddhatri, and Bihar's pioneering glass-bottomed suspension hanging bridge spanning the canyon gorge.",
        "best_time_to_visit": "July to February (post-monsoon for maximum waterfall flow)",
        "entry_fee": "Nominal eco-development fee (~Rs. 30 per person)",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Bateshwar Sthan & Patharghata Caves",
        "district_id": 5, # Bhagalpur
        "category": "historical",
        "latitude": 25.3341,
        "longitude": 87.2712,
        "slug": "bateshwar-sthan-and-patharghata-caves-bhagalpur",
        "description": "Bateshwar Sthan and Patharghata Caves is an ancient Centrally Protected archaeological and spiritual complex located on the south bank of the River Ganga in Kahalgaon block of Bhagalpur district. The site features remarkable 6th to 8th century rock-cut caves known as Chaurasi Munis (84 Sages) adorned with bas-relief sculptures depicting Ramayana and Mahabharata episodes, alongside the historic Bateshwar Nath Shiva temple overlooking the sacred northern bend (Uttaravahini) of the Ganga.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Bio-Diversity Park, Kusiargaon",
        "district_id": 11, # Araria
        "category": "nature",
        "latitude": 26.1158,
        "longitude": 87.4589,
        "slug": "bio-diversity-park-kusiargaon-araria",
        "description": "Bio-Diversity Park at Kusiargaon is the premier institutional eco-park in the Seemanchal region of northeastern Bihar, situated along National Highway 57 in Araria district. Developed across more than 50 acres by the Department of Environment, Forest and Climate Change, the park conserves over 250 species of medicinal, endangered, and indigenous flora, featuring landscaped botanical gardens, a bamboo grove, a natural wetland sanctuary, and educational nature trails.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Nominal entry fee (~Rs. 20 for adults, Rs. 10 for children)",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Dhuan Kund & Manjhar Kund Waterfalls",
        "district_id": 8, # Rohtas
        "category": "waterfall",
        "latitude": 24.8912,
        "longitude": 84.0124,
        "slug": "dhuan-kund-and-manjhar-kund-waterfalls-rohtas",
        "description": "Dhuan Kund and Manjhar Kund are twin perennial waterfalls cascading over 100 feet down the forested sandstone cliffs of the Kaimur plateau, located approximately 10 km southwest of Sasaram in Rohtas district. The intense plunge of the water creates a perpetual mist or vapor cloud that gives Dhuan Kund its evocative name ('Smoke Pool'). The waterfalls are also the historic venue for an annual post-monsoon cultural mela on Raksha Bandhan that has been celebrated for over a century.",
        "best_time_to_visit": "August to February (peak flow post-monsoon)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Someshwar Fort & Hills",
        "district_id": 9, # West Champaran
        "category": "mountain",
        "latitude": 27.4685,
        "longitude": 84.3125,
        "slug": "someshwar-fort-and-hills-west-champaran",
        "description": "Someshwar Fort and Hills marks the highest geographical summit in Bihar at an elevation of approximately 865 meters (2,838 feet) above sea level, located along the Indo-Nepal international border in West Champaran district. Crowned by Border Pillar 87 and the atmospheric ruins of a medieval stone frontier fort, the peak offers breathtaking panoramic views of the Terai plains, dense sal forests, and snow-capped Himalayan peaks on clear winter days, making it Bihar's premier mountain trekking destination.",
        "best_time_to_visit": "October to March (dry winter season for clear mountain views)",
        "entry_fee": "Free (Border outpost identity verification required by SSB)",
        "family_friendly": 0,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Ghora Katora Lake Eco-Reserve",
        "district_id": 3, # Nalanda
        "category": "nature",
        "latitude": 24.9921,
        "longitude": 85.4812,
        "slug": "ghora-katora-lake-eco-reserve-nalanda",
        "description": "Ghora Katora Lake Eco-Reserve is a pristine natural water body situated in a scenic valley between the historic hills of Rajgir in Nalanda district. Strictly maintained as a zero-emission eco-tourism zone where only electric vehicles, bicycles, and horse carts are permitted, the lake features pedal boating and a monumental 70-foot standing statue of Lord Buddha carved from pink Chunar sandstone standing gracefully in the center of the waters.",
        "best_time_to_visit": "October to March; morning and late afternoon",
        "entry_fee": "Eco-zone entry fee (~Rs. 20; electric cart transport extra)",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Kusheshwar Asthan Bird Sanctuary & Temple",
        "district_id": 18, # Darbhanga
        "category": "nature",
        "latitude": 25.8125,
        "longitude": 86.1158,
        "slug": "kusheshwar-asthan-bird-sanctuary-and-temple-darbhanga",
        "description": "Kusheshwar Asthan Bird Sanctuary and Temple is a unique dual-heritage destination in southeastern Darbhanga district. Declared a statutory Wildlife Sanctuary under the Wildlife Protection Act 1972, the vast 7,014-hectare wetland ecosystem (chaurs) hosts thousands of Central Asian migratory waterfowl including pelicans, Siberian cranes, and bar-headed geese every winter. The sanctuary adjoins the ancient Baba Kusheshwarnath Shiva temple, a celebrated Shaivite pilgrimage shrine drawing over 200,000 devotees during Shravan.",
        "best_time_to_visit": "November to March (winter bird migration season)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Areraj Someshwar Nath Temple & Ashokan Pillar",
        "district_id": 10, # East Champaran
        "category": "historical",
        "latitude": 26.5412,
        "longitude": 84.7485,
        "slug": "areraj-someshwar-nath-temple-and-ashokan-pillar-east-champaran",
        "description": "Areraj Someshwar Nath Temple and Ashokan Pillar is a renowned historical and spiritual destination located 28 km southwest of Motihari in East Champaran district. The site features the famous Lauriya Areraj Ashokan Pillar, a Centrally Protected single-piece polished Chunar sandstone monolithic column erected in 242 BC bearing six pillar edicts of Emperor Ashoka in pristine Brahmi script. Nearby stands the historic Baba Someshwar Nath Mahadev temple, one of north Bihar's most sacred Shiva shrines.",
        "best_time_to_visit": "October to March; Shravani Mela period",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Chirand Archaeological Site",
        "district_id": 31, # Saran
        "category": "historical",
        "latitude": 25.7125,
        "longitude": 84.8125,
        "slug": "chirand-archaeological-site-saran",
        "description": "Chirand Archaeological Site is a globally significant prehistoric mound situated on the northern bank of the Ganga near the confluence of the Ghaghara river in Saran district. Excavations have revealed it as the earliest identified Neolithic settlement in the Middle Gangetic Plain dating back to circa 2500 BC, famous for its extraordinarily rich assemblage of worked bone tools, antler implements, and terracotta figurines, with an unbroken multi-millennial habitation stratigraphy extending through Chalcolithic, Mauryan, Kushan, and Pala periods.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
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
        if pre_count != 88:
            raise RuntimeError(f"Expected 88 active places before insert, found {pre_count}")
            
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
        
        for p in batch3_data:
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
            inserted_ids.append((new_id, p['name'], p['district_id'], p['category'], p['slug']))
            print(f"  Inserted ID {new_id}: {p['name']} (District ID: {p['district_id']}, Category: {p['category']})")
        
        if len(inserted_ids) != 10:
            raise RuntimeError(f"Expected exactly 10 inserts, but got {len(inserted_ids)}")
            
        # Post-check count within transaction
        cursor.execute("SELECT COUNT(*) FROM places WHERE deleted_at IS NULL")
        post_count = cursor.fetchone()
        post_count_val = post_count['COUNT(*)'] if isinstance(post_count, dict) else post_count[0]
        print(f"Post-insert active count in transaction: {post_count_val}")
        if post_count_val != 98:
            raise RuntimeError(f"Expected 98 active places, found {post_count_val}")
            
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
