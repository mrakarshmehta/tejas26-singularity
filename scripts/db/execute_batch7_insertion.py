import sys
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

batch7_data = [
    {
        "name": "Bhitiharwa Gandhi Ashram",
        "district": "West Champaran",
        "district_id": 9,
        "category": "historical",
        "latitude": 27.2437,
        "longitude": 84.4838,
        "slug": "bhitiharwa-gandhi-ashram-west-champaran",
        "description": "Bhitiharwa Gandhi Ashram is a revered national freedom heritage monument situated in Gaunaha block of West Champaran district, serving as the operational epicenter of Mahatma Gandhi's historic 1917 Champaran Satyagraha. Established on 20 November 1917, the ashram housed the nation's first basic school (Kasturba Gandhi Vidyalaya) where Bapu and Kasturba Gandhi pioneered community education, sanitation, and civil resistance against oppressive indigo plantation exploitation. Today, the tranquil complex preserves the original mud-walled and thatched residential hut, the historical school bell rung by Gandhiji to gather villagers, a sacred prayer ground, and a comprehensive museum exhibiting authentic spinning charkhas, original correspondence, hand-spun khadi garments, and rare photographic archives of India's freedom struggle.",
        "best_time_to_visit": "October to March; 9:00 AM to 5:00 PM",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Baba Mahendra Nath Temple, Mehdar",
        "district": "Siwan",
        "district_id": 35,
        "category": "temple",
        "latitude": 25.9870,
        "longitude": 84.4380,
        "slug": "baba-mahendra-nath-temple-mehdar-siwan",
        "description": "Baba Mahendra Nath Temple (popularly celebrated as Mehdar Dham) is a monumental 17th-century Shaivite pilgrimage destination situated in Siswan block of southeastern Siwan district, approximately 32 km from the district headquarters. Constructed by King Mahendra Bir Bikram Shah of Nepal after being miraculously cured of chronic leprosy upon bathing in the sacred forest pond, the temple is set along the expansive 55-acre Kamaldah Sarovar (Kamaldah Lake), famous for sacred blooming water lilies and therapeutic mineral waters. The temple complex enshrines a revered self-manifested (Swayambhu) Shiva Lingam within an imposing multi-tiered tower adorned with intricate stucco carvings, drawing over 200,000 pilgrims during the annual state-sponsored Mehdar Mahotsav, Mahashivratri, and the holy month of Shravan.",
        "best_time_to_visit": "October to March; Shravan month and Mahashivratri",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Jaimangla Garh",
        "district": "Begusarai",
        "district_id": 15,
        "category": "historical",
        "latitude": 25.5921,
        "longitude": 86.1613,
        "slug": "jaimangla-garh-begusarai",
        "description": "Jaimangla Garh is an ancient fortified island promontory and Shaktipeeth sanctuary situated on the southern fringe of Kabartal (Kanwar Lake) in Manjhaul subdivision of Begusarai district. Dating back to the pre-medieval Pala dynasty and documented in regional archaeological surveys, the elevated mound reveals ancient brick fortifications, defensive moats, and antiquities excavated by the State Archaeology Directorate and the Archaeological Survey of India. The complex houses the sacred 9th–10th century temple of Goddess Chandi Mangla Devi, where the presiding deity is carved from a rare monolithic block of lustrous black basalt stone, surrounded by ancient stone votive stupas and Pala-era sculptural reliefs that draw thousands of pilgrims during Navratri and the annual Chandi Mela.",
        "best_time_to_visit": "October to March; Navratri festival",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Ramrekha Ghat",
        "district": "Buxar",
        "district_id": 17,
        "category": "cultural",
        "latitude": 25.5761,
        "longitude": 83.9711,
        "slug": "ramrekha-ghat-buxar",
        "description": "Ramrekha Ghat is the prime sacred Ganga riverfront pilgrimage destination of Buxar, celebrated in Valmiki Ramayana traditions as the holy river crossing where Lord Rama and Lakshmana crossed the Ganges under the guidance of Sage Vishwamitra after slaying the demoness Tadaka. The site features the ancient Rameshwarnath Shiva Temple housing a clay-fashioned Shivling that bears the legendary handprint of Lord Rama, along with sacred foot imprints (Charan Paduka). Following a comprehensive Rs. 13.24-crore riverfront development by Bihar Tourism, the ghat boasts expansive paved promenades, illuminated pavilions, and seating steps where thousands gather for the nightly grand Maha Aarti ceremonies and the massive annual Panchkosi Parikrama and Makar Sankranti fairs.",
        "best_time_to_visit": "October to March; evening Aarti hours (5:30 PM - 7:00 PM)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Aganoor Mini Hydroelectric Project",
        "district": "Arwal",
        "district_id": 12,
        "category": "tourist_spot",
        "latitude": 25.1328,
        "longitude": 84.5385,
        "slug": "aganoor-mini-hydroelectric-project-arwal",
        "description": "Aganoor Mini Hydroelectric Project (Aganoor Jal Vidyut Pariyojna) is a scenic eco-engineering and leisure destination situated in Kaler block of southern Arwal district along the Sone River canal network. Built as a sustainable run-of-the-river hydroelectric generation facility by the Bihar State Hydroelectric Power Corporation (BSHPC), the installation features an engineered canal barrage, surging spillway gates, and dynamic cascading canal waterfalls surrounded by lush greenery and tree-lined embankment bunds. Officially recognized by the Arwal District Administration as a prime regional picnic spot and recreational gateway, the site draws visitors for family outings, monsoon landscape photography, and serene riverine canal sunsets.",
        "best_time_to_visit": "October to March; monsoon season (July to September) for high water flows",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Raja Bali Ka Garh",
        "district": "Madhubani",
        "district_id": 20,
        "category": "historical",
        "latitude": 26.4595,
        "longitude": 86.3230,
        "slug": "raja-bali-ka-garh-madhubani",
        "description": "Raja Bali Ka Garh (officially Balirajgarh) is a monumental Centrally Protected monument of National Importance under the Archaeological Survey of India (ASI Patna Circle, declared in 1938), situated in Babubarhi block of northeastern Madhubani district. Sprawling across 176 acres, the ancient fortified urban settlement is enclosed by massive kiln-burnt brick and earthen ramparts rising up to 40 feet above the surrounding plains. Excavations by the ASI have revealed five continuous cultural epochs spanning the Northern Black Polished Ware (NBPW), Sunga, Kushan, Gupta, and Pala periods, yielding exquisite Sunga terracotta figurines, inscribed sealings, punch-marked silver coins, and pre-Christian urban drainage works, identifying it as an ancient political capital of the Videha Kingdom.",
        "best_time_to_visit": "October to March; daytime exploration (9:00 AM to 5:00 PM)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Dr. Rajendra Prasad Central Agricultural University",
        "district": "Samastipur",
        "district_id": 30,
        "category": "historical",
        "latitude": 25.9860,
        "longitude": 85.6754,
        "slug": "dr-rajendra-prasad-central-agricultural-university-samastipur",
        "description": "Dr. Rajendra Prasad Central Agricultural University (DRPCAU, historically the Imperial Agricultural Research Institute at Pusa) is an institution of national importance and the historic birthplace of modern agricultural science in India, located in Pusa block of Samastipur district along the Burhi Gandak river. Established in 1905 by British Viceroy Lord Curzon with a landmark philanthropic donation from American philanthropist Henry Phipps, the sprawling heritage campus showcases magnificent Edwardian colonial architecture, the historic Phipps Laboratory ruins, the heritage Curzon Ground, and expansive botanical gardens with exotic flora. The campus museum preserves antique 20th-century agronomic laboratory equipment, rare historical archives, and photographic records of early Indian scientific history.",
        "best_time_to_visit": "October to March; campus visiting hours (10:00 AM to 5:00 PM)",
        "entry_fee": "Free (visitor pass registration at main gate)",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    },
    {
        "name": "Baba Vishu Raut Temple, Pachrasi Dham",
        "district": "Madhepura",
        "district_id": 27,
        "category": "cultural",
        "latitude": 25.4450,
        "longitude": 87.0250,
        "slug": "baba-vishu-raut-temple-pachrasi-dham-madhepura",
        "description": "Baba Vishu Raut Temple (Pachrasi Dham) is an extraordinary 300-year-old pastoral folk shrine and cultural pilgrimage destination located at Pachrasi in Chausa block of southern Madhepura district. Dedicated to the legendary 18th-century cowherd folk hero Baba Vishu Raut, who laid down his life protecting village cattle herds from predatory Royal Bengal tigers, the shrine is the site of a profound living ritual where hundreds of thousands of dairy farmers and pastoralists from Bihar, Bengal, and Nepal converge to pour countless liters of raw cow milk over his samadhi in a perpetual white torrent. The site hosts an annual official 4-day state-recognized Rajkiya Mela every April (Chaitra Sankranti), featuring traditional rural wrestling (dangal), folk theatrical plays, and vibrant regional fairs.",
        "best_time_to_visit": "October to April; especially during Chaitra Sankranti Rajkiya Mela (mid-April)",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Kanhaiya Ji Mandir, Bandarjhula",
        "district": "Kishanganj",
        "district_id": 25,
        "category": "historical",
        "latitude": 26.3683,
        "longitude": 87.9636,
        "slug": "kanhaiya-ji-mandir-bandarjhula-kishanganj",
        "description": "Kanhaiya Ji Mandir at Bandarjhula is a Centrally Protected monument of National Importance under the Archaeological Survey of India (ASI Patna Circle), situated in Thakurganj block of northern Kishanganj district near the Indo-Nepal international border. Located atop ancient archaeological mounds that were once part of pre-medieval trans-Himalayan trade routes, the site preserves a magnificent 8th–9th century monolithic black basalt stone idol of Lord Vishnu (locally revered as Kanhaiya Ji), standing over four feet tall and carved with intricate iconography of the four attributes (Sankha, Chakra, Gada, Padma). The archaeological complex includes ancient kiln-fired brick foundation plinths, carved architectural doorframes, and elevated earthen mounds that highlight the ancient sculptural heritage of the Seemanchal borderland.",
        "best_time_to_visit": "October to March; daytime visits recommended",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 1,
        "best_season": "winter"
    },
    {
        "name": "Gautam Asthan, Revelganj",
        "district": "Saran",
        "district_id": 31,
        "category": "cultural",
        "latitude": 25.7812,
        "longitude": 84.6712,
        "slug": "gautam-asthan-revelganj-saran",
        "description": "Gautam Asthan is a venerated ancient hermitage and pilgrimage destination situated on the high bluffs of the holy Saryu (Ghaghara) River at Revelganj in Saran district, approximately 8 km west of Chhapra. Celebrated in the Valmiki Ramayana, Puranas, and local folklore as the Vedic hermitage of Sage Maharshi Gautama, the site is revered as the sacred 'Ahilya Uddhar Sthal', where Goddess Ahilya was redeemed from her curse of petrification upon being touched by the dust of Lord Rama's feet. An official destination on Bihar Tourism's Ramayana Circuit, the site features the historic Gautam Rishi Temple, ancient river bathing ghats, and parikrama halls, drawing immense congregations of devotees during Kartik Purnima and Ram Navami for sacred dips and religious fairs.",
        "best_time_to_visit": "October to March; Kartik Purnima and Ram Navami",
        "entry_fee": "Free",
        "family_friendly": 1,
        "is_hidden_gem": 0,
        "best_season": "winter"
    }
]

def main():
    print("=" * 80)
    print("EXECUTING BATCH 7 ATOMIC TRANSACTION INSERTION")
    print("=" * 80)
    
    conn = get_db()
    conn.autocommit = False
    cursor = conn.cursor()
    
    try:
        # 1. Pre-check baseline
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_count = row['cnt'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert active count: {pre_count} (Must be 128)")
        if pre_count != 128:
            raise RuntimeError(f"ABORT: Expected 128 active places before insert, found {pre_count}")
            
        cursor.execute("SELECT MAX(id) as max_id FROM places WHERE deleted_at IS NULL")
        row = cursor.fetchone()
        pre_max_id = row['max_id'] if isinstance(row, dict) else row[0]
        print(f"Pre-insert max ID: {pre_max_id} (Expected: 178)")
        if pre_max_id != 178:
            raise RuntimeError(f"ABORT: Expected max ID 178, found {pre_max_id}")

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
        
        for p in batch7_data:
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
        if post_count != 138:
            raise RuntimeError(f"ABORT: Expected 138 active places, found {post_count}")

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
