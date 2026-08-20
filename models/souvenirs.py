"""
Bihar Authentic Geographical Indication (GI) Souvenirs & Artisan Crafts Model
Provides certified handicrafts, GI tags, artisan guild cooperatives,
fair-trade pricing benchmarks, and authenticity verification indicators.
"""

GI_SOUVENIRS_DB = [
    {
        "id": "souvenir-madhubani-tussar",
        "slug": "mithila-madhubani-tussar-scroll",
        "name": "Mithila Madhubani Handpainted Tussar Silk Scroll",
        "gi_tag_status": "GI Certified (Geographical Indication No. 105)",
        "district": "Madhubani",
        "artisan_cluster": "Jitwarpur & Ranti Master Artist Guilds",
        "craft_category": "Folk Painting & Handloom Textile",
        "materials": "Wild Tussar silk, natural organic mineral & botanical pigments (soot, turmeric, madder)",
        "price_range_inr": {"min": 1200, "max": 8500},
        "authenticity_seal": "Silk Mark India & Craftmark Certified",
        "icon": "🎨",
        "description": "Authentic hand-painted Mithila artwork executed with bamboo nibs and cotton rags. Features traditional Kohbar fertility motifs, Tree of Life, and cosmic Krishna Rasaleela compositions.",
        "ethical_impact": "100% of proceeds go directly to rural women artist cooperatives."
    },
    {
        "id": "souvenir-bhagalpur-silk",
        "slug": "bhagalpur-tussar-matka-shawl",
        "name": "Bhagalpur Pure Tussar & Matka Silk Shawl",
        "gi_tag_status": "GI Certified (Geographical Indication No. 125)",
        "district": "Bhagalpur",
        "artisan_cluster": "Nathnagar Silk Weavers Cooperative",
        "craft_category": "Natural Wild Silk Handloom Weaving",
        "materials": "100% Ahimsa / Peace Tussar silk yarn with natural lustrous gold sheen",
        "price_range_inr": {"min": 1800, "max": 6500},
        "authenticity_seal": "Handloom Mark & Silk Mark Certified",
        "icon": "🧣",
        "description": "Bhagalpur, the historic 'Silk City' of eastern India, produces rich textured wild silk known for exceptional breathability in summer and comforting warmth in winter.",
        "ethical_impact": "Supports generational master pit-loom weavers of Nathnagar and Champanagar."
    },
    {
        "id": "souvenir-sikki-golden-grass",
        "slug": "sikki-golden-grass-coasters-box",
        "name": "Sikki Golden Grass Royal Trinket Box & Coaster Set",
        "gi_tag_status": "GI Certified (Geographical Indication No. 107)",
        "district": "Madhubani",
        "artisan_cluster": "Rajnagar Women's Artisanal Guild",
        "craft_category": "Eco-Friendly Wild Grass Basketry",
        "materials": "Indigenous wild golden Sikki grass (Chrysopogon zizanioides) and Khar reed core",
        "price_range_inr": {"min": 450, "max": 2200},
        "authenticity_seal": "State Handicrafts Board Certified",
        "icon": "🌾",
        "description": "Hand-plaited from lustrous wild golden grass collected from riverbanks after monsoons. The natural metallic sheen never tarnishes with age, creating durable, biodegradable heirlooms.",
        "ethical_impact": "Zero carbon footprint; empowers over 2,000 rural women artisans."
    },
    {
        "id": "souvenir-tikuli-art-plate",
        "slug": "patna-tikuli-glass-enamel-platter",
        "name": "Patna Mauryan Tikuli Enamel Decorative Platter",
        "gi_tag_status": "GI Certified / UNESCO Endorsed Heritage Craft",
        "district": "Patna",
        "artisan_cluster": "Digha Tikuli Kala Kendra",
        "craft_category": "Fine Enamel & Gold-Foil Micro-Painting",
        "materials": "Hardboard base, multi-coat natural enamel lacquer, 24K gold foil lines",
        "price_range_inr": {"min": 650, "max": 3500},
        "authenticity_seal": "Upendra Maharathi Shilp Sansthan Seal",
        "icon": "✨",
        "description": "An 800-year-old Patna court craft originally created on glass bindis. Up to 15 layers of enamel are hand-polished to create a glass-like jewel sheen with intricate court dancer designs.",
        "ethical_impact": "Revived by master craftsman Padma Shri Ashok Kumar Biswas, sustaining urban artisan livelihoods."
    },
    {
        "id": "souvenir-patharkatti-stone",
        "slug": "gaya-patharkatti-black-stone-sculpture",
        "name": "Gaya Patharkatti Softstone Carved Buddha Miniature",
        "gi_tag_status": "State Heritage Craft Registry",
        "district": "Gaya",
        "artisan_cluster": "Patharkatti Village Sculptors Guild",
        "craft_category": "Traditional Stone Masonry & Sculpture",
        "materials": "Indigenous Kasauti / Chunar metamorphic black stone",
        "price_range_inr": {"min": 850, "max": 5000},
        "authenticity_seal": "Gaya Shilpi Sangh Guarantee",
        "icon": "🗿",
        "description": "Hand-chiseled by descendants of Rajasthani master stonemasons invited by Queen Ahilyabai Holkar in the 18th century to build the Vishnupad temple. Silky smooth dark stone finish.",
        "ethical_impact": "Preserves rare classical hand-chiseling techniques passed down across 8 generations."
    }
]

