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