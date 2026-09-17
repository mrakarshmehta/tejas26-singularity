import sys
import os
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

batch6_data = [
    {
        "name": "Kahalgaon Rock-Cut Temples",
        "district": "Bhagalpur",
        "district_id": 5,
        "category": "historical",
        "latitude": 25.2689,
        "longitude": 87.2345,
        "slug": "kahalgaon-rock-cut-temples-bhagalpur",
        "description": "Kahalgaon Rock-Cut Temples (historically documented as the Colgong Rock Temple) is an extraordinary Centrally Protected monument of the Archaeological Survey of India (ASI Patna Circle) situated on monolithic granite boulder islands rising directly within the mainstream of the River Ganga at Kahalgaon in Bhagalpur district. Dating back to the 7th–8th century Gupta-Pala transition period and recorded by Chinese pilgrim Hiuen Tsang, these rare riverine monolithic shrines feature exquisitely sculpted rock reliefs and cave chambers combining Shaivite, Vaishnavite, Buddhist, and Jain iconographic traditions, making it one of eastern India's most exceptional water-surrounded rock heritage marvels.",
        "best_time_to_visit": "October to March (dry winter months when river water recedes for optimal boulder access)",
        "entry_fee": "Free (local boat ferry charges apply)",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Vishwa Shanti Stupa & Ratnagiri Ropeway",
        "district": "Nalanda",
        "district_id": 3,
        "category": "cultural",
        "latitude": 25.0085,
        "longitude": 85.4385,
        "slug": "vishwa-shanti-stupa-and-ratnagiri-ropeway-nalanda",
        "description": "Vishwa Shanti Stupa (World Peace Pagoda) & Ratnagiri Ropeway is an internationally celebrated Buddhist pilgrimage landmark crowning the 1,000-foot summit of Ratnagiri Hill in Rajgir, Nalanda district. Consecrated in 1969 by venerable Nichidatsu Fujii (Fujii Guruji) on the 2,500th anniversary of Lord Buddha, the magnificent 125-foot white marble pagoda features four monumental gilded statues depicting Buddha's birth, enlightenment, first sermon, and mahaparinirvana. Visitors ascend to the summit via Bihar's premier aerial chairlift ropeway operated by the Bihar State Tourism Development Corporation (BSTDC), taking in breathtaking panoramic vistas of the ancient Rajgir valley and hills.",
        "best_time_to_visit": "October to March; morning and late afternoon",
        "entry_fee": "Stupa entry free; BSTDC Ropeway ticket ~Rs. 100-150 round-trip",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Shringirishi Dham",
        "district": "Lakhisarai",
        "district_id": 26,
        "category": "nature",
        "latitude": 25.1278,
        "longitude": 86.2344,
        "slug": "shringirishi-dham-lakhisarai",
        "description": "Shringirishi Dham is an enchanting eco-tourism, spiritual, and nature destination nestled in a forested mountain gorge of the Kharagpur hills in Suryagarha block of Lakhisarai district. Deeply revered in Ramayana traditions as the hermitage of Sage Shringi, who performed the Putrakameshti Yajna for King Dasharatha resulting in the birth of Lord Rama, the site features perennial mountain waterfalls, the sacred natural hot sulfur water spring 'Sita Kund', and the scenic Shringi Rishi Dam irrigation reservoir, creating a serene sanctuary of natural beauty, medicinal waters, and ancient cultural heritage.",
        "best_time_to_visit": "October to March; Makar Sankranti and Shravan",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Girihinda Pahar & Shiv Temple",
        "district": "Sheikhpura",
        "district_id": 32,
        "category": "mountain",
        "latitude": 25.1385,
        "longitude": 85.8562,
        "slug": "girihinda-pahar-and-shiv-temple-sheikhpura",
        "description": "Girihinda Pahar & Shiv Temple is a dramatic 500-foot rocky granite inselberg rising abruptly above the alluvial plains in Sheikhpura town, serving as the district's premier scenic and religious landmark. Offering commanding 360-degree panoramic vistas across the entire district landscape, the hilltop is reached via stone stairways and a paved winding road developed with a landscaped children's park (Bal Udyan). The summit houses the ancient Baba Kameshwar Nath Shiva Temple, celebrated in local Mahabharata traditions as the historic abode of demoness Hidimba and the site of her sacred marriage to Pandava prince Bhima.",
        "best_time_to_visit": "October to March; sunset and sunrise hours",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Matsyagandha Lake & Raktakali Temple",
        "district": "Saharsa",
        "district_id": 29,
        "category": "lake",
        "latitude": 25.8825,
        "longitude": 86.5985,
        "slug": "matsyagandha-lake-and-raktakali-temple-saharsa",
        "description": "Matsyagandha Lake & Raktakali Temple is a vibrant 80-acre urban freshwater lake and cultural complex situated in Saharsa town. Rejuvenated into a prime eco-tourism and recreation hub under Bihar's Jal-Jeevan-Hariyali mission, the lake features pedal boating, walking promenades, and landscaped gardens. The complex is distinguished by the unique Raktakali Temple, built in a rare oval architectural design dedicated to the 64 Yoginis (Chausath Yogini) with finely engraved stone wall deities representing Shakta and Tantric artistic traditions, attracting thousands during Diwali and Chhath.",
        "best_time_to_visit": "October to March; evening boating hours",
        "entry_fee": "Free (boating charges separate ~Rs. 50)",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Kajha Kothi Eco Park",
        "district": "Purnia",
        "district_id": 28,
        "category": "nature",
        "latitude": 25.7185,
        "longitude": 87.3512,
        "slug": "kajha-kothi-eco-park-purnia",
        "description": "Kajha Kothi Eco Park (also known as Shastri Park) is a historic colonial-era plantation estate and eco-tourism park situated on the banks of the serene Kajri river in Krityanand Nagar block of Purnia district. Established around 1775 as a British indigo circuit house ('Neel Kothi') that once hosted Lord Mountbatten and Indira Gandhi, the estate was named in honour of former Bihar Chief Minister Bhola Paswan Shastri. Rejuvenated by the Bihar Forest Department, the park features an expansive freshwater lake with pedal boating, shaded woodland walking trails, birdwatching viewpoints, and family picnic grounds.",
        "best_time_to_visit": "October to March; afternoon and winter weekends",
        "entry_fee": "Nominal park entry fee (~Rs. 10-20)",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Guru Tegh Bahadur Historic Gurdwara, Lakshmipur",
        "district": "Katihar",
        "district_id": 23,
        "category": "cultural",
        "latitude": 25.3912,
        "longitude": 87.2812,
        "slug": "guru-tegh-bahadur-historic-gurdwara-lakshmipur-katihar",
        "description": "Sri Guru Tegh Bahadur Historic Gurdwara at Lakshmipur (historically known as Kantanagar) is a revered spiritual destination on the official Sikh Circuit promoted by Bihar Tourism, located in Barari block of Katihar district. The Gurdwara commemorates the historic 1670 AD visit of the ninth Sikh Guru, Sri Guru Tegh Bahadur Ji, while journeying from Assam back to Patna. The sacred shrine reverently preserves rare 17th-century historical artifacts, including authentic royal Hukumnamas (edicts) bearing the Guru's seal and an ancient handwritten copy of the sacred Guru Granth Sahib, serving as a beacon of interfaith harmony and Sikh heritage in eastern Bihar.",
        "best_time_to_visit": "Throughout the year; Gurpurab celebrations in winter",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Dighwa Dubauli Archaeological Mounds",
        "district": "Gopalganj",
        "district_id": 19,
        "category": "historical",
        "latitude": 26.2485,
        "longitude": 84.7312,
        "slug": "dighwa-dubauli-archaeological-mounds-gopalganj",
        "description": "Dighwa Dubauli Archaeological Mounds is a monumental pre-medieval earthwork and archaeological heritage site located in Baikunthpur block of Gopalganj district. The site is distinguished by two extraordinary pyramidal earthen mounds with bases projecting outward into a distinct four-pointed star pattern topped by a conical summit, traditionally attributed to the ancient Chero dynasties. The site gained international epigraphic fame following the discovery of the 761–762 AD Dighwa-Dubauli copper plate inscription issued by Gurjara-Pratihara emperor Mahendrapala I, confirming the strategic and cultural antiquity of northwestern Bihar.",
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Champanagar Ancient Capital & Jain Tirth",
        "district": "Bhagalpur",
        "district_id": 5,
        "category": "cultural",
        "latitude": 25.2312,
        "longitude": 86.9245,
        "slug": "champanagar-ancient-capital-and-jain-tirth-bhagalpur",
        "description": "Champanagar Ancient Capital & Jain Tirth is an illustrious historical, epic, and sacred pilgrimage center located in Nathnagar on the western periphery of Bhagalpur city. Historically documented as Champa, the fortified capital of ancient Anga Mahajanapada immortalized in the Mahabharata as the domain of King Karna (preserved in the towering earthen ramparts of Karna Garh), the site is globally revered in Jainism as the holy Panch Kalyanaka Kshetra of Bhagwan Vasupujya, the 12th Tirthankara, who was born, renounced the world, and attained omniscience and Nirvana here. Excavations have unearthed fortified mud ramparts, ancient brickwork, and rich Northern Black Polished Ware (NBPW) artifacts.",
        "best_time_to_visit": "October to March; Mahavira Jayanti and Paryushana",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Deokund",
        "district": "Aurangabad",
        "district_id": 13,
        "category": "temple",
        "latitude": 24.9512,
        "longitude": 84.5829,
        "slug": "deokund-aurangabad",
        "description": "Deokund is a venerated ancient Shaivite pilgrimage sanctuary and perennial spring located in Goh block of northeastern Aurangabad district near the Arwal border. Centered around the ancient Baba Dudheshwar Nath Shiva temple housing a revered east-facing lingam, the site features a sacred perennial pond (kund) traditionally believed to have been established during the Treta Yuga as the hermitage of Sage Chyavana (author of the Ayurvedic Chyawanprash tradition). Organized under the patronage of the district administration, the site draws over 100,000 devotees during the grand annual Mahashivratri and Shravani melas.",
        "best_time_to_visit": "October to March; Mahashivratri and Shravan months",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    }
]