FAIR_TRADE_GUIDELINES = [
    {
        "title": "Look for Official Authenticity Seals",
        "detail": "Insist on Silk Mark for genuine Tussar, Handloom Mark for pit-loom weaves, and Craftmark for authentic handmade tribal artifacts."
    },
    {
        "title": "Direct Artisan Cooperative Sourcing",
        "detail": "Buy directly from artisan clusters (e.g. Jitwarpur village or Nathnagar weavers) to ensure full value reaches the creator."
    },
    {
        "title": "Respect Handcrafted Time & Natural Dyes",
        "detail": "Authentic Madhubani paintings on silk take 15 to 45 days of meticulous line drawing using organic pigments."
    }
]

def get_all_souvenirs():
    """Return all cataloged GI and heritage artisan souvenirs."""
    return GI_SOUVENIRS_DB

def get_souvenir_by_slug(slug):
    """Retrieve souvenir by slug or ID."""
    if not slug:
        return None
    s = slug.lower().strip()
    for item in GI_SOUVENIRS_DB:
        if item["slug"] == s or item["id"] == s:
            return item
    return None

def get_souvenirs_by_district(district):
    """Filter souvenirs by manufacturing district."""
    if not district or district.lower() == 'all':
        return GI_SOUVENIRS_DB
    d_clean = district.lower().strip()
    return [s for s in GI_SOUVENIRS_DB if d_clean in s["district"].lower()]

def get_souvenirs_by_category(cat):
    """Filter souvenirs by craft category."""
    if not cat or cat.lower() == 'all':
        return GI_SOUVENIRS_DB
    c_clean = cat.lower().strip()
    return [s for s in GI_SOUVENIRS_DB if c_clean in s["craft_category"].lower()]

def get_fair_trade_shopping_guidelines():
    """Return fair-trade ethical buying principles."""
    return FAIR_TRADE_GUIDELINES

ARTISAN_WORKSHOPS_DB = [
    {
        "id": "workshop-jitwarpur-kala-gram",
        "name": "Jitwarpur Mithila Painting Master Artisan Village",
        "district": "Madhubani",
        "craft": "Madhubani / Mithila Painting",
        "visiting_hours": "09:00 AM - 05:00 PM (Daily)",
        "activities": ["Live pigment grinding demonstrations", "Interactive brush & bamboo nib workshops", "Direct artist studio visits"],
        "cooperative_contact": "Jitwarpur Shilp Samiti / Gram Panchayat"
    },
    {
        "id": "workshop-nathnagar-silk-cluster",
        "name": "Nathnagar Pit-Loom Silk Weavers Guild",
        "district": "Bhagalpur",
        "craft": "Bhagalpuri Ahimsa Tussar Weaving",
        "visiting_hours": "10:00 AM - 04:30 PM (Closed Sundays)",
        "activities": ["Silk cocoon spinning demonstrations", "Pit-loom jacquard weaving observation", "Certified pure silk yarn testing"],
        "cooperative_contact": "Bhagalpur Silk Weavers Union, Nathnagar"
    }
]

def get_all_artisan_workshops():
    """Return verified artisan craft villages and workshop visit destinations."""
    return ARTISAN_WORKSHOPS_DB

GI_AUTHENTICITY_CHECKLIST = [
    {
        "craft_type": "Mithila / Madhubani Painting",
        "authentic_indicator": "Hand-drawn nib double-lines filled with organic natural pigments (soot black, lampblack, Palash orange). Slight natural variations across motifs.",
        "fake_warning_sign": "Pixelated machine digital prints on polyester with uniform synthetic chemical color fills."
    },
    {
        "craft_type": "Bhagalpuri Silk",
        "authentic_indicator": "Distinct textured coarse feel with rich natural golden-brown sheen. Carries official green Silk Mark India label with unique hologram.",
        "fake_warning_sign": "Overly slippery, static-generating synthetic rayon/polyester sold as 'pure tussar'."
    },
    {
        "craft_type": "Sikki Grass Craft",
        "authentic_indicator": "Natural sweet hay aroma, lustrous metallic golden hue that intensifies with age. Sturdy ribbed weave.",
        "fake_warning_sign": "Bleached plastic reeds dyed with synthetic spray paints that peel under moisture."
    }
]

def get_authenticity_checklist():
    """Return GI and handicraft authenticity verification checklist."""
    return GI_AUTHENTICITY_CHECKLIST