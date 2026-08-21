"""
HiddenYatra — Comprehensive Homestay & Local Stay Seed Script
Seeds 10 authentic, high-quality Bihar homestays with hosts, photos, amenities, and room details.
Run directly: python scripts/seed/seed_homestays.py
Or imported by models/connection.py during initial startup.
"""
import os
import sys
import json
import logging
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv()
from models.connection import get_cursor
from models.auth import hash_password

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HOMESTAYS_SEED_DATA = [
    {
        "host_username": "host_anjali_gaya",
        "host_email": "anjali.gaya@hiddenyatra.demo",
        "host_name": "Anjali Kumari",
        "host_bio": "Passionate heritage educator and cultural host in Bodh Gaya. Hosting mindful travellers since 2022 to share local Buddhist traditions, organic meals, and temple walks.",
        "host_languages": "Hindi, English, Magahi",
        "is_verified_badge": 1,
        "avg_host_rating": 4.9,
        "title": "Bodh Gaya Lotus Heritage Homestay",
        "slug": "bodh-gaya-lotus-heritage-homestay",
        "listing_type": "paid_homestay",
        "property_type": "heritage_homestay",
        "district_slug": "gaya",
        "address_text": "Near Kalachakra Ground, Mastipur, Bodh Gaya",
        "address_full": "House No. 42, Lotus Lane, Mastipur, Bodh Gaya, Gaya, Bihar 824231",
        "latitude": 24.69613,
        "longitude": 84.99128,
        "price_per_night": 1200.0,
        "max_guests": 4,
        "num_rooms": 2,
        "num_beds": 2,
        "num_bathrooms": 2,
        "amenities": ["wifi", "hot_water", "local_food", "meals", "power_backup", "garden", "balcony", "guide"],
        "description": "Experience serene and mindful living at Bodh Gaya Lotus Heritage Homestay, located just 800 metres from the UNESCO World Heritage Mahabodhi Temple.\n\nOur traditional brick and clay home features a shaded open-air rooftop terrace ideal for morning yoga, meditation, and reading. Enjoy freshly prepared satvik home-cooked Bihar meals including Dal-Bhat-Bhujia, sattu parathas, and seasonal herbal teas. The guest rooms are spacious, air-cooled, with spotless attached private bathrooms and high-speed Wi-Fi.",
        "house_rules": "• Quiet hours after 10:00 PM\n• Shoes off inside guest rooms\n• Vegetarian meals served\n• No smoking or alcohol on premises",
        "check_in_time": "12:00 PM",
        "check_out_time": "11:00 AM",
        "cover_image": "stay_demo_gaya_cover.jpg",
        "is_featured": 1,
        "avg_rating": 4.9,
        "review_count": 28,
        "view_count": 145,
        "photos": [
            {"filename": "stay_demo_gaya_cover.jpg", "caption": "Serene exterior & sunlit courtyard", "sort_order": 0},
            {"filename": "stay_demo_gaya_bedroom.jpg", "caption": "Comfortable master bedroom with study desk", "sort_order": 1},
            {"filename": "stay_demo_gaya_terrace.jpg", "caption": "Peaceful rooftop yoga & meditation terrace", "sort_order": 2},
            {"filename": "stay_demo_gaya_dining.jpg", "caption": "Traditional dining area for home-cooked meals", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_neha_nalanda",
        "host_email": "neha.nalanda@hiddenyatra.demo",
        "host_name": "Neha Singh",
        "host_bio": "Certified local nature guide and eco-homestay host in Rajgir. Fond of sharing Magadha history, hot spring lore, and cycling routes around Nalanda ruins.",
        "host_languages": "Hindi, English, Magahi",
        "is_verified_badge": 1,
        "avg_host_rating": 4.8,
        "title": "Rajgir Green Valley Eco Homestay",
        "slug": "rajgir-green-valley-eco-homestay",
        "listing_type": "paid_homestay",
        "property_type": "eco_cottage",
        "district_slug": "nalanda",
        "address_text": "Venuvan Valley Road, Rajgir, Nalanda",
        "address_full": "Plot 18, Bamboo Grove Path, Rajgir, Nalanda, Bihar 803116",
        "latitude": 25.01889,
        "longitude": 85.42194,
        "price_per_night": 1500.0,
        "max_guests": 5,
        "num_rooms": 2,
        "num_beds": 3,
        "num_bathrooms": 2,
        "amenities": ["wifi", "hot_water", "ac", "parking", "local_food", "garden", "balcony", "guide", "pickup"],
        "description": "Nestled at the gentle foothills of the Rajgir mountain range, Rajgir Green Valley Eco Homestay is an environmentally conscious cottage built with local stone, bamboo, and terracotta.\n\nWake up to the birdsong of Venuvan, breathe in the fresh mountain air, and explore nearby Gridhakuta (Vulture Peak) and the ancient Nalanda University ruins. We offer complimentary bicycles, herbal tea from our garden, and authentic Bihari culinary classics including Khaja from Silao and hot Litti Chokha.",
        "house_rules": "• Eco-friendly stay: please conserve water and power\n• Check-in with valid ID\n• Mountain bicycle gear available upon request",
        "check_in_time": "01:00 PM",
        "check_out_time": "11:00 AM",
        "cover_image": "stay_demo_rajgir_cover.jpg",
        "is_featured": 1,
        "avg_rating": 4.8,
        "review_count": 31,
        "view_count": 150,
        "photos": [
            {"filename": "stay_demo_rajgir_cover.jpg", "caption": "Eco cottage exterior with flowering garden", "sort_order": 0},
            {"filename": "stay_demo_rajgir_bedroom.jpg", "caption": "Cosy timber-accented guest bedroom", "sort_order": 1},
            {"filename": "stay_demo_rajgir_garden.jpg", "caption": "Lush garden walkway with mountain backdrop", "sort_order": 2},
            {"filename": "stay_demo_rajgir_bathroom.jpg", "caption": "Modern private attached bathroom with hot shower", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_sanjay_jamui",
        "host_email": "sanjay.jamui@hiddenyatra.demo",
        "host_name": "Sanjay Marandi",
        "host_bio": "Nature enthusiast, organic horticulturist, and community homestay pioneer in Simultala Hills. Welcoming travelers to experience the peaceful climate of the Mini-Shimla of Bihar.",
        "host_languages": "Hindi, Santhali, Angika, English",
        "is_verified_badge": 1,
        "avg_host_rating": 4.9,
        "title": "Simultala Pine Breeze Forest Stay",
        "slug": "simultala-pine-breeze-forest-stay",
        "listing_type": "paid_homestay",
        "property_type": "hill_cottage",
        "district_slug": "jamui",
        "address_text": "Litti Para Road, Simultala, Jamui",
        "address_full": "Pine Ridge Estate, Post Simultala, Dist Jamui, Bihar 811316",
        "latitude": 24.7125,
        "longitude": 86.54167,
        "price_per_night": 1000.0,
        "max_guests": 4,
        "num_rooms": 2,
        "num_beds": 2,
        "num_bathrooms": 1,
        "amenities": ["hot_water", "parking", "local_food", "meals", "garden", "balcony", "guide", "pet_friendly", "first_aid"],
        "description": "Perched amidst the fragrant pine and sal forests of Simultala, this heritage-style hill cottage offers cool breezes, pure country air, and tranquility.\n\nHistorically celebrated as a health resort during the colonial era, Simultala remains Bihar's hidden hill haven. Enjoy morning walks to Lattu Pahar and Haldi Jharana waterfalls, starry night campfires, and authentic Chulha-cooked Bihari cuisine with fresh organic vegetables from our farm.",
        "house_rules": "• Campfire permitted in designated outdoor stone pit\n• Quiet hours after 10:00 PM\n• Pets welcome in outdoor & veranda spaces",
        "check_in_time": "12:00 PM",
        "check_out_time": "10:30 AM",
        "cover_image": "stay_demo_simultala_cover.jpg",
        "is_featured": 0,
        "avg_rating": 4.9,
        "review_count": 19,
        "view_count": 138,
        "photos": [
            {"filename": "stay_demo_simultala_cover.jpg", "caption": "Pine grove hill cottage exterior", "sort_order": 0},
            {"filename": "stay_demo_simultala_bedroom.jpg", "caption": "Spacious bedroom with garden vista", "sort_order": 1},
            {"filename": "stay_demo_simultala_veranda.jpg", "caption": "Panoramic sunlit veranda for reading & tea", "sort_order": 2},
            {"filename": "stay_demo_simultala_dining.jpg", "caption": "Earthen-pot organic meal dining space", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_imtiaz_bhagalpur",
        "host_email": "imtiaz.bhagalpur@hiddenyatra.demo",
        "host_name": "Mohammad Imtiaz",
        "host_bio": "Master craftsman & Tussar silk heritage host in Champanagar, Bhagalpur. Offering authentic artisan stays with handloom demonstrations and Gangetic culture.",
        "host_languages": "Hindi, Urdu, Angika, English",
        "is_verified_badge": 1,
        "avg_host_rating": 4.8,
        "title": "Silk City Weaver's Heritage Homestay",
        "slug": "silk-city-weavers-heritage-homestay",
        "listing_type": "paid_homestay",
        "property_type": "heritage_homestay",
        "district_slug": "bhagalpur",
        "address_text": "Weavers Colony, Champanagar, Bhagalpur",
        "address_full": "Resham Kunj, Ward 14, Champanagar, Bhagalpur, Bihar 812004",
        "latitude": 25.24445,
        "longitude": 86.97184,
        "price_per_night": 1100.0,
        "max_guests": 4,
        "num_rooms": 2,
        "num_beds": 2,
        "num_bathrooms": 1,
        "amenities": ["wifi", "ac", "hot_water", "parking", "local_food", "meals", "power_backup", "guide"],
        "description": "Immerse yourself in India's famous Silk City at Weaver's Heritage Homestay.\n\nLocated in the historic weaving quarter of Champanagar, our family has practiced Tussar silk weaving for four generations. Guests can try their hand on traditional handlooms, learn about silk cocoon harvesting, enjoy famous Bhagalpuri Katarni rice and fish curry, and explore Vikramshila Buddhist University ruins.",
        "house_rules": "• Free 1-hour handloom weaving demonstration for guests\n• Check-in with valid photo ID\n• No loud music after 10 PM",
        "check_in_time": "01:00 PM",
        "check_out_time": "11:00 AM",
        "cover_image": "stay_demo_bhagalpur_cover.jpg",
        "is_featured": 0,
        "avg_rating": 4.8,
        "review_count": 24,
        "view_count": 132,
        "photos": [
            {"filename": "stay_demo_bhagalpur_cover.jpg", "caption": "Traditional brick & lime courtyard entrance", "sort_order": 0},
            {"filename": "stay_demo_bhagalpur_bedroom.jpg", "caption": "Silk-furnished comfortable guest bedroom", "sort_order": 1},
            {"filename": "stay_demo_bhagalpur_courtyard.jpg", "caption": "Active handloom weaving courtyard", "sort_order": 2},
            {"filename": "stay_demo_bhagalpur_dining.jpg", "caption": "Dining area serving authentic Katarni rice meals", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_rajesh_patna",
        "host_email": "rajesh.patna@hiddenyatra.demo",
        "host_name": "Rajeshwar Prasad",
        "host_bio": "Retired history professor & Patna heritage enthusiast. Hosting travelers wishing to explore the ancient capital of Pataliputra, Golghar, and Patna Museum.",
        "host_languages": "Hindi, English, Bhojpuri",
        "is_verified_badge": 1,
        "avg_host_rating": 4.9,
        "title": "Patliputra Heritage Courtyard Stay",
        "slug": "patliputra-heritage-courtyard-stay",
        "listing_type": "paid_homestay",
        "property_type": "heritage_homestay",
        "district_slug": "patna",
        "address_text": "Near Gandhi Maidan, Exhibition Road, Patna",
        "address_full": "Prasad Niwas, Lane 3, South Gandhi Maidan, Patna, Bihar 800001",
        "latitude": 25.62925,
        "longitude": 85.04891,
        "price_per_night": 1800.0,
        "max_guests": 4,
        "num_rooms": 2,
        "num_beds": 2,
        "num_bathrooms": 2,
        "amenities": ["wifi", "ac", "hot_water", "parking", "local_food", "meals", "power_backup", "garden", "balcony"],
        "description": "Stay in a meticulously preserved 1930s heritage colonial courtyard mansion in central Patna.\n\nFeaturing tall high ceilings, handcrafted teak wood furniture, a peaceful inner garden courtyard, and high-speed Wi-Fi. Located within easy reach of Takht Sri Patna Sahib, Bihar Museum, Golghar, and the Ganges Riverfront. Freshly made breakfast with local delicacies like Chura-Dahi and Sattu Puri included.",
        "house_rules": "• Valid government photo ID mandatory upon arrival\n• Gate closes at 11:00 PM (night key provided upon request)\n• Peaceful residential neighborhood",
        "check_in_time": "02:00 PM",
        "check_out_time": "11:30 AM",
        "cover_image": "stay_demo_patna_cover.jpg",
        "is_featured": 1,
        "avg_rating": 4.9,
        "review_count": 46,
        "view_count": 165,
        "photos": [
            {"filename": "stay_demo_patna_cover.jpg", "caption": "Grand colonial courtyard facade", "sort_order": 0},
            {"filename": "stay_demo_patna_bedroom.jpg", "caption": "Classic heritage bedroom with high ceilings", "sort_order": 1},
            {"filename": "stay_demo_patna_living.jpg", "caption": "Vintage lounge and personal historical library", "sort_order": 2},
            {"filename": "stay_demo_patna_bathroom.jpg", "caption": "Modern en-suite bathroom with 24/7 hot water", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_ramakant_vaishali",
        "host_email": "ramakant.vaishali@hiddenyatra.demo",
        "host_name": "Ramakant Shukla",
        "host_bio": "Organic mango orchard farmer and panchayat elder in Vaishali. Hosting backpackers and history enthusiasts for free community cultural exchange.",
        "host_languages": "Hindi, Bajjika",
        "is_verified_badge": 1,
        "avg_host_rating": 5.0,
        "title": "Vaishali Mango Orchard Village Stay",
        "slug": "vaishali-mango-orchard-village-stay",
        "listing_type": "free_stay",
        "property_type": "farmstay",
        "district_slug": "vaishali",
        "address_text": "Near Buddha Relic Stupa, Basarh, Vaishali",
        "address_full": "Shukla Farm, Basarh Gram, Vaishali District, Bihar 844128",
        "latitude": 25.9875,
        "longitude": 85.1275,
        "price_per_night": 0.0,
        "max_guests": 4,
        "num_rooms": 2,
        "num_beds": 2,
        "num_bathrooms": 1,
        "amenities": ["local_food", "meals", "garden", "parking", "guide", "pet_friendly"],
        "description": "Experience true Bihari rural hospitality at this free community village stay set within a 5-acre Shahi mango orchard.\n\nVaishali is the world's first republic and sacred land of Lord Buddha and Mahavira. Guests stay in clean earthen guest cottages, sleep on traditional charpais under starry night skies, taste fresh cow milk and organic seasonal fruits, and explore the ancient Ashoka Pillar and Coronation Tank.",
        "house_rules": "• Free community stay for travelers, students, and culture seekers\n• Please respect rural village customs and traditions\n• Help in organic farming activities is warmly appreciated",
        "check_in_time": "11:00 AM",
        "check_out_time": "10:00 AM",
        "cover_image": "stay_demo_vaishali_cover.jpg",
        "is_featured": 1,
        "avg_rating": 5.0,
        "review_count": 15,
        "view_count": 142,
        "photos": [
            {"filename": "stay_demo_vaishali_cover.jpg", "caption": "Organic mango orchard cottage view", "sort_order": 0},
            {"filename": "stay_demo_vaishali_farm.jpg", "caption": "Shahi mango tree groves and walking path", "sort_order": 1},
            {"filename": "stay_demo_vaishali_courtyard.jpg", "caption": "Village chaupal and open sitting area", "sort_order": 2},
            {"filename": "stay_demo_vaishali_bedroom.jpg", "caption": "Clean, airy rural bedroom with traditional charpai", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_sharda_madhubani",
        "host_email": "sharda.madhubani@hiddenyatra.demo",
        "host_name": "Sharda Devi",
        "host_bio": "State Awardee Madhubani Painting artist in Ranti/Jhanjharpur village. Offering authentic art immersion stays with daily folk painting workshops and Mithila food.",
        "host_languages": "Hindi, Maithili, English",
        "is_verified_badge": 1,
        "avg_host_rating": 4.9,
        "title": "Mithila Folk Art & Heritage Homestay",
        "slug": "mithila-folk-art-heritage-homestay",
        "listing_type": "paid_homestay",
        "property_type": "art_homestay",
        "district_slug": "jhanjharpur-madhubani",
        "address_text": "Artist Colony, Ranti Village, Madhubani",
        "address_full": "Kala Kuteer, Ranti Post, Madhubani District, Bihar 847211",
        "latitude": 26.355,
        "longitude": 86.085,
        "price_per_night": 800.0,
        "max_guests": 3,
        "num_rooms": 1,
        "num_beds": 2,
        "num_bathrooms": 1,
        "amenities": ["wifi", "local_food", "meals", "garden", "guide", "pet_friendly", "wheelchair"],
        "description": "Live inside a living canvas in the heartland of Mithila!\n\nEvery wall of our traditional home is painted with authentic handmade Madhubani (Mithila) art depicting Ramayana scenes, nature, and Kohbar motifs. Guests receive complimentary hands-on folk art lessons using natural bamboo twigs and handmade paper, and enjoy homemade Maithili cuisine (Makhana Kheer, Fish Curry, and Dal-Puri).",
        "house_rules": "• Daily morning folk art workshop included for guests\n• Respect original artwork on walls and murals\n• Traditional vegetarian & Mithila fish meals served",
        "check_in_time": "12:00 PM",
        "check_out_time": "11:00 AM",
        "cover_image": "stay_demo_madhubani_cover.jpg",
        "is_featured": 0,
        "avg_rating": 4.9,
        "review_count": 33,
        "view_count": 140,
        "photos": [
            {"filename": "stay_demo_madhubani_cover.jpg", "caption": "Mural-painted courtyard entrance", "sort_order": 0},
            {"filename": "stay_demo_madhubani_bedroom.jpg", "caption": "Guest room decorated with traditional Madhubani wall murals", "sort_order": 1},
            {"filename": "stay_demo_madhubani_workshop.jpg", "caption": "Active painting studio with natural dye pots", "sort_order": 2},
            {"filename": "stay_demo_madhubani_courtyard.jpg", "caption": "Spacious central courtyard for evening folklore discussions", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_manju_munger",
        "host_email": "manju.munger@hiddenyatra.demo",
        "host_name": "Manju Sinha",
        "host_bio": "Certified yoga instructor and home baker in Munger. Offers mindful stays next to the Ganges and near the renowned Bihar School of Yoga.",
        "host_languages": "Hindi, English",
        "is_verified_badge": 1,
        "avg_host_rating": 4.8,
        "title": "Munger Ganga Riverfront Yoga Stay",
        "slug": "munger-ganga-riverfront-yoga-stay",
        "listing_type": "paid_homestay",
        "property_type": "yoga_retreat",
        "district_slug": "munger",
        "address_text": "Ganga Darshan Road, Near Munger Fort, Munger",
        "address_full": "Ashram View Villa, Ganga Ghat Path, Munger, Bihar 811201",
        "latitude": 25.375,
        "longitude": 86.475,
        "price_per_night": 1400.0,
        "max_guests": 4,
        "num_rooms": 2,
        "num_beds": 2,
        "num_bathrooms": 2,
        "amenities": ["wifi", "hot_water", "ac", "local_food", "meals", "balcony", "garden", "power_backup"],
        "description": "Recharge your mind, body, and spirit at Munger Ganga Riverfront Yoga Stay.\n\nEnjoy sunrise yoga sessions on our open terrace looking out over the sacred river Ganges and historic Munger Fort walls. We serve Ayurvedic vegetarian breakfasts, herbal teas, and assist guests with visits to Kashtaharini Ghat, Sita Kund, and Bhimbandh Wildlife Sanctuary.",
        "house_rules": "• Daily morning yoga session (optional for guests)\n• Quiet hours after 9:30 PM\n• Sattvic vegetarian meals only",
        "check_in_time": "01:00 PM",
        "check_out_time": "11:00 AM",
        "cover_image": "stay_demo_munger_cover.jpg",
        "is_featured": 0,
        "avg_rating": 4.8,
        "review_count": 21,
        "view_count": 126,
        "photos": [
            {"filename": "stay_demo_munger_cover.jpg", "caption": "Riverfront property exterior with lush trees", "sort_order": 0},
            {"filename": "stay_demo_munger_bedroom.jpg", "caption": "Minimalist and airy bedroom with wooden floor", "sort_order": 1},
            {"filename": "stay_demo_munger_terrace.jpg", "caption": "Sunrise yoga and meditation deck", "sort_order": 2},
            {"filename": "stay_demo_munger_dining.jpg", "caption": "Organic satvik vegetarian breakfast table", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_ravi_rohtas",
        "host_email": "ravi.rohtas@hiddenyatra.demo",
        "host_name": "Ravi Shankar Pandey",
        "host_bio": "Local trekking leader and heritage lover from Sasaram. Guiding visitors to Rohtasgarh Fort, Tutla Bhawani Waterfall, and Sher Shah Tomb.",
        "host_languages": "Hindi, Bhojpuri, English",
        "is_verified_badge": 1,
        "avg_host_rating": 4.9,
        "title": "Sasaram Sher Shah Heritage Homestay",
        "slug": "sasaram-sher-shah-heritage-homestay",
        "listing_type": "paid_homestay",
        "property_type": "heritage_homestay",
        "district_slug": "rohtas",
        "address_text": "Tomb Circular Road, Sasaram, Rohtas",
        "address_full": "Heritage Lane 5, Near Grand Tomb Gate, Sasaram, Bihar 821115",
        "latitude": 24.954,
        "longitude": 84.032,
        "price_per_night": 1000.0,
        "max_guests": 5,
        "num_rooms": 2,
        "num_beds": 3,
        "num_bathrooms": 2,
        "amenities": ["wifi", "ac", "hot_water", "parking", "local_food", "meals", "guide", "pickup", "power_backup"],
        "description": "Stay in a restored sandstone haveli walking distance from the majestic water mausoleum of Sher Shah Suri in Sasaram.\n\nOur property is the perfect base for exploring Rohtasgarh Fort, Dhuan Kund waterfalls, and the Kaimur hill plateau. Features modern clean rooms, private secure parking, local guide support, and spicy Bihari mutton or paneer thali dinners.",
        "house_rules": "• Guided trekking excursions available on advance request\n• ID verification mandatory\n• Respect local monument regulations",
        "check_in_time": "12:00 PM",
        "check_out_time": "11:00 AM",
        "cover_image": "stay_demo_rohtas_cover.jpg",
        "is_featured": 1,
        "avg_rating": 4.9,
        "review_count": 35,
        "view_count": 127,
        "photos": [
            {"filename": "stay_demo_rohtas_cover.jpg", "caption": "Sandstone heritage home exterior", "sort_order": 0},
            {"filename": "stay_demo_rohtas_bedroom.jpg", "caption": "Spacious traditional bedroom with comfortable beds", "sort_order": 1},
            {"filename": "stay_demo_rohtas_lounge.jpg", "caption": "Upper floor veranda lounge overlooking city skyline", "sort_order": 2},
            {"filename": "stay_demo_rohtas_bathroom.jpg", "caption": "Modern attached bathroom with 24/7 hot water", "sort_order": 3}
        ]
    },
    {
        "host_username": "host_kavita_kaimur",
        "host_email": "kavita.kaimur@hiddenyatra.demo",
        "host_name": "Kavita Tiwari",
        "host_bio": "Eco-conservationist and village homestay host in Adhaura / Kaimur hills. Offering free hospitality to nature lovers, birdwatchers, and forest trekkers.",
        "host_languages": "Hindi, Bhojpuri",
        "is_verified_badge": 1,
        "avg_host_rating": 4.9,
        "title": "Kaimur Plateau Waterfall Farmstay",
        "slug": "kaimur-plateau-waterfall-farmstay",
        "listing_type": "free_stay",
        "property_type": "farmstay",
        "district_slug": "kaimur",
        "address_text": "Near Telhar Kund Road, Bhabhua, Kaimur",
        "address_full": "Adhaura Plateau Road, Kaimur Hills, Bihar 821102",
        "latitude": 24.81,
        "longitude": 83.58,
        "price_per_night": 0.0,
        "max_guests": 3,
        "num_rooms": 1,
        "num_beds": 2,
        "num_bathrooms": 1,
        "amenities": ["local_food", "meals", "garden", "guide", "pet_friendly", "first_aid"],
        "description": "Immerse yourself in raw, untouched wilderness on the Kaimur Plateau! This free community stay is hosted on an organic farm near Telhar Kund and Karkat Waterfalls.\n\nSleep under starry skies, enjoy freshly harvested organic meals, listen to forest birds at dawn, and explore hidden canyon trails. Ideal for trekking enthusiasts and nature photographers.",
        "house_rules": "• Free stay for nature lovers & environmentalists\n• Zero plastic waste zone: please carry back non-biodegradable waste\n• Forest trekking must follow sanctuary safety guidelines",
        "check_in_time": "12:00 PM",
        "check_out_time": "11:00 AM",
        "cover_image": "stay_demo_kaimur_cover.jpg",
        "is_featured": 0,
        "avg_rating": 4.9,
        "review_count": 14,
        "view_count": 126,
        "photos": [
            {"filename": "stay_demo_kaimur_cover.jpg", "caption": "Scenic stone farm cottage on Kaimur plateau", "sort_order": 0},
            {"filename": "stay_demo_kaimur_bedroom.jpg", "caption": "Cosy timber-finish bedroom with valley breeze", "sort_order": 1},
            {"filename": "stay_demo_kaimur_waterfall.jpg", "caption": "Nearby Telhar Kund waterfall stream", "sort_order": 2},
            {"filename": "stay_demo_kaimur_lawn.jpg", "caption": "Open-air seating & campfire area under the night sky", "sort_order": 3}
        ]
    }
]


def seed_all_homestays(cur):
    """Seed all 10 authentic Bihar homestays into MySQL database."""
    default_pw_hash = hash_password('Host@123')
    seeded_count = 0

    for item in HOMESTAYS_SEED_DATA:
        # 1. Resolve district ID
        d_slug = item['district_slug']
        cur.execute("SELECT id FROM districts WHERE slug = %s", (d_slug,))
        row = cur.fetchone()
        if not row:
            cur.execute("SELECT id FROM districts WHERE name LIKE %s OR slug LIKE %s", (f"%{d_slug}%", f"%{d_slug}%"))
            row = cur.fetchone()
        district_id = row['id'] if row else 1

        # 2. Upsert User
        username = item['host_username']
        email = item['host_email']
        display_name = item['host_name']

        cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        user_row = cur.fetchone()
        if user_row:
            user_id = user_row['id']
            cur.execute("""
                UPDATE users SET display_name = %s, full_name = %s, is_host = 1, status = 'active', email_verified = 1
                WHERE id = %s
            """, (display_name, display_name, user_id))
        else:
            cur.execute("""
                INSERT INTO users (username, email, password_hash, display_name, full_name, is_host, status, email_verified)
                VALUES (%s, %s, %s, %s, %s, 1, 'active', 1)
            """, (username, email, default_pw_hash, display_name, display_name))
            user_id = cur.lastrowid

        # 3. Upsert Host Profile
        cur.execute("SELECT id FROM host_profiles WHERE user_id = %s", (user_id,))
        hp_row = cur.fetchone()
        if hp_row:
            host_profile_id = hp_row['id']
            cur.execute("""
                UPDATE host_profiles SET
                    bio = %s, languages = %s, district_id = %s, address_line = %s,
                    verification_status = 'approved', is_verified_badge = %s, avg_host_rating = %s
                WHERE id = %s
            """, (item['host_bio'], item['host_languages'], district_id, item['address_text'],
                  item['is_verified_badge'], item['avg_host_rating'], host_profile_id))
        else:
            cur.execute("""
                INSERT INTO host_profiles
                    (user_id, bio, languages, address_line, district_id, verification_status,
                     is_verified_badge, avg_host_rating, total_hosted, response_rate, response_time_hrs)
                VALUES (%s, %s, %s, %s, %s, 'approved', %s, %s, 12, 98.0, 1.5)
            """, (user_id, item['host_bio'], item['host_languages'], item['address_text'], district_id,
                  item['is_verified_badge'], item['avg_host_rating']))
            host_profile_id = cur.lastrowid

        # 4. Upsert Host Listing
        amenities_json = json.dumps(item['amenities'])
        slug = item['slug']

        cur.execute("SELECT id FROM host_listings WHERE slug = %s", (slug,))
        hl_row = cur.fetchone()
        if hl_row:
            listing_id = hl_row['id']
            cur.execute("""
                UPDATE host_listings SET
                    host_id = %s, listing_type = %s, title = %s, description = %s,
                    district_id = %s, address_text = %s, address_full = %s,
                    latitude = %s, longitude = %s, price_per_night = %s,
                    max_guests = %s, num_rooms = %s, num_beds = %s, num_bathrooms = %s,
                    property_type = %s, amenities = %s, house_rules = %s,
                    check_in_time = %s, check_out_time = %s, cancellation_policy = %s,
                    cover_image = %s, status = 'published', is_featured = %s,
                    avg_rating = %s, review_count = %s, view_count = %s
                WHERE id = %s
            """, (
                host_profile_id, item['listing_type'], item['title'], item['description'],
                district_id, item['address_text'], item['address_full'],
                item['latitude'], item['longitude'], item['price_per_night'],
                item['max_guests'], item['num_rooms'], item['num_beds'], item['num_bathrooms'],
                item['property_type'], amenities_json, item['house_rules'],
                item['check_in_time'], item['check_out_time'], 'flexible',
                item['cover_image'], item['is_featured'],
                item['avg_rating'], item['review_count'], item['view_count'],
                listing_id
            ))
        else:
            cur.execute("""
                INSERT INTO host_listings
                    (host_id, listing_type, title, slug, description,
                     district_id, address_text, address_full, latitude, longitude,
                     price_per_night, currency, max_guests, num_rooms, num_beds, num_bathrooms,
                     property_type, amenities, house_rules, check_in_time, check_out_time,
                     cancellation_policy, cover_image, status, is_featured,
                     avg_rating, review_count, view_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'INR', %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, 'flexible', %s, 'published', %s, %s, %s, %s)
            """, (
                host_profile_id, item['listing_type'], item['title'], slug, item['description'],
                district_id, item['address_text'], item['address_full'], item['latitude'], item['longitude'],
                item['price_per_night'], item['max_guests'], item['num_rooms'], item['num_beds'], item['num_bathrooms'],
                item['property_type'], amenities_json, item['house_rules'], item['check_in_time'], item['check_out_time'],
                item['cover_image'], item['is_featured'], item['avg_rating'], item['review_count'], item['view_count']
            ))
            listing_id = cur.lastrowid

        # 5. Insert listing photos
        cur.execute("DELETE FROM listing_photos WHERE listing_id = %s", (listing_id,))
        for p in item.get('photos', []):
            cur.execute("""
                INSERT INTO listing_photos (listing_id, filename, caption, sort_order)
                VALUES (%s, %s, %s, %s)
            """, (listing_id, p['filename'], p['caption'], p['sort_order']))

        seeded_count += 1
        logger.info(f"  ✓ Seeded homestay '{item['title']}' ({item['listing_type']}) in {d_slug}")

    return seeded_count


if __name__ == '__main__':
    print("═════════════════════════════════════════════════════════")
    print("  HiddenYatra — Seeding 10 Authentic Bihar Homestays")
    print("═════════════════════════════════════════════════════════")
    with get_cursor(commit=True) as cursor:
        count = seed_all_homestays(cursor)
        print(f"\n✅ Successfully seeded {count} homestays into MySQL database!")
