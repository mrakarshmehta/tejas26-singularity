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
