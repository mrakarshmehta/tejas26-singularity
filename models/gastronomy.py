"""
Bihar Culinary Heritage & Gastronomy Trails Model
Provides authentic regional dishes, GI-tagged sweets, dietary classifications,
historical origins, and verified heritage sweetmaker/eatery locations.
"""

GASTRONOMY_DISHES_DB = [
    {
        "id": "dish-litti-chokha",
        "slug": "litti-chokha",
        "name": "Bihari Litti Chokha",
        "hindi_name": "लिट्टी चोखा",
        "category": "Signature Heritage Meal",
        "origin_district": "Bhojpur & Magadha",
        "gi_status": False,
        "dietary_tags": ["Vegetarian", "High-Fiber", "High-Protein"],
        "taste_profile": "Smoky, Earthy, Savory & Ghee-Infused",
        "icon": "🥟",
        "description": "The quintessential dish of Bihar consisting of roasted whole wheat dough balls stuffed with spiced roasted gram flour (sattu), aromatic ajwain, kalonji, mustard oil, and green chillies, dipped generously in desi ghee and served with baingan-tamatar chokha.",
        "cultural_backstory": "Originating in ancient Magadha as an energy-dense warrior food for Mauryan soldiers and later 1857 revolutionary fighters under Veer Kunwar Singh due to its long shelf life without spoiling.",
        "key_ingredients": ["Roasted Gram Flour (Sattu)", "Whole Wheat", "Mustard Oil", "Ajwain & Kalonji", "Smoked Eggplant", "Cow Desi Ghee"],
        "iconic_eateries": [
            {"name": "Bihari Litti Hub", "location": "Maurya Lok Complex, Patna", "district": "Patna"},
            {"name": "DK Litti Corner", "location": "Near Patna Junction, Patna", "district": "Patna"},
            {"name": "Bodh Gaya Local Heritage Kitchens", "location": "Temple Road, Bodh Gaya", "district": "Gaya"}
        ]
    },
    {
        "id": "dish-silao-khaja",
        "slug": "silao-khaja",
        "name": "Silao Khaja (GI Certified)",
        "hindi_name": "सिलाव खाजा",
        "category": "Certified GI Sweetmeat",
        "origin_district": "Nalanda",
        "gi_status": True,
        "gi_year": 2018,
        "dietary_tags": ["Vegetarian", "Crispy Delicacy"],
        "taste_profile": "Multi-Layered, Ultra-Crisp, Mildly Sweet",
        "icon": "🥠",
        "description": "Famous multi-layered sweet pastry made of 52 wafer-thin crisp sheets of wheat flour and pure ghee, lightly dipped in sugar syrup. The local alkaline water of Silao gives it its signature crispness.",
        "cultural_backstory": "Legend records that Lord Buddha was offered Khaja by local villagers as he traveled between Rajgir and Nalanda. Mentioned in Buddhist texts and patronized by the Mauryan and Gupta emperors.",
        "key_ingredients": ["Refined Wheat Flour (Maida)", "Desi Ghee", "Sugar Syrup", "Local Silao Well Water"],
        "iconic_eateries": [
            {"name": "Kailash Sah Khaja Bhandar (Original 1912)", "location": "Main Bazaar, Silao", "district": "Nalanda"},
            {"name": "Mithila Khaja Mahal", "location": "Near Nalanda University Gate", "district": "Nalanda"}
        ]
    },
    {
        "id": "dish-gaya-tilkut",
        "slug": "gaya-tilkut",
        "name": "Gaya Tilkut & Anarsa",
        "hindi_name": "गया तिलकुट",
        "category": "Winter Heritage Confection",
        "origin_district": "Gaya",
        "gi_status": False,
        "dietary_tags": ["Vegan", "Gluten-Free", "High-Calcium", "Winter Special"],
        "taste_profile": "Nutty, Crumbly, Sweet & Caramelized",
        "icon": "🍪",
        "description": "Traditional sweet made by pounding roasted sesame seeds (til) with hot molten sugarcane jaggery (gur) or sugar in stone mortars using heavy wooden mallets until it forms an airy, melting texture.",
        "cultural_backstory": "A sacred offering during the winter festival of Makar Sankranti. The narrow lanes of Ramna and Tekari Road in Gaya have been hammering Tilkut for over two centuries.",
        "key_ingredients": ["White Sesame Seeds (Til)", "Sugarcane Jaggery (Gur)", "Cardamom"],
        "iconic_eateries": [
            {"name": "Sri Ram Tilkut Bhandar", "location": "Ramna Road, Gaya", "district": "Gaya"},
            {"name": "Pramod Tilkut & Sweets", "location": "Tekari Road, Gaya", "district": "Gaya"}
        ]
    },
    {
        "id": "dish-maner-laddu",
        "slug": "maner-laddu",
        "name": "Maner Ka Laddu",
        "hindi_name": "मनेर का लड्डू",
        "category": "Heritage Sweetmeat",
        "origin_district": "Patna",
        "gi_status": False,
        "dietary_tags": ["Vegetarian"],
        "taste_profile": "Melt-in-Mouth, Cardamom & Ghee Rich",
        "icon": "🟡",
        "description": "Legendary bright golden Motichoor Laddu crafted with tiny droplet pearls of gram flour fried in pure cow ghee and bound with fragrant saffron sugar syrup and water from the Sone River.",
        "cultural_backstory": "Originated near the Sufi shrine of Maner Sharif in Patna. Mughal chroniclers praised the laddu for its delicate melt-in-mouth texture attributed to the mineral qualities of Sone River water.",
        "key_ingredients": ["Besan (Gram Flour)", "Pure Cow Ghee", "Saffron (Kesar)", "Pistachios & Melon Seeds"],
        "iconic_eateries": [
            {"name": "Original Maner Sweet House", "location": "Near Badi Dargah, Maner", "district": "Patna"},
            {"name": "Harilal's Sweets", "location": "Boring Road, Patna", "district": "Patna"}
        ]
    },
    {
        "id": "dish-mithila-makhana-kheer",
        "slug": "mithila-makhana-kheer",
        "name": "Mithila Makhana Kheer (Foxnut Pudding)",
        "hindi_name": "मिथिला मखाना खीर",
        "category": "Royal Dessert & Superfood",
        "origin_district": "Darbhanga & Madhubani",
        "gi_status": True,
        "gi_year": 2022,
        "dietary_tags": ["Vegetarian", "Gluten-Free", "Low-Glycemic", "Superfood"],
        "taste_profile": "Creamy, Saffron-Infused, Mild & Nutty",
        "icon": "🥣",
        "description": "Rich royal pudding prepared by lightly roasting GI-tagged Mithila Makhana (gorgon nuts) in ghee, then simmering in full-cream milk with green cardamom, saffron strands, and crushed almonds.",
        "cultural_backstory": "Makhana is one of the three auspicious emblems of Mithila culture (Paan, Maachh, and Makhaan). Revered as sacred food offering (Naivedyam) during wedding rituals and Kojagara festival.",
        "key_ingredients": ["Mithila Foxnuts (Makhana)", "Full Cream Milk", "Saffron", "Cardamom", "Almonds & Cashews"],
        "iconic_eateries": [
            {"name": "Mithilanchal Heritage Foods", "location": "Tower Chowk, Darbhanga", "district": "Darbhanga"},
            {"name": "Madhubani Royal Kitchens", "location": "Station Road, Madhubani", "district": "Madhubani"}
        ]
    },
    {
        "id": "dish-sattu-sherbet",
        "slug": "bihari-sattu-sherbet",
        "name": "Bihari Sattu Namkeen Sherbet",
        "hindi_name": "सत्तू का शरबत",
        "category": "Refreshing Traditional Elixir",
        "origin_district": "All Bihar",
        "gi_status": False,
        "dietary_tags": ["Vegan", "Gluten-Free", "High-Protein", "Natural Probiotic"],
        "taste_profile": "Zesty, Tangy, Cooling & Roasted Cumin",
        "icon": "🥤",
        "description": "Nutrient-dense natural cooler made of roasted chickpea and barley flour whisked with chilled water, roasted cumin powder, black salt, chopped mint, green chillies, onions, and freshly squeezed lemon juice.",
        "cultural_backstory": "Known as the indigenous super-drink of farmers and travelers throughout the blazing summer months of Bihar, offering instant hydration, high fiber, and gut-friendly cooling properties.",
        "key_ingredients": ["Roasted Chana Sattu", "Black Salt (Kala Namak)", "Roasted Cumin", "Lemon Juice", "Fresh Mint"],
        "iconic_eateries": [
            {"name": "Gandhi Maidan Sattu Kiosks", "location": "Gandhi Maidan, Patna", "district": "Patna"},
            {"name": "Patna City Heritage Stalls", "location": "Ashok Rajpath, Patna", "district": "Patna"}
        ]
    }
]

