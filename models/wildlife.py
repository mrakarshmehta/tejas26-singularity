"""
Bihar Wildlife Sanctuaries, Nature Reserves & Eco-Safari Directory Model
Provides protected national parks, river dolphin sanctuaries, Ramsar wetlands,
endangered wildlife checklists, and safari permit guidelines.
"""

WILDLIFE_SANCTUARIES_DB = [
    {
        "id": "reserve-valmiki-tiger",
        "slug": "valmiki-tiger-reserve",
        "name": "Valmiki National Park & Tiger Reserve",
        "district": "West Champaran",
        "type": "National Park & Project Tiger Reserve",
        "area_sq_km": 898.45,
        "ramsar_site": False,
        "best_season": "November to April",
        "entry_permit_required": True,
        "safari_available": True,
        "safari_types": ["Open Gypsy Jungle Safari", "Gandak River Boat Safari", "Canopy Eco-Walk"],
        "tagline": "Bihar's premier tiger kingdom nestled in the Terai foothills of the Himalayas.",
        "description": "Located along the Indo-Nepal border where the Gandak River enters the plains. Features dense moist Sal forests, alluvial grasslands, and rich biodiversity representing the Terai-Duar savanna ecosystem.",
        "key_fauna": [
            "Royal Bengal Tiger (Panthera tigris)",
            "Indian One-Horned Rhinoceros (migratory from Chitwan)",
            "Indian Leopard",
            "Sloth Bear",
            "Spotted Deer (Chital)",
            "Wild Boar",
            "Flying Squirrel"
        ],
        "key_avifauna": [
            "Great Indian Hornbill",
            "Kalij Pheasant",
            "Pallas's Fish Eagle",
            "Black Stork"
        ],
        "coordinates": {"lat": 27.3500, "lng": 84.1800},
        "nearest_hub": "Bettiah (80 km) / Gorakhpur Airport (130 km)"
    },
    {
        "id": "reserve-vikramshila-dolphin",
        "slug": "vikramshila-dolphin-sanctuary",
        "name": "Vikramshila Gangetic Dolphin Sanctuary",
        "district": "Bhagalpur",
        "type": "Riverine Protected Area",
        "area_sq_km": 60.0,
        "ramsar_site": False,
        "best_season": "October to June",
        "entry_permit_required": False,
        "safari_available": True,
        "safari_types": ["Silent Country Boat Dolphin Safari", "Riverbank Birdwatching Cruise"],
        "tagline": "India's only protected river sanctuary for the endangered Gangetic Dolphin.",
        "description": "A protected 60 km stretch of the Ganges River extending from Sultanganj to Kahalgaon. The sanctuary provides crucial refuge for the blind Gangetic Dolphin (Platanista gangetica), known locally as 'Susu' or 'Soons'.",
        "key_fauna": [
            "Gangetic River Dolphin (National Aquatic Animal)",
            "Smooth-Coated Indian Otter",
            "Gharial (Fish-eating Crocodile)",
            "Indian Softshell Turtle",
            "Greater Adjutant Stork (Garuda)"
        ],
        "key_avifauna": [
            "Indian Skimmer",
            "Greater Spotted Eagle",
            "River Tern",
            "Bar-headed Goose"
        ],
        "coordinates": {"lat": 25.2600, "lng": 87.0200},
        "nearest_hub": "Bhagalpur Junction (5 km) / Patna Airport (230 km)"
    },
    {
        "id": "reserve-kanwar-lake",
        "slug": "kanwar-lake-bird-sanctuary",
        "name": "Kanwar (Kabar) Taal Wetland Sanctuary",
        "district": "Begusarai",
        "type": "Ramsar Wetland & Bird Sanctuary",
        "area_sq_km": 67.5,
        "ramsar_site": True,
        "best_season": "November to February",
        "entry_permit_required": False,
        "safari_available": True,
        "safari_types": ["Traditional Rowboat Birdwatching", "Watchtower Observation"],
        "tagline": "Asia's largest freshwater oxbow lake and designated Ramsar wetland of international importance.",
        "description": "Formed by the meandering Gandak and Burhi Gandak rivers, Kabar Taal is a paradise for ornithologists, hosting over 100 species of migratory waterfowl flying along the Central Asian Flyway.",
        "key_fauna": [
            "Oriental White-Backed Vulture",
            "Long-Billed Vulture",
            "Fishing Cat",
            "Marsh Crocodile",
            "Freshwater Turtles"
        ],
        "key_avifauna": [
            "Sarus Crane",
            "Red-Crested Pochard",
            "Greylag Goose",
            "Northern Pintail",
            "Black-Necked Stork"
        ],
        "coordinates": {"lat": 25.6200, "lng": 86.1500},
        "nearest_hub": "Begusarai (22 km) / Barauni Junction (30 km)"
    },
    {
        "id": "reserve-bhimbandh",
        "slug": "bhimbandh-wildlife-sanctuary",
        "name": "Bhimbandh Wildlife Sanctuary & Thermal Springs",
        "district": "Munger",
        "type": "Wildlife Sanctuary & Geothermal Eco-Park",
        "area_sq_km": 681.99,
        "ramsar_site": False,
        "best_season": "October to March",
        "entry_permit_required": True,
        "safari_available": True,
        "safari_types": ["Forest Trail Trekking", "Thermal Springs Eco-Tour"],
        "tagline": "Pristine Kharagpur hills with natural thermal mineral springs and dense Sal forests.",
        "description": "Surrounded by undulating hill tracts south of the Ganges. Renowned for its bubbling geothermal hot springs (temperature 52°C to 65°C) rich in therapeutic minerals, nestled within dense deciduous woodland.",
        "key_fauna": [
            "Sloth Bear",
            "Sambhar Deer",
            "Barking Deer (Muntjac)",
            "Chousingha (Four-Horned Antelope)",
            "Wild Boar",
            "Jungle Cat"
        ],
        "key_avifauna": [
            "Peafowl",
            "Grey Junglefowl",
            "Emerald Dove",
            "Indian Pitta"
        ],
        "coordinates": {"lat": 25.0600, "lng": 86.4000},
        "nearest_hub": "Munger (56 km) / Jamalpur Junction (45 km)"
    },
    {
        "id": "reserve-kaimur",
        "slug": "kaimur-wildlife-sanctuary",
        "name": "Kaimur Wildlife Sanctuary & Eco-Plateau",
        "district": "Kaimur & Rohtas",
        "type": "Wildlife Sanctuary & Proposed Tiger Reserve",
        "area_sq_km": 1504.96,
        "ramsar_site": False,
        "best_season": "October to April",
        "entry_permit_required": True,
        "safari_available": True,
        "safari_types": ["4x4 Plateau Safari", "Waterfall Gorge Trek", "Prehistoric Cave Art Walk"],
        "tagline": "Bihar's largest wildlife landscape spanning dramatic sandstone canyons and waterfalls.",
        "description": "Spanning the Kaimur hills and Vindhyan escarpment. Features ancient rock paintings, the majestic Telhar Kund and Tutla Bhawani waterfalls, and vibrant populations of Indian leopards and antelopes.",
        "key_fauna": [
            "Indian Leopard",
            "Blackbuck (Antilope cervicapra)",
            "Chinkara (Indian Gazelle)",
            "Striped Hyena",
            "Nilgai (Blue Bull)",
            "Golden Jackal"
        ],
        "key_avifauna": [
            "Egyptian Vulture",
            "Crested Serpent Eagle",
            "Painted Francolin",
            "Indian Eagle-Owl"
        ],
        "coordinates": {"lat": 24.8500, "lng": 83.7500},
        "nearest_hub": "Sasaram (40 km) / Bhabua Road (35 km)"
    },
    {
        "id": "reserve-pant-rajgir",
        "slug": "pant-wildlife-sanctuary",
        "name": "Pant (Rajgir) Wildlife Sanctuary & Nature Safari",
        "district": "Nalanda",
        "type": "Eco-Tourism Sanctuary & Nature Safari Park",
        "area_sq_km": 35.84,
        "ramsar_site": False,
        "best_season": "October to March",
        "entry_permit_required": True,
        "safari_available": True,
        "safari_types": ["Glass Skywalk Bridge Walk", "Herbivore & Carnivore Safari", "Nature Trail Cycling"],
        "tagline": "State-of-the-art nature safari and glass skywalk in the five sacred hills of Rajgir.",
        "description": "Enclosing the scenic valley between Vipula, Ratna, Giri, Udaya, and Sona hills. Features modern glass skybridge, zoo safari enclosures, and medicinal botanical gardens.",
        "key_fauna": [
            "Spotted Deer",
            "Sambhar",
            "Nilgai",
            "Barking Deer",
            "Wild Boar",
            "Langur"
        ],
        "key_avifauna": [
            "Paradise Flycatcher",
            "Indian Roller",
            "Green Bee-Eater",
            "Coppersmith Barbet"
        ],
        "coordinates": {"lat": 25.0200, "lng": 85.4200},
        "nearest_hub": "Rajgir (3 km) / Patna Airport (100 km)"
    }
]

