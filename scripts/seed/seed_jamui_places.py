"""
Seed script to add verified tourist places for Jamui district
into the existing HiddenYatra database.

Uses existing Place model schema. Only inserts if slug does not already exist.
Sources: Official Jamui District website (jamui.nic.in), Bihar Tourism, Wikipedia.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.connection import get_cursor

JAMUI_DISTRICT_ID = 22
STATE_ID = 1  # Bihar

PLACES = [
    # ──────────────────────────────────────────────
    # 1. Giddheswar Temple
    # ──────────────────────────────────────────────
    {
        "name": "Giddheswar Temple",
        "slug": "giddheswar-temple-jamui",
        "category": "temple",
        "description": (
            "Giddheswar Temple is a revered Shiva temple perched atop massive stone boulders in the "
            "Khaira block of Jamui district, approximately 15 km south of the district headquarters. "
            "According to Ramayana legend, this is the spot where the mythical vulture king Jatayu fell "
            "after his fierce battle with Ravana while attempting to rescue Goddess Sita. The name "
            "'Giddheswar' derives from 'Giddh' (vulture). The modern temple was built around 1941 by "
            "Lala Harinandan Prasad, a Tehsildar under the Maharaja of Gidhaur, who discovered a "
            "Shivling near the mountain and was divinely inspired to construct the shrine. The temple "
            "complex offers serene hill views and is a major pilgrimage site where devotees offer the "
            "first harvest of their crops."
        ),
        "latitude": 24.8350,
        "longitude": 86.2200,
        "best_time_to_visit": "October to March (Winter)",
        "entry_fee": "Free",
        "history": (
            "According to Ramayana legend, this is the sacred spot where the mythical vulture king "
            "Jatayu fell after battling Ravana while trying to rescue Goddess Sita from abduction. "
            "The modern temple structure was built around 1941 by Lala Harinandan Prasad, who served "
            "as a Tehsildar under the Maharaja of Gidhaur. While returning from his duties, he "
            "discovered a Shivling near the Giddheswar mountain. Following a divine dream instructing "
            "him to build a temple at the site, he oversaw its construction."
        ),
        "travel_tips": (
            "Wear comfortable shoes as the temple is situated on rocky terrain atop stone boulders. "
            "Carry water during summer months. The trek to the temple offers panoramic views of the "
            "surrounding hills and forests."
        ),
        "best_season": "Winter",
        "best_time_of_day": "Morning",
        "crowd_level": "Moderate",
        "nearest_railway": "Jamui Railway Station (15 km)",
        "nearest_bus_stand": "Jamui Bus Stand (15 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (200 km)",
        "is_featured": 1,
        "is_hidden_gem": 0,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 2. Patneshwar Mandir
    # ──────────────────────────────────────────────
    {
        "name": "Patneshwar Mandir",
        "slug": "patneshwar-mandir-jamui",
        "category": "temple",
        "description": (
            "Patneshwar Mandir (Patneshwar Dham) is a significant Shiva temple located approximately "
            "5 km north of Jamui district headquarters in the Mallehpur area along Station Road. "
            "Situated on the Patneshwar Hill near the banks of the Kiul River, this ancient shrine "
            "is one of the most visited religious sites in Jamui. The temple attracts large numbers "
            "of devotees during Maha Shivaratri and Shravan month. The serene hilltop setting "
            "provides a tranquil atmosphere for worship and meditation."
        ),
        "latitude": 24.9636,
        "longitude": 86.2397,
        "best_time_to_visit": "October to March, Maha Shivaratri",
        "entry_fee": "Free",
        "history": (
            "Patneshwar Mandir is an ancient Shiva temple believed to have been a site of worship "
            "for centuries. Located on Patneshwar Hill near the Kiul River, the temple has been a "
            "major spiritual center for the region. During Shravan month and Maha Shivaratri, "
            "thousands of devotees visit to offer prayers and perform rituals."
        ),
        "travel_tips": (
            "The temple is on a hilltop so wear comfortable walking shoes. Visit early morning for "
            "a peaceful experience. The Kiul River nearby adds to the scenic beauty."
        ),
        "best_season": "Winter",
        "best_time_of_day": "Morning",
        "crowd_level": "Moderate to High during festivals",
        "nearest_railway": "Jamui Railway Station (5 km)",
        "nearest_bus_stand": "Jamui Bus Stand (5 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (195 km)",
        "is_featured": 1,
        "is_hidden_gem": 0,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 3. Simultala Hill Station
    # ──────────────────────────────────────────────
    {
        "name": "Simultala Hill Station",
        "slug": "simultala-hill-station-jamui",
        "category": "mountain",
        "description": (
            "Simultala, often called the 'Mini Shimla of Bihar,' is a tranquil hill station located "
            "in the Jhajha block of Jamui district. Situated at an elevation of approximately "
            "242-243 meters above sea level, with Lattu Pahar reaching 1,200 feet, Simultala is "
            "known for its scenic hilly landscape, lush greenery, and pleasant climate. It holds "
            "cultural significance as the Tapo-Bhumi (meditation place) of Sri Ramakrishna Paramahansa. "
            "Historically, it was a popular retreat for affluent visitors from Bengal, evidenced by "
            "the many old abandoned villas scattered across the area. Key attractions include "
            "Lattu Pahar for sunset views, Haldi Jharna, Dharara Falls, Lilabhram Falls, the "
            "historic Naldanga Palace (Rajakothi), and the Shikhatia Ashram."
        ),
        "latitude": 24.7136,
        "longitude": 86.5422,
        "best_time_to_visit": "October to March (Winter and early Spring)",
        "entry_fee": "Free",
        "history": (
            "Simultala has been a well-known retreat since the British era, when affluent families "
            "from Bengal built villas here to escape the summer heat. The area is culturally significant "
            "as the Tapo-Bhumi of Sri Ramakrishna Paramahansa. The Naldanga Palace (Rajakothi) and "
            "the Shikhatia Ashram are prominent historical landmarks. The name 'Simultala' derives "
            "from the Simul (silk-cotton) trees that once dominated the landscape."
        ),
        "travel_tips": (
            "Simultala is on the Howrah-Delhi main line, making it easily accessible by train. "
            "Visit Lattu Pahar for stunning sunset views. Carry light woolens during winter months. "
            "Explore the abandoned colonial-era villas for a unique historical experience."
        ),
        "best_season": "Winter",
        "best_time_of_day": "Evening (for sunset from Lattu Pahar)",
        "crowd_level": "Low to Moderate",
        "nearest_railway": "Simultala Railway Station (0 km - on Howrah-Delhi main line)",
        "nearest_bus_stand": "Jhajha Bus Stand (15 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (220 km)",
        "is_featured": 1,
        "is_hidden_gem": 1,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 4. Kali Mandir, Malaypur
    # ──────────────────────────────────────────────
    {
        "name": "Kali Mandir, Malaypur",
        "slug": "kali-mandir-malaypur-jamui",
        "category": "temple",
        "description": (
            "Kali Mandir in Malaypur (Mallehpur) is a prominent temple dedicated to Goddess Kali, "
            "situated in the Barhat block near Jamui railway station. The temple is renowned for "
            "its annual Kali Mela (fair) held during Kali Puja, which attracts thousands of devotees "
            "from across Bihar. The temple is famous for its exceptional cleanliness, grandeur, and "
            "the tradition of being repainted and decorated with new lights every year. It serves "
            "as a major spiritual center for the region."
        ),
        "latitude": 24.9714,
        "longitude": 86.2533,
        "best_time_to_visit": "Year-round; Kali Puja (October-November) for the grand Mela",
        "entry_fee": "Free",
        "history": (
            "The Kali Mandir at Malaypur has been a center of Shakti worship for generations. "
            "The annual Kali Mela during Kali Puja is one of the largest religious gatherings in "
            "Jamui district. The temple has a unique tradition of annual renovation where the "
            "entire structure is repainted and adorned with new lighting each year."
        ),
        "travel_tips": (
            "Visit during Kali Puja (October-November) to experience the grand Kali Mela. "
            "The temple is easily accessible from Jamui railway station. Photography is "
            "generally permitted outside the main sanctum."
        ),
        "best_season": "Autumn (Kali Puja season)",
        "best_time_of_day": "Evening (for aarti)",
        "crowd_level": "High during Kali Mela, Moderate otherwise",
        "nearest_railway": "Jamui Railway Station (2 km)",
        "nearest_bus_stand": "Jamui Bus Stand (2 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (195 km)",
        "is_featured": 1,
        "is_hidden_gem": 0,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 5. Minto Tower, Gidhaur
    # ──────────────────────────────────────────────
    {
        "name": "Minto Tower, Gidhaur",
        "slug": "minto-tower-gidhaur-jamui",
        "category": "historical",
        "description": (
            "Minto Tower is a historic monument located in the heart of Gidhaur market in Jamui "
            "district. Built in 1909 by the Maharaja of Gidhaur, the tower was constructed to "
            "commemorate the visit of the British Viceroy, Lord Minto (not Lord Irwin as sometimes "
            "incorrectly cited). The tower stands as an important colonial-era landmark and a "
            "testament to the historical significance of the Gidhaur estate. It remains one of the "
            "most recognizable heritage structures in Jamui district."
        ),
        "latitude": 24.8579,
        "longitude": 86.3004,
        "best_time_to_visit": "October to March",
        "entry_fee": "Free",
        "history": (
            "The Minto Tower was built in 1909 by the Maharaja of Gidhaur to mark the visit of "
            "Lord Minto, the British Viceroy of India. Gidhaur was historically an important "
            "zamindari estate in Bihar. The tower reflects the colonial architectural style of "
            "the early 20th century and stands as a memorial to the historical ties between "
            "the Gidhaur royal family and British administration."
        ),
        "travel_tips": (
            "The tower is located in Gidhaur market and is easily accessible. Visit the nearby "
            "Giddheswar Temple for a combined historical and spiritual experience. Best visited "
            "during daylight hours for photography."
        ),
        "best_season": "Winter",
        "best_time_of_day": "Morning or Afternoon",
        "crowd_level": "Low",
        "nearest_railway": "Jamui Railway Station (20 km)",
        "nearest_bus_stand": "Gidhaur Bus Stop (0.5 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (215 km)",
        "is_featured": 0,
        "is_hidden_gem": 1,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 6. Maa Netula Temple
    # ──────────────────────────────────────────────
    {
        "name": "Maa Netula Temple",
        "slug": "maa-netula-temple-jamui",
        "category": "temple",
        "description": (
            "Maa Netula Temple (Maa Ambe Temple) is a well-known temple dedicated to Maa Ambe, "
            "situated in the village of Kumar in the Sikandra block of Jamui district. The temple "
            "is a significant pilgrimage destination for devotees of the Mother Goddess in the "
            "region. It attracts large gatherings during Navratri festivals. The temple is "
            "surrounded by natural greenery and offers a peaceful spiritual atmosphere."
        ),
        "latitude": 24.9558,
        "longitude": 86.0011,
        "best_time_to_visit": "Year-round; Navratri (March-April, September-October)",
        "entry_fee": "Free",
        "history": (
            "Maa Netula Temple has been a center of Shakti worship in the Sikandra block of "
            "Jamui for several generations. Dedicated to Maa Ambe (Mother Goddess), the temple "
            "is particularly revered during Navratri when special pujas and cultural programs "
            "are organized. The temple holds deep spiritual significance for the local community."
        ),
        "travel_tips": (
            "The temple is in a rural setting in Kumar village, Sikandra block. Local transport "
            "or private vehicle is recommended. Visit during Navratri for the festive atmosphere. "
            "Carry water and snacks as limited facilities are available nearby."
        ),
        "best_season": "Autumn and Spring (Navratri)",
        "best_time_of_day": "Morning",
        "crowd_level": "High during Navratri, Low otherwise",
        "nearest_railway": "Jamui Railway Station (25 km)",
        "nearest_bus_stand": "Sikandra Bus Stand (8 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (185 km)",
        "is_featured": 0,
        "is_hidden_gem": 1,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 7. Lachhuar Jain Temple
    # ──────────────────────────────────────────────
    {
        "name": "Lachhuar Jain Temple",
        "slug": "lachhuar-jain-temple-jamui",
        "category": "temple",
        "description": (
            "Lachhuar Jain Temple is a highly significant Jain pilgrimage site located in "
            "Lachhuar village in Jamui district. The temple complex features a historic "
            "dharamshala with 65 rooms and houses a revered black stone idol of Lord Mahavira "
            "believed to be over 2,600 years old. The site is closely linked to Kshatriya Kund "
            "Gram, which is traditionally believed to be the birthplace of Lord Mahavira, the "
            "24th Tirthankara of Jainism. This makes it one of the most important Jain "
            "heritage sites in Bihar."
        ),
        "latitude": 24.9145,
        "longitude": 86.0144,
        "best_time_to_visit": "October to March; Mahavir Jayanti (March-April)",
        "entry_fee": "Free",
        "history": (
            "Lachhuar is closely associated with the life of Lord Mahavira, the 24th Tirthankara "
            "of Jainism. The nearby Kshatriya Kund Gram is traditionally believed to be Mahavira's "
            "birthplace. The temple houses a black stone idol of Lord Mahavira estimated to be "
            "over 2,600 years old, making it one of the most ancient Jain relics in India. The "
            "dharamshala with 65 rooms was built to accommodate visiting pilgrims."
        ),
        "travel_tips": (
            "This is a major Jain pilgrimage site. Maintain respectful silence inside the temple. "
            "Photography may be restricted in the inner sanctum. The dharamshala offers accommodation "
            "for visiting pilgrims. Visit during Mahavir Jayanti for the grand celebrations."
        ),
        "best_season": "Winter",
        "best_time_of_day": "Morning",
        "crowd_level": "Moderate; High during Mahavir Jayanti",
        "nearest_railway": "Jamui Railway Station (20 km)",
        "nearest_bus_stand": "Lachhuar Bus Stop (1 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (190 km)",
        "is_featured": 1,
        "is_hidden_gem": 0,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 8. Bhim Bandh (Hot Springs)
    # ──────────────────────────────────────────────
    {
        "name": "Bhim Bandh Hot Springs",
        "slug": "bhim-bandh-hot-springs-jamui",
        "category": "nature",
        "description": (
            "Bhim Bandh is a renowned natural hot spring site located in the Bhimbandh Wildlife "
            "Sanctuary area between the Lakshmipur and Haveli Kharagpur jungles near the "
            "Jamui-Munger border. The springs are famous for their constant high temperatures "
            "ranging from 52 degrees C to 65 degrees C throughout the year, making them significant "
            "for geothermal research. According to Mahabharata legend, the Pandavas stayed in "
            "this forest during their exile, and Bhima constructed a dam (bandh) to merge two "
            "water sources, giving the site its name. Bhim Bandh is a popular picnic spot, "
            "especially during winter months."
        ),
        "latitude": 25.2300,
        "longitude": 86.2800,
        "best_time_to_visit": "October to February (Winter)",
        "entry_fee": "Nominal entry fee for sanctuary",
        "history": (
            "According to the Mahabharata, the Pandavas stayed in this forest during their "
            "period of exile. It is said that Bhima constructed a dam (bandh) to merge two "
            "water sources, giving the site its name 'Bhimbandh.' The natural hot springs "
            "have temperatures ranging from 52 to 65 degrees Celsius throughout the year. "
            "The site is part of the Bhimbandh Wildlife Sanctuary in the Kharagpur Hills."
        ),
        "travel_tips": (
            "The hot springs are within a wildlife sanctuary, so follow all forest department "
            "regulations. Best visited during winter when the contrast between cold weather and "
            "hot springs is most enjoyable. Carry your own food and water. Local guides are "
            "recommended for navigating the forest trails."
        ),
        "best_season": "Winter",
        "best_time_of_day": "Morning to Afternoon",
        "crowd_level": "Low to Moderate",
        "nearest_railway": "Jamui Railway Station (40 km)",
        "nearest_bus_stand": "Kharagpur Bus Stand (15 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (230 km)",
        "is_featured": 1,
        "is_hidden_gem": 1,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 9. Nagi Dam (Bird Sanctuary)
    # ──────────────────────────────────────────────
    {
        "name": "Nagi Dam Bird Sanctuary",
        "slug": "nagi-dam-bird-sanctuary-jamui",
        "category": "nature",
        "description": (
            "Nagi Dam Bird Sanctuary is a renowned Important Bird Area (IBA) and Ramsar site "
            "located near Jhajha in Jamui district, close to the Jharkhand border. It is "
            "approximately 31 km from Jamui railway station and 12 km from Jhajha railway "
            "station. The sanctuary is a paradise for birdwatchers, especially during the "
            "winter season (November to February) when thousands of migratory birds including "
            "the bar-headed goose congregate at the dam. Along with the nearby Nakti Dam, "
            "it forms one of Bihar's most important wetland ecosystems."
        ),
        "latitude": 24.8175,
        "longitude": 86.4000,
        "best_time_to_visit": "November to February (Winter migratory season)",
        "entry_fee": "Free",
        "history": (
            "Nagi Dam was constructed as an irrigation reservoir and has since evolved into one "
            "of Bihar's most significant bird habitats. Designated as an Important Bird Area (IBA) "
            "and a Ramsar site, it hosts thousands of migratory birds during winter months. "
            "Together with the nearby Nakti Dam, it forms a critical wetland ecosystem for "
            "avian conservation in eastern India."
        ),
        "travel_tips": (
            "Best visited early morning for optimal bird sighting. Carry binoculars and a "
            "telephoto lens for birdwatching. The dam is accessible from both Jamui and Jhajha "
            "railway stations. Winter months (November to February) offer the best migratory "
            "bird sightings including bar-headed goose and various duck species."
        ),
        "best_season": "Winter",
        "best_time_of_day": "Early Morning",
        "crowd_level": "Low",
        "nearest_railway": "Jhajha Railway Station (12 km)",
        "nearest_bus_stand": "Jhajha Bus Stand (12 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (235 km)",
        "is_featured": 1,
        "is_hidden_gem": 0,
        "family_friendly": 1,
    },
    # ──────────────────────────────────────────────
    # 10. Kshatriya Kund
    # ──────────────────────────────────────────────
    {
        "name": "Kshatriya Kund",
        "slug": "kshatriya-kund-jamui",
        "category": "cultural",
        "description": (
            "Kshatriya Kund Gram is a site of profound historical and religious importance "
            "in Jamui district, traditionally believed to be the birthplace of Lord Mahavira, "
            "the 24th Tirthankara of Jainism. The site features a picturesque waterfall "
            "surrounded by dense forest, making it both a spiritual and natural attraction. "
            "Jain pilgrims from across India visit this sacred site to pay homage. The area "
            "around Kshatriya Kund offers trekking opportunities through forested hills."
        ),
        "latitude": 24.9100,
        "longitude": 86.0200,
        "best_time_to_visit": "October to March; Mahavir Jayanti",
        "entry_fee": "Free",
        "history": (
            "Kshatriya Kund is traditionally recognized as the birthplace of Lord Mahavira "
            "(599 BCE - 527 BCE), the founder of Jainism. The site has been venerated by "
            "the Jain community for millennia. Archaeological and textual evidence supports "
            "the area's deep connection to early Jain history."
        ),
        "travel_tips": (
            "Combine your visit with Lachhuar Jain Temple which is nearby. The waterfall area "
            "requires a short trek through forest. Wear sturdy footwear and carry insect repellent. "
            "Respect the religious sanctity of the site."
        ),
        "best_season": "Winter and Monsoon (for waterfall)",
        "best_time_of_day": "Morning",
        "crowd_level": "Low; Moderate during Jain festivals",
        "nearest_railway": "Jamui Railway Station (22 km)",
        "nearest_bus_stand": "Lachhuar Bus Stop (3 km)",
        "nearest_airport": "Jay Prakash Narayan International Airport, Patna (192 km)",
        "is_featured": 0,
        "is_hidden_gem": 1,
        "family_friendly": 1,
    },
]


def seed_jamui_places():
    """Insert verified Jamui tourist places into the existing database."""
    inserted = 0
    skipped = 0

    with get_cursor(commit=True) as cur:
        # Dynamically look up Jamui district ID
        cur.execute("SELECT id FROM districts WHERE state_id = %s AND slug = 'jamui'", (STATE_ID,))
        j_row = cur.fetchone()
        jamui_district_id = j_row['id'] if j_row else 4

        for place in PLACES:
            # Check for duplicate slug
            cur.execute("SELECT id FROM places WHERE slug = %s", (place["slug"],))
            existing = cur.fetchone()
            if existing:
                print("  [SKIP] " + place["name"] + " (slug already exists: " + place["slug"] + ")")
                skipped += 1
                continue

            cur.execute("""
                INSERT INTO places (
                    state_id, district_id, name, slug, description, category,
                    latitude, longitude,
                    best_time_to_visit, entry_fee, history, travel_tips,
                    best_season, best_time_of_day, crowd_level,
                    nearest_railway, nearest_bus_stand, nearest_airport,
                    is_featured, is_hidden_gem, family_friendly
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s
                )
            """, (
                STATE_ID, jamui_district_id,
                place["name"], place["slug"], place["description"], place["category"],
                place["latitude"], place["longitude"],
                place["best_time_to_visit"], place["entry_fee"],
                place.get("history", ""), place.get("travel_tips", ""),
                place.get("best_season", ""), place.get("best_time_of_day", ""),
                place.get("crowd_level", ""),
                place.get("nearest_railway", ""), place.get("nearest_bus_stand", ""),
                place.get("nearest_airport", ""),
                place.get("is_featured", 0), place.get("is_hidden_gem", 0),
                place.get("family_friendly", 1),
            ))

            print("  [OK] Inserted: " + place["name"] + " (slug: " + place["slug"] + ")")
            inserted += 1

    print()
    print("=" * 60)
    print("Jamui Places Seed Results:")
    print("  Inserted: " + str(inserted))
    print("  Skipped (duplicates): " + str(skipped))
    print("  Total defined: " + str(len(PLACES)))
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("Seeding verified Jamui tourist places...")
    print("=" * 60)
    seed_jamui_places()
