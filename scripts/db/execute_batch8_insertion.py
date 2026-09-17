import sys
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

batch8_data = [
    {
        "name": "Ara House",
        "district": "Bhojpur",
        "district_id": 16,
        "category": "historical",
        "latitude": 25.5539,
        "longitude": 84.6680,
        "slug": "ara-house-bhojpur",
        "description": "Ara House is a celebrated 1857 Indian Uprising heritage fortification situated inside the campus of Maharaja College south of Ramna Maidan in Arrah, Bhojpur district. Originally constructed by British railway engineer Richard Vicars Boyle as a two-storeyed billiard room on an elevated plinth, the building became the focal defense bastion during the famous Siege of Arrah in July 1857. A small garrison of 68 defenders held out against the revolutionary forces led by the legendary 80-year-old chieftain Babu Veer Kunwar Singh for eight days until relieved. Today, it stands as an officially protected state heritage monument featuring original defensive rifle embrasures, historical memorial plaques, and interpretive exhibits on the 1857 rebellion in central Bihar.",
        "best_time_to_visit": "October to March; 9:00 AM to 5:00 PM",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Ahilya Sthan, Ahiyari",
        "district": "Darbhanga",
        "district_id": 18,
        "category": "cultural",
        "latitude": 26.2917,
        "longitude": 85.8015,
        "slug": "ahilya-sthan-ahiyari-darbhanga",
        "description": "Ahilya Sthan is an ancient Ramayana Circuit pilgrimage sanctuary situated in Ahiyari village under Jale block of northwest Darbhanga district, approximately 3 km from Kamtaul railway station and 24 km from Darbhanga town. Celebrated in the Valmiki Ramayana and local Mithila lore, this sacred site marks the hermitage of Maharshi Gautama where his wife Devi Ahilya, cursed to stone, was restored to human form by the touch of Lord Rama's feet during his journey to King Janaka's court in Mithila. The present temple complex was constructed by the Maharajas of Darbhanga Raj and features a sanctum enshrining the sacred footprint impressions, surrounded by ancient peepal groves and sacred water tanks that host massive cultural gatherings during Ram Navami.",
        "best_time_to_visit": "October to March; Ram Navami festival",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Baba Garibnath Temple",
        "district": "Muzaffarpur",
        "district_id": 7,
        "category": "temple",
        "latitude": 26.1205,
        "longitude": 85.3912,
        "slug": "baba-garibnath-temple-muzaffarpur",
        "description": "Baba Garibnath Temple (reverently celebrated as the \"Deoghar of North Bihar\") is a renowned 300-year-old Shaivite pilgrimage destination situated in the heart of Muzaffarpur city. According to oral and temple lore, the self-manifested (Swayambhu) Shiva Lingam was discovered beneath a sacred banyan tree when a local landowner ordered it felled, oozing sacred red liquid. As the premier spiritual pilgrimage center of the Tirhut division, the temple draws over ten lakh Kanwariya pilgrims every year during the holy month of Shravan, who carry holy Ganga water on foot from Pahleza Ghat on the Ganges in Saran to perform Jalabhishek. The site is actively being enhanced under a comprehensive multi-crore pilgrimage corridor redevelopment project by Bihar Tourism (BSTDC).",
        "best_time_to_visit": "October to March; Shravan month and Mahashivratri",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Surya Mandir, Kandaha",
        "district": "Saharsa",
        "district_id": 29,
        "category": "historical",
        "latitude": 25.8820,
        "longitude": 86.4670,
        "slug": "surya-mandir-kandaha-saharsa",
        "description": "Surya Mandir at Kandaha is an extraordinary medieval Sun temple and archaeological monument situated in Pastwar Panchayat (Kandaha village) of Mahishi block in western Saharsa district, about 16 km west of the district headquarters. The sanctum houses a masterpiece of medieval sculptural art: a life-sized idol of the Sun God (Lord Surya) intricately carved from a single monolithic slab of lustrous black chlorite/granite, depicting him riding a chariot drawn by seven horses driven by Aruna. The temple's doorframe bears a priceless 14th-century Sanskrit epigraph dating to the reign of King Narasimha Deva of the Oinwar (Kameshwar) dynasty, verified by the Archaeological Survey of India (ASI) as an invaluable epigraphical record of Mithila's medieval history.",
        "best_time_to_visit": "October to March; Chhath Puja and daytime exploration (9:00 AM to 5:00 PM)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Mata Puran Devi Temple",
        "district": "Purnia",
        "district_id": 28,
        "category": "cultural",
        "latitude": 25.7725,
        "longitude": 87.4580,
        "slug": "mata-puran-devi-temple-purnia",
        "description": "Mata Puran Devi Temple is the ancient titular Shakti shrine situated in the Purnea City area of Purnia district, approximately 5 km east of the modern town center. Widely documented in British gazetteers and regional heritage chronicles, this revered temple is universally acknowledged as the eponym from which the historic district and city of Purnia (\"Purna-Aranya\" or forest of Puran Devi) derives its name. Devotees revere the presiding goddess as an incarnation of Adi Shakti, offering prayers to ancient stone pindis that have been continuously worshipped across centuries. Supported by Bihar Tourism infrastructure development, the temple complex features ceremonial courtyards and pilgrim amenities that host grand congregations during Chaitra and Sharadiya Navratri.",
        "best_time_to_visit": "October to March; Navratri festivals",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Baba Brahmeshwar Nath Temple, Brahmpur",
        "district": "Buxar",
        "district_id": 17,
        "category": "temple",
        "latitude": 25.5992,
        "longitude": 84.2882,
        "slug": "baba-brahmeshwar-nath-temple-brahmpur-buxar",
        "description": "Baba Brahmeshwar Nath Temple (popularly celebrated as \"Mini Kashi\" of the Shahabad region) is a historic Shaivite pilgrimage destination located in Brahmpur town in eastern Buxar district, near the NH-922 highway. The ancient temple enshrines a Swayambhu (self-manifested) Shiva Lingam within a sanctum uniquely facing west rather than east. According to regional lore, the entrance miraculously rotated westward when foreign invaders challenged the divine power of the deity. The temple complex is surrounded by a sacred water pond and serves as the epicenter of one of the largest and oldest traditional cattle and agricultural fairs in northern India, organized annually during Mahashivratri and Phalguna, drawing pilgrims and traders from across Bihar and Uttar Pradesh.",
        "best_time_to_visit": "October to March; Mahashivratri and Phalguna Mela",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Gunawa Ji (Jain Tirth)",
        "district": "Nawada",
        "district_id": 38,
        "category": "cultural",
        "latitude": 24.8944,
        "longitude": 85.5312,
        "slug": "gunawa-ji-jain-tirth-nawada",
        "description": "Gunawa Ji (also known as Gonawan Tirth or Gunawa Jal Mandir) is an internationally revered Jain pilgrimage center situated 3 km south of Nawada town along the Patna-Ranchi Highway (NH-31). The prime attraction of the peaceful complex is an exquisite white-marble Jal Mandir standing gracefully in the center of an expansive, lotus-filled lake, reminiscent of the renowned Jal Mandir at Pawapuri. Accessible via an arched causeway, the sanctum marks the sacred spot where Indrabhuti Gautama Swami, the foremost Ganadhara (chief disciple) of Bhagwan Mahavira, achieved supreme omniscience (Kevala Jnana) following Mahavira's Nirvana. The complex includes extensive pilgrim dharamsalas, lush gardens, and meditation halls welcoming Jain devotees from across the globe.",
        "best_time_to_visit": "October to March; 6:00 AM to 6:00 PM",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Ambika Sthan, Aami",
        "district": "Saran",
        "district_id": 31,
        "category": "cultural",
        "latitude": 25.6881,
        "longitude": 85.0062,
        "slug": "ambika-sthan-aami-saran",
        "description": "Ambika Sthan is an ancient Shaktipeeth sanctuary perched on a high archaeological fort-mound overlooking the northern floodplains of the Ganges in Aami village of Dighwara block, Saran district, situated along the Patna-Chhapra highway. Immersed in Puranic mythology, local belief identifies this elevated mound as the site of King Daksha Prajapati's cosmic Yajna, where Sati immolated herself and where the torso of the Goddess fell. The inner sanctum features a sacred clay pindi of Maa Ambika Bhawani enclosed within an antique brick and stone fort-like structure that has survived multiple Ganges flood epochs. Devotees flock here for Navratri rituals, taking holy dips at the adjacent ghat and seeking blessings at the ancient Yajna Kunda.",
        "best_time_to_visit": "October to March; Chaitra and Sharadiya Navratri",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Lakri Dargah",
        "district": "Gopalganj",
        "district_id": 19,
        "category": "cultural",
        "latitude": 26.3150,
        "longitude": 84.4720,
        "slug": "lakri-dargah-gopalganj",
        "description": "Lakri Dargah is a renowned 16th-century Sufi pilgrimage shrine and architectural landmark situated in Gopalganj district, approximately 25 km south of the district headquarters. The holy complex encloses the historic tomb and chilla of the venerated Muslim mystic Shah Arzan, who hailed from Patna and underwent 40 days of continuous spiritual austerity (Chilla) in the tranquil regional forests. Deeply impressed by the saint's piety, Mughal Emperor Aurangzeb endowed the shrine with extensive royal land grants and revenues. The dargah is famed for its antique woodwork, exquisitely carved timber doorways, and lattice screens. The annual Urs fair celebrated on the 11th of Rabi-ul-Awwal attracts tens of thousands of devotees across all communities in a vibrant display of communal harmony.",
        "best_time_to_visit": "October to March; Annual Urs festival",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Baba Tileshwar Nath Mandir, Sukhpur",
        "district": "Supaul",
        "district_id": 36,
        "category": "temple",
        "latitude": 26.0620,
        "longitude": 86.6080,
        "slug": "baba-tileshwar-nath-mandir-sukhpur-supaul",
        "description": "Baba Tileshwar Nath Mandir (also revered as Tileshwar Sthan) is an ancient, highly venerated Shaivite pilgrimage destination situated in Sukhpur Solhani village under the Supaul block, about 10 km south of Supaul district headquarters. The sanctum enshrines an ancient self-manifested (Swayambhu) Shiva Lingam that has served as the spiritual guardian of the lower Kosi river basin across generations. Officially listed by the Supaul District Administration alongside the Kosi Barrage as one of the district's premier heritage attractions, the temple complex features a serene sacred pond, ceremonial pavilion halls, and expansive grounds that draw tens of thousands of devotees during Mahashivratri and the holy Mondays of Shravan.",
        "best_time_to_visit": "October to March; Shravan month and Mahashivratri",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    }
]