SAFARI_GUIDELINES = [
    {
        "topic": "Entry Permits & Advance Booking",
        "guideline": "For Valmiki Tiger Reserve and Rajgir Nature Safari, obtain online entry permits or arrive at forest entry gates before 8:00 AM for morning safari slots."
    },
    {
        "topic": "Dress Code & Wildlife Respect",
        "guideline": "Wear neutral earthy colors (khaki, olive green, brown). Maintain absolute silence; do not play loud music or use camera flashlights."
    },
    {
        "topic": "River & Boating Safety",
        "guideline": "During boat safaris in Vikramshila Dolphin Sanctuary or Kanwar Lake, ensure certified life jackets are fastened at all times and avoid using plastic bags."
    },
    {
        "topic": "Plastic-Free Zero Trace Zone",
        "guideline": "All sanctuaries are strict zero-plastic zones. Any littering attracts immediate forest department penalties."
    }
]

def get_all_sanctuaries():
    """Return all cataloged wildlife sanctuaries and nature reserves."""
    return WILDLIFE_SANCTUARIES_DB

def get_sanctuary_by_slug(slug):
    """Find sanctuary by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for w in WILDLIFE_SANCTUARIES_DB:
        if w["slug"] == s or w["id"] == s:
            return w
    return None

def get_sanctuaries_by_district(district):
    """Filter sanctuaries by district."""
    if not district or district.lower() == 'all':
        return WILDLIFE_SANCTUARIES_DB
    d_clean = district.lower().strip()
    return [w for w in WILDLIFE_SANCTUARIES_DB if d_clean in w["district"].lower()]

def get_ramsar_wetlands():
    """Return only Ramsar designated wetland sites."""
    return [w for w in WILDLIFE_SANCTUARIES_DB if w.get("ramsar_site")]

def get_safari_guidelines():
    """Return wildlife safari and forest guidelines."""
    return SAFARI_GUIDELINES

def get_endangered_species_list():
    """Extract distinct list of key endangered species across all reserves."""
    species = set()
    for w in WILDLIFE_SANCTUARIES_DB:
        for f in w.get("key_fauna", []):
            species.add(f)
    return sorted(list(species))