"""
HiddenYatra — Traditional Handicrafts & Geographical Indication (GI) Tags Model
Provides authentic documentation for Bihar's GI-tagged folk arts, silk weaving, and stone crafts.
"""

BIHAR_GI_CRAFTS = [
    {
        "id": 1,
        "slug": "madhubani-mithila-painting",
        "name": "Madhubani (Mithila) Painting",
        "type": "GI Tagged Folk Art",
        "gi_status": "Registered GI (GI Application #1)",
        "origin_district": "Madhubani",
        "region": "Mithila Region",
        "icon": "🎨",
        "tagline": "Centuries-old folk art painted with natural twigs, fingers, and natural mineral dyes",
        "description": "Originating in the Mithila region, Madhubani art features distinctive geometric patterns depicting Hindu deities, cosmic harmony, flora, and weddings. Painted with natural pigments derived from turmeric, indigo, and marigold.",
        "prominent_villages": ["Ranti", "Jitwarpur", "Rasidpur"],
        "materials": "Handmade Lokta/cotton paper, cow dung wash, natural plant and mineral pigments."
    },
    {
        "id": 2,
        "slug": "bhagalpuri-tussar-silk",
        "name": "Bhagalpuri (Tussar) Silk",
        "type": "GI Tagged Handloom Textile",
        "gi_status": "Registered GI",
        "origin_district": "Bhagalpur",
        "region": "Silk City (Anga Region)",
        "icon": "🧵",
        "tagline": "Known globally as the Queen of Wild Silks with a rich, natural golden sheen",
        "description": "Woven for over a century along the banks of the Ganges, Bhagalpuri Tussar silk is renowned for its organic texture, breathability, and eco-friendly reeling process.",
        "prominent_villages": ["Champanagar", "Nathnagar", "Pirpainti"],
        "materials": "Wild Antheraea mylitta silkworm cocoons, hand-operated pit looms."
    },
    {
        "id": 3,
        "slug": "sikki-grass-craft",
        "name": "Sikki Grass Craft of Mithila",
        "type": "GI Tagged Natural Fiber Craft",
        "gi_status": "Registered GI",
        "origin_district": "Madhubani & Sitamarhi",
        "region": "North Bihar",
        "icon": "🌾",
        "tagline": "Golden grass woven into intricate wedding baskets, boxes, and divine figurines",
        "description": "Sikki is a golden-stemmed reed indigenous to the riverbanks of North Bihar. Artisans dry and weave it into lightweight, eco-friendly storage boxes (Pauti) and folk ornaments.",
        "prominent_villages": ["Ranti", "Rajnagar"],
        "materials": "Indigenous golden Sikki reed, natural vegetable dyes."
    },
    {
        "id": 4,
        "slug": "manjusha-art",
        "name": "Manjusha (Angika) Art",
        "type": "Heritage Folk Art",
        "gi_status": "Registered GI (Anga Region)",
        "origin_district": "Bhagalpur",
        "region": "Anga Region",
        "icon": "🐍",
        "tagline": "Scroll painting depicting the folklore of Bihula-Bishahari with three primary colors",
        "description": "Manjusha art is a sequential narrative scroll art rendered strictly in green, pink, and yellow. It recounts the epic tale of Bihula's devotion to save her husband from snake god Mansa.",
        "prominent_villages": ["Champanagar", "Sabour"],
        "materials": "Bamboo boxes (Manjusha), handmade paper, ink pens."
    },
    {
        "id": 5,
        "slug": "sujini-embroidery",
        "name": "Sujini Kantha Embroidery",
        "type": "GI Tagged Textile Craft",
        "gi_status": "Registered GI",
        "origin_district": "Muzaffarpur",
        "region": "Tirhut Region",
        "icon": "🪡",
        "tagline": "Quilted narrative embroidery depicting women empowerment and daily village tales",
        "description": "Sujini is a traditional quilting technique where layers of old cotton fabric are sewn together with fine running stitches depicting social themes, nature, and folklore.",
        "prominent_villages": ["Bhitiharwa", "Muzaffarpur Rural"],
        "materials": "Organic cotton fabric, colorful silk embroidery threads."
    }
]


def get_all_crafts():
    """Return all documented traditional crafts and GI arts."""
    return BIHAR_GI_CRAFTS


def get_craft_by_slug(slug):
    """Retrieve craft details by URL slug."""
    if not slug:
        return None
    slug_clean = slug.strip().lower()
    for c in BIHAR_GI_CRAFTS:
        if c['slug'] == slug_clean:
            return c
    return None


ARTISAN_CENTERS_DB = [
    {
        "id": 1,
        "center_name": "Mithila Kalashilp Artisan Co-Op",
        "craft_slug": "madhubani-mithila-painting",
        "district": "Madhubani",
        "location": "Jitwarpur Village",
        "lat": 26.3540,
        "lng": 86.0820,
        "master_artisans_count": 45,
        "accepts_visitors": True,
        "contact_phone": "+91-6276-224100",
        "experience": "Live wall mural workshops & authentic signed painting purchases direct from National Awardees."
    },
    {
        "id": 2,
        "center_name": "Anga Handloom Silk Weavers Guild",
        "craft_slug": "bhagalpuri-tussar-silk",
        "district": "Bhagalpur",
        "location": "Champanagar Weavers Colony",
        "lat": 25.2425,
        "lng": 86.9842,
        "master_artisans_count": 120,
        "accepts_visitors": True,
        "contact_phone": "+91-6412-421500",
        "experience": "Watch live cocoon boiling, silk thread spinning, and wooden pit loom weaving."
    },
    {
        "id": 3,
        "center_name": "Mahila Vikas Sikki Grass Producers",
        "craft_slug": "sikki-grass-craft",
        "district": "Madhubani",
        "location": "Ranti Village",
        "lat": 26.3600,
        "lng": 86.0900,
        "master_artisans_count": 30,
        "accepts_visitors": True,
        "contact_phone": "+91-6276-225588",
        "experience": "Participate in half-day grass dyeing and box weaving masterclasses."
    }
]


def get_artisan_centers_for_craft(craft_slug):
    """Return artisan centers and workshops for a given craft slug."""
    if not craft_slug:
        return ARTISAN_CENTERS_DB
    slug_clean = craft_slug.strip().lower()
    return [c for c in ARTISAN_CENTERS_DB if c['craft_slug'] == slug_clean]


def get_crafts_by_district(district_name):
    """Return traditional crafts originating from a given district."""
    if not district_name:
        return BIHAR_GI_CRAFTS
    d_clean = district_name.strip().lower()
    return [
        c for c in BIHAR_GI_CRAFTS
        if d_clean in c['origin_district'].lower() or d_clean in c['region'].lower()
    ]