def main():
    print("=" * 80)
    print("EXECUTING ATOMIC INSERTION FOR BATCH 8 (10 CANDIDATES)")
    print("=" * 80)
    
    conn = get_db()
    conn.autocommit = False
    cursor = conn.cursor()
    
    try:
        # 1. Pre-check baseline within transaction
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_count = row['cnt'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert active count: {pre_count} (Must be 138)")
        if pre_count != 138:
            raise RuntimeError(f"ABORT: Expected 138 active places before insert, found {pre_count}")
            
        cursor.execute("SELECT MAX(id) as max_id FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_max_id = row['max_id'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert max ID: {pre_max_id} (Expected: 188)")
        if pre_max_id != 188:
            raise RuntimeError(f"ABORT: Expected max ID 188, found {pre_max_id}")

        # Verify live districts
        for p in batch8_data:
            cursor.execute("SELECT id, name FROM districts WHERE name = %s", (p['district'],))
            drow = cursor.fetchone()
            if not drow or drow['id'] != p['district_id']:
                raise RuntimeError(f"District verification failed for {p['district']}: expected {p['district_id']}, found {drow}")
        print("Live districts table verification: ALL 10 MATCH.")

        inserted_records = []
        
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
        
        for p in batch8_data:
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
            inserted_records.append({
                "id": new_id,
                "name": p['name'],
                "district_id": p['district_id'],
                "district": p['district'],
                "category": p['category'],
                "slug": p['slug'],
                "lat": p['latitude'],
                "lng": p['longitude']
            })
            print(f"  [+] Inserted ID {new_id}: {p['name']} ({p['district']}, Cat: {p['category']}) -> {p['slug']}")
        
        if len(inserted_records) != 10:
            raise RuntimeError(f"ABORT: Expected exactly 10 inserts, but got {len(inserted_records)}")
            
        # Post-check count within transaction
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        post_count = row['cnt'] if isinstance(row, dict) else row[0]
        print(f"\nPost-insert active count in transaction: {post_count}")
        if post_count != 148:
            raise RuntimeError(f"ABORT: Expected 148 active places, found {post_count}")

        cursor.execute("SELECT MAX(id) as max_id FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        post_max_id = row['max_id'] if isinstance(row, dict) else row[0]
        print(f"Post-insert max ID in transaction: {post_max_id}")
        if post_max_id != 198:
            raise RuntimeError(f"ABORT: Expected max ID 198, found {post_max_id}")

        cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        post_dist_count = row['cnt'] if isinstance(row, dict) else row[0]
        print(f"Districts covered in transaction: {post_dist_count}/38")
        if post_dist_count != 38:
            raise RuntimeError(f"ABORT: Expected 38 districts covered, found {post_dist_count}")
            
        # All 10 succeeded -> COMMIT!
        conn.commit()
        print("\n" + "=" * 80)
        print("TRANSACTION COMMITTED SUCCESSFULLY! All 10 places inserted atomically.")
        print("Inserted IDs:", [x['id'] for x in inserted_records])
        print("=" * 80)
        
    except Exception as e:
        conn.rollback()
        print(f"\nFATAL ERROR: Insertion failed, TRANSACTION ROLLED BACK! Error: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