CULINARY_TRAILS = [
    {
        "id": "trail-magadha-sweets",
        "title": "Grand Magadha Sweetmeat & Savory Trail",
        "region": "Patna - Maner - Nalanda - Gaya",
        "duration_days": 2,
        "dishes_included": ["Litti Chokha", "Maner Ka Laddu", "Silao Khaja", "Gaya Tilkut"],
        "highlights": "Explore 2,000-year-old culinary traditions from the banks of the Sone River to the holy lanes of Ramna."
    },
    {
        "id": "trail-mithila-royal",
        "title": "Mithilanchal Royal Flavors & Makhana Trail",
        "region": "Darbhanga - Madhubani",
        "duration_days": 2,
        "dishes_included": ["Mithila Makhana Kheer", "Maachh Bhaat", "Tilkut", "Anarsa"],
        "highlights": "Savor authentic lotus-seed puddings and sweet delicacies of the ancient Videha kingdom."
    }
]

def get_all_dishes():
    """Return all cataloged traditional Bihar dishes and delicacies."""
    return GASTRONOMY_DISHES_DB

def get_dish_by_slug(slug):
    """Retrieve dish details by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for d in GASTRONOMY_DISHES_DB:
        if d["slug"] == s or d["id"] == s:
            return d
    return None

def get_dishes_by_district(district):
    """Filter dishes by origin district."""
    if not district or district.lower() == 'all':
        return GASTRONOMY_DISHES_DB
    d_clean = district.lower().strip()
    return [d for d in GASTRONOMY_DISHES_DB if d_clean in d["origin_district"].lower() or d["origin_district"] == "All Bihar"]

def get_dishes_by_dietary(tag):
    """Filter dishes by dietary preferences (e.g. Vegan, Gluten-Free)."""
    if not tag or tag.lower() == 'all':
        return GASTRONOMY_DISHES_DB
    t_clean = tag.lower().strip()
    return [d for d in GASTRONOMY_DISHES_DB if any(t_clean in dt.lower() for dt in d.get("dietary_tags", []))]

def get_gi_tagged_dishes():
    """Return only GI-certified food items."""
    return [d for d in GASTRONOMY_DISHES_DB if d.get("gi_status")]

def get_culinary_trails():
    """Return curated regional gastronomy trail itineraries."""
    return CULINARY_TRAILS