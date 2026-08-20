"""
HiddenYatra — Thematic Tourism Circuits & Heritage Trails Model
Provides curated multi-stop itineraries grouped by spiritual, cultural, ecological, and historical themes.
"""

BIHAR_THEMATIC_CIRCUITS = [
    {
        "id": 1,
        "slug": "buddhist-circuit",
        "title": "Enlightenment Trail (Buddhist Circuit)",
        "theme": "Spiritual & Heritage",
        "tagline": "Follow the footprints of Lord Buddha across ancient Magadha",
        "description": "A transformative journey connecting Bodh Gaya (where Buddha attained enlightenment), Nalanda (ancient university), Rajgir (Gridhakuta Hill & Vulture's Peak), and Vaishali (site of the second Buddhist council).",
        "total_distance_km": 340,
        "duration_days": 4,
        "best_season": "October to March",
        "icon": "☸️",
        "accent_color": "#d97706",
        "stops": [
            {"order": 1, "place_name": "Mahabodhi Temple", "district": "Gaya", "lat": 24.6961, "lng": 84.9913, "days": 1, "highlight": "Venerable Bodhi Tree & Vajrasana"},
            {"order": 2, "place_name": "Dungeshwari Cave", "district": "Gaya", "lat": 24.7833, "lng": 85.0500, "days": 1, "highlight": "Pre-enlightenment meditation site"},
            {"order": 3, "place_name": "Vulture Peak & Peace Pagoda", "district": "Nalanda (Rajgir)", "lat": 25.0134, "lng": 85.4194, "days": 2, "highlight": "Vishva Shanti Stupa & Lotus Sutra sermons"},
            {"order": 4, "place_name": "Ancient Nalanda Ruins", "district": "Nalanda", "lat": 25.1357, "lng": 85.4450, "days": 3, "highlight": "UNESCO World Heritage ancient university"},
            {"order": 5, "place_name": "Ashoka Pillar & Relic Stupa", "district": "Vaishali", "lat": 25.9904, "lng": 85.1278, "days": 4, "highlight": "Last sermon site of Lord Buddha"}
        ]
    },
    {
        "id": 2,
        "slug": "jain-circuit",
        "title": "Tirthankara Trail (Jain Circuit)",
        "theme": "Spiritual & Historical",
        "tagline": "Sacred footsteps of Lord Mahavira across Pavapuri, Champapuri & Mandar",
        "description": "Discover the profound Jain pilgrimage route honoring Lord Mahavira, the 24th Tirthankara, including Jal Mandir where he achieved Nirvana.",
        "total_distance_km": 290,
        "duration_days": 3,
        "best_season": "November to February",
        "icon": "🖐️",
        "accent_color": "#0284c7",
        "stops": [
            {"order": 1, "place_name": "Jal Mandir Pavapuri", "district": "Nalanda", "lat": 25.0933, "lng": 85.5264, "days": 1, "highlight": "White marble temple floating on lotus pond"},
            {"order": 2, "place_name": "Kundalpur Digambar Teerth", "district": "Nalanda", "lat": 25.1480, "lng": 85.4620, "days": 2, "highlight": "Birthplace temple of Lord Mahavira"},
            {"order": 3, "place_name": "Mandar Hill", "district": "Banka", "lat": 24.8389, "lng": 87.0267, "days": 3, "highlight": "Site of Lord Vasupujya's Nirvana & Samudra Manthan legend"}
        ]
    },
    {
        "id": 3,
        "slug": "eco-wildlife-circuit",
        "title": "Nature & Wildlife Circuit",
        "theme": "Eco-Tourism & Nature",
        "tagline": "Pristine waterfalls, tiger reserves, and Gangetic dolphin sanctuaries",
        "description": "Experience Bihar's untamed natural majesty from the sub-Himalayan Terai forests of Valmiki National Park to the scenic waterfalls of Kaimur and Kakolat.",
        "total_distance_km": 520,
        "duration_days": 5,
        "best_season": "November to April",
        "icon": "🐯",
        "accent_color": "#059669",
        "stops": [
            {"order": 1, "place_name": "Valmiki National Park", "district": "West Champaran", "lat": 27.2798, "lng": 84.1834, "days": 2, "highlight": "Tiger safari, Gandak riverbanks & Tharu tribal culture"},
            {"order": 2, "place_name": "Vikramshila Dolphin Sanctuary", "district": "Bhagalpur", "lat": 25.2933, "lng": 87.0360, "days": 3, "highlight": "India's only Gangetic river dolphin sanctuary"},
            {"order": 3, "place_name": "Kakolat Waterfall", "district": "Nawada", "lat": 24.7186, "lng": 85.6025, "days": 4, "highlight": "Cascading natural plunge pool in forested gorge"},
            {"order": 4, "place_name": "Telhar Kund & Kaimur Hills", "district": "Kaimur", "lat": 24.9667, "lng": 83.6167, "days": 5, "highlight": "Deep canyon waterfall and prehistoric rock art"}
        ]
    },
    {
        "id": 4,
        "slug": "gandhian-satyagraha-circuit",
        "title": "Satyagraha Trail (Gandhi Circuit)",
        "theme": "Freedom Struggle & History",
        "tagline": "Where Mahatma Gandhi launched India's freedom revolution in 1917",
        "description": "Trace the historic footsteps of the Champaran Satyagraha of 1917, the first non-violent civil disobedience movement that transformed India's independence struggle.",
        "total_distance_km": 210,
        "duration_days": 2,
        "best_season": "October to March",
        "icon": "🕊️",
        "accent_color": "#475569",
        "stops": [
            {"order": 1, "place_name": "Bhitiharwa Ashram", "district": "West Champaran", "lat": 27.2100, "lng": 84.4500, "days": 1, "highlight": "Original school and cottage established by Gandhiji"},
            {"order": 2, "place_name": "Gandhi Smarak Motihari", "district": "East Champaran", "lat": 26.6500, "lng": 84.9167, "days": 1, "highlight": "Monument marking Gandhi's historic court appearance"},
            {"order": 3, "place_name": "Sadaqat Ashram Patna", "district": "Patna", "lat": 25.6250, "lng": 85.0950, "days": 2, "highlight": "Headquarters of freedom fighters & Dr. Rajendra Prasad"}
        ]
    },
    {
        "id": 5,
        "slug": "sufi-spiritual-circuit",
        "title": "Sufi & Interfaith Harmony Trail",
        "theme": "Spiritual & Interfaith",
        "tagline": "Sacred Khanqahs, historic Dargahs, and centuries of syncretic harmony",
        "description": "Journey through mystical Sufi shrines that have fostered peace, poetry, and communal brotherhood across Bihar for nearly a millennium.",
        "total_distance_km": 260,
        "duration_days": 3,
        "best_season": "Year-round (Best Oct-Feb)",
        "icon": "🕌",
        "accent_color": "#0d9488",
        "stops": [
            {"order": 1, "place_name": "Maner Sharif", "district": "Patna", "lat": 25.6447, "lng": 84.8775, "days": 1, "highlight": "Chhoti Dargah — finest Mughal architecture in Bihar"},
            {"order": 2, "place_name": "Bihar Sharif Dargahs", "district": "Nalanda", "lat": 25.1982, "lng": 85.5186, "days": 2, "highlight": "Tomb of Makhdoom Sharfuddin Yahya Maneri"},
            {"order": 3, "place_name": "Khanqah Mujibia Phulwari Sharif", "district": "Patna", "lat": 25.5786, "lng": 85.0744, "days": 3, "highlight": "Historic 18th-century Sufi library and spiritual seat"}
        ]
    }
]


def get_all_circuits():
    """Return all curated thematic circuits with basic summary."""
    return BIHAR_THEMATIC_CIRCUITS


def get_circuit_by_slug(slug):
    """Retrieve a specific circuit definition by its URL slug."""
    if not slug:
        return None
    slug_clean = slug.strip().lower()
    for c in BIHAR_THEMATIC_CIRCUITS:
        if c['slug'] == slug_clean:
            return c
    return None


def get_circuit_places(slug):
    """Return the ordered list of stop locations for a circuit."""
    circuit = get_circuit_by_slug(slug)
    if not circuit:
        return []
    return circuit.get('stops', [])
