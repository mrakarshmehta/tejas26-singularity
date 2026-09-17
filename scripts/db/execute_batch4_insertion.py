import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_db

batch4_data = [
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

def main():
    conn = get_db()
    conn.autocommit = False
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_count = row['COUNT(*)'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert active count: {pre_count}")
        if pre_count != 98:
            raise RuntimeError(f"Expected 98 active places before insert, found {pre_count}")
            
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
        
        for p in batch4_data:
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
        if post_count_val != 108:
            raise RuntimeError(f"Expected 108 active places, found {post_count_val}")
            
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
