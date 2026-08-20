"""
Bihar Eco-Trails, Wilderness Expeditions & Hill Treks Model
Provides scenic hiking routes, elevation profiles, difficulty ratings,
GPX coordinates, water sources, and wilderness safety guidelines.
"""

ECO_TREKS_DB = [
    {
        "id": "trek-mandar-hill",
        "slug": "mandar-hill-granite-ascent",
        "name": "Mandar Giri Sacred Granite Hill Ascent",
        "district": "Banka",
        "elevation_gain_m": 215,
        "summit_elevation_m": 244,
        "distance_km": 3.8,
        "difficulty": "Moderate",
        "duration_hours": "3 - 4 Hours",
        "best_season": "October to March",
        "trail_type": "Rock-Cut Stone Steps & Monolithic Granite Ridge",
        "coordinates": {"lat": 24.8410, "lng": 87.0250},
        "description": "An imposing monolithic granite hill mythologically revered as Mount Mandara used to churn the cosmic ocean (Samudra Manthan). Features rock carvings, Paapharni lake at the base, and ancient Vishnu sculptures.",
        "trail_highlights": [
            "Ancient serpent carving of King Vasuki coiled around the granite mountain",
            "Mandar Giri Digambara Jain Temple at the summit",
            "Paapharni holy water tank and natural rock-cut cisterns"
        ],
        "gear_required": ["Hiking boots with stone grip", "2L Hydration bottle", "Sun protection hat"]
    },
    {
        "id": "trek-brahmayoni-peak",
        "slug": "brahmayoni-peak-trail",
        "name": "Brahmayoni Holy Peak & Ridge Trail",
        "district": "Gaya",
        "elevation_gain_m": 145,
        "summit_elevation_m": 230,
        "distance_km": 2.2,
        "difficulty": "Easy to Moderate",
        "duration_hours": "2 - 2.5 Hours",
        "best_season": "October to February",
        "trail_type": "424 Stone Stairway & Rocky Escarpment",
        "coordinates": {"lat": 24.7820, "lng": 84.9850},
        "description": "Highest peak overlooking Gaya sacred city. Lord Buddha delivered the famous Fire Sermon (Adittapariyaya Sutta) to a thousand ascetics on this panoramic hill.",
        "trail_highlights": [
            "Natural stone cave fissure (Brahmayoni) with narrow passage",
            "360-degree vista of Falgu River, Vishnupad Temple, and distant Bodh Gaya stupa",
            "Ashokan and medieval epigraphical rock carvings"
        ],
        "gear_required": ["Comfortable walking shoes", "Drinking water", "Walking pole optional"]
    },
    {
        "id": "trek-dungeshwari-caves",
        "slug": "dungeshwari-pragbodhi-hill-trail",
        "name": "Pragbodhi (Dungeshwari) Hermit Ridge Trail",
        "district": "Gaya",
        "elevation_gain_m": 180,
        "summit_elevation_m": 260,
        "distance_km": 3.0,
        "difficulty": "Moderate",
        "duration_hours": "2.5 - 3 Hours",
        "best_season": "November to March",
        "trail_type": "Rocky Forest Path & Winding Hill Stairway",
        "coordinates": {"lat": 24.7430, "lng": 85.0410},
        "description": "Winds through rocky scrub forest up the Pragbodhi ridge to the sacred cave where Prince Siddhartha practiced 6 years of intense ascetic meditation before achieving enlightenment at Bodh Gaya.",
        "trail_highlights": [
            "Cave shrine enshrining golden emaciated Fasting Buddha image",
            "Tibetan prayer flags fluttering across the craggy mountain crest",
            "Serene meditation spots overlooking the Niranjana riverbed"
        ],
        "gear_required": ["Trail runners or trekking shoes", "Water bottle", "Modest temple clothing"]
    },
    {
        "id": "trek-rohtasgarh-canyon",
        "slug": "rohtasgarh-fort-plateau-trek",
        "name": "Rohtasgarh Plateau & Canyon Wilderness Expedition",
        "district": "Rohtas",
        "elevation_gain_m": 450,
        "summit_elevation_m": 500,
        "distance_km": 11.5,
        "difficulty": "Challenging / Full-Day Trek",
        "duration_hours": "6 - 7 Hours",
        "best_season": "October to March",
        "trail_type": "Steep Escarpment Ascent, Forest Trails & Canyon Plateau",
        "coordinates": {"lat": 24.6200, "lng": 83.9180},
        "description": "One of India's most dramatic hill fort treks. Rises 1,500 feet above the Sone River into a 28 sq. km plateau fortress containing medieval palaces, underground tunnels, and deep sandstone gorges.",
        "trail_highlights": [
            "Elephant Gate (Hathi Pol) and ancient fortified stone bastions",
            "Aina Mahal palace and Jama Masjid at the plateau summit",
            "Breathtaking 1,000-foot sheer drops overlooking Sone Valley"
        ],
        "gear_required": ["High-ankle trekking boots", "3L Hydration bladder", "Trail snacks", "Headlamp / Flashlight"]
    },
    {
        "id": "trek-tutla-bhawani-gorge",
        "slug": "tutla-bhawani-canyon-trek",
        "name": "Tutla Bhawani Waterfall Valley & Gorge Hike",
        "district": "Rohtas",
        "elevation_gain_m": 120,
        "summit_elevation_m": 180,
        "distance_km": 4.5,
        "difficulty": "Easy to Moderate",
        "duration_hours": "2.5 - 3 Hours",
        "best_season": "July to February (Monsoon for Waterfall)",
        "trail_type": "Canyon Riverbed, Hanging Suspension Bridge & Rock Steps",
        "coordinates": {"lat": 24.8950, "lng": 83.9820},
        "description": "Follows the green gorge of the Kachhuar river enclosed by soaring 200m red sandstone cliffs, leading over an eco-friendly suspension bridge to a thunderous waterfall and 8th-century Mahishasuramardini shrine.",
        "trail_highlights": [
            "Valley-spanning aerial suspension skybridge",
            "Crystal clear natural pool and cascading monsoon waterfall",
            "7th-century Nayaka Pratapadhavala rock inscription"
        ],
        "gear_required": ["Quick-dry apparel", "Water shoes or grippy sandals", "Waterproof drybag"]
    }
]

