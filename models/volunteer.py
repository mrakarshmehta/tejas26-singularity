"""
Rural Immersion & Cultural Volunteerism Program Model
Provides community-based rural tourism initiatives, artisan apprenticeships,
ecological farming exchanges, and volunteer application matching.
"""

VOLUNTEER_PROGRAMS_DB = [
    {
        "id": "prog-madhubani-art-residency",
        "slug": "madhubani-art-guild-residency",
        "title": "Mithila Folk Art Guild Apprenticeship & Documentation",
        "village": "Jitwarpur & Ranti",
        "district": "Madhubani",
        "category": "Artisan Guild Apprenticeship",
        "duration_weeks": 2,
        "stipend_or_board": "Village Homestay & Authentic Maithil Meals Included",
        "skills_needed": ["Digital Photography", "Social Media Archiving", "Art History Interest", "Basic Hindi/English"],
        "impact_focus": "Preserving indigenous Kohbar & Aripan folklore motifs and assisting female artisan self-help groups with digital cataloging.",
        "tagline": "Live with National Award-winning Mithila painters and learn ancient natural pigment techniques.",
        "description": "Volunteers live with traditional artisan families in Jitwarpur. You will participate in preparing natural mineral and botanical dyes from marigold, turmeric, and lamp soot, while helping master artists photograph and catalog their collections for fair-trade markets."
    },
    {
        "id": "prog-organic-makhana-harvest",
        "slug": "organic-makhana-wetland-exchange",
        "title": "Mithilanchal Organic Makhana Wetland Farming Exchange",
        "village": "Manigachhi & Biraul",
        "district": "Darbhanga",
        "category": "Sustainable Agriculture",
        "duration_weeks": 1,
        "stipend_or_board": "Farmhouse Stay & Organic Meals Included",
        "skills_needed": ["Outdoor Physical Fitness", "Agricultural Interest", "Community Interaction"],
        "impact_focus": "Supporting local aquatic farming collectives in pesticide-free wetland pond management and value-added packaging.",
        "tagline": "Wade into tranquil village lotus ponds and discover the sustainable cycle of GI-certified foxnut harvesting.",
        "description": "An authentic agro-tourism immersion where participants work alongside third-generation Makhana harvesters, learning how the spiny gorgon water lily pods are gathered from pond beds, sun-dried, and hand-popped over wood fires."
    },
    {
        "id": "prog-nalanda-heritage-docent",
        "slug": "nalanda-heritage-docent-program",
        "title": "Ancient Nalanda Heritage Docent & Youth Ambassador",
        "village": "Bargaon & Pawapuri",
        "district": "Nalanda",
        "category": "Heritage Conservation & Education",
        "duration_weeks": 3,
        "stipend_or_board": "Heritage Guesthouse Board & Local Transport Allowance",
        "skills_needed": ["Public Speaking", "History/Archaeology Knowledge", "English & Hindi Fluency"],
        "impact_focus": "Training local rural youth as certified heritage guides and conducting interactive history sessions for visiting rural school groups.",
        "tagline": "Help bridge 1,500 years of monastic history for the next generation of travelers.",
        "description": "Stationed near the UNESCO World Heritage Nalanda ruins and Pawapuri, volunteers collaborate with local heritage trusts to develop child-friendly storytelling walks, oral history recordings, and eco-cleanliness drives around ancient monument boundaries."
    },
    {
        "id": "prog-tharu-tribal-homestay",
        "slug": "tharu-tribal-eco-village-exchange",
        "title": "Tharu Indigenous Eco-Village & Forest Lore Immersion",
        "village": "Harnatanr & Naurangia",
        "district": "West Champaran",
        "category": "Indigenous Cultural Immersion",
        "duration_weeks": 2,
        "stipend_or_board": "Tharu Traditional Thatch Homestay & Forest Food",
        "skills_needed": ["Eco-Tourism Interest", "Storytelling", "Respect for Tribal Customs"],
        "impact_focus": "Empowering Tharu community-based eco-tourism lodges and documenting indigenous ethno-botanical herbal knowledge.",
        "tagline": "Immerse yourself in the eco-friendly lifestyle of the guardians of the Valmiki forest canopy.",
        "description": "Live inside eco-friendly clay and grass huts built by the indigenous Tharu community. Learn traditional bamboo craftsmanship, assist in community nature guiding, and document traditional songs that celebrate the coexistence between humans and the Royal Bengal Tiger."
    }
]