def main():
    print("================================================================================")
    print("EXECUTING BATCH 6 ATOMIC TRANSACTION INSERTION")
    print("================================================================================")
    
    conn = get_db()
    conn.autocommit = False
    cursor = conn.cursor()
    
    try:
        # Pre-check baseline
        cursor.execute("SELECT COUNT(*) FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_count = row['COUNT(*)'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert active count: {pre_count}")
        if pre_count != 118:
            raise RuntimeError(f"ABORT: Expected 118 active places before insert, found {pre_count}")
            
        cursor.execute("SELECT MAX(id) FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_max_id = row['MAX(id)'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert max ID: {pre_max_id} (Expected: 168)")
        if pre_max_id != 168:
            raise RuntimeError(f"ABORT: Expected max ID 168, found {pre_max_id}")

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
        
        for p in batch6_data:
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
        cursor.execute("SELECT COUNT(*) FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        post_count = row['COUNT(*)'] if isinstance(row, dict) else row[0]
        print(f"\nPost-insert active count in transaction: {post_count}")
        if post_count != 128:
            raise RuntimeError(f"ABORT: Expected 128 active places, found {post_count}")

        cursor.execute("SELECT COUNT(DISTINCT district_id) FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        post_dist_count = row['COUNT(DISTINCT district_id)'] if isinstance(row, dict) else row[0]
        print(f"Districts covered in transaction: {post_dist_count}/38")
        if post_dist_count != 38:
            raise RuntimeError(f"ABORT: Expected 38 districts covered, found {post_dist_count}")
            
        # All 10 succeeded -> COMMIT!
        conn.commit()
        print("\n" + "="*80)
        print("TRANSACTION COMMITTED SUCCESSFULLY! All 10 places inserted atomically.")
        print("Inserted IDs:", [x['id'] for x in inserted_records])
        print("="*80)
        
    except Exception as e:
        conn.rollback()
        print(f"\nFATAL ERROR: Insertion failed, TRANSACTION ROLLED BACK! Error: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