TREK_SAFETY_GUIDELINES = [
    {
        "principle": "Leave No Trace (Pristine Eco-Trails)",
        "protocol": "Carry back all plastic wrappers, bottles, and non-biodegradable waste. Refuse single-use plastics."
    },
    {
        "principle": "Hydration & Electrolyte Management",
        "protocol": "Carry minimum 2 liters of drinking water on hill treks. Plateau heat requires continuous hydration."
    },
    {
        "principle": "Respect Wildlife & Sacred Hill Sanctuaries",
        "protocol": "Stay on marked trails. Do not disturb wild monkeys or birds; refrain from loud acoustic noise in hermit caves."
    },
    {
        "principle": "Daylight Turnaround Time",
        "protocol": "Always initiate descents at least 90 minutes prior to sunset to ensure safe footing before darkness falls."
    }
]

def get_all_treks():
    """Return all cataloged eco-trails and trekking expeditions."""
    return ECO_TREKS_DB

def get_trek_by_slug(slug):
    """Retrieve trek by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for t in ECO_TREKS_DB:
        if t["slug"] == s or t["id"] == s:
            return t
    return None

def get_treks_by_district(district):
    """Filter treks by district."""
    if not district or district.lower() == 'all':
        return ECO_TREKS_DB
    d_clean = district.lower().strip()
    return [t for t in ECO_TREKS_DB if d_clean in t["district"].lower()]

def get_treks_by_difficulty(diff):
    """Filter treks by difficulty level."""
    if not diff or diff.lower() == 'all':
        return ECO_TREKS_DB
    df_clean = diff.lower().strip()
    return [t for t in ECO_TREKS_DB if df_clean in t["difficulty"].lower()]

def get_trekking_safety_guidelines():
    """Return wilderness trail safety principles."""
    return TREK_SAFETY_GUIDELINES

ECO_CAMPSITES_DB = [
    {
        "id": "camp-valmiki-sal-canopy",
        "name": "Valmiki Sal Forest Eco-Huts & Wilderness Camp",
        "district": "West Champaran",
        "near_trek": "Triveni Sangam & Tiger Trail",
        "tents_available": 12,
        "amenities": ["Solar Lighting", "Filtered Spring Water", "Campfire Circle", "Local Tharu Meals"],
        "permit_authority": "Valmiki Tiger Reserve Eco-Tourism Board",
        "nightly_rate_inr": 1400
    },
    {
        "id": "camp-rohtas-plateau-ridge",
        "name": "Rohtasgarh Plateau Escarpment Basecamp",
        "district": "Rohtas",
        "near_trek": "Rohtasgarh Plateau & Canyon Wilderness Expedition",
        "tents_available": 8,
        "amenities": ["Stargazing Deck", "Trek Guide Station", "Pack Lunches", "Emergency Radio"],
        "permit_authority": "Rohtas District Eco-Tourism Committee",
        "nightly_rate_inr": 1200
    }
]

def get_all_eco_campsites():
    """Return verified wilderness eco-campsites and tenting grounds."""
    return ECO_CAMPSITES_DB