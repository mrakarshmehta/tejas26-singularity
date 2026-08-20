"""
HiddenYatra — Sustainable Tourism & Eco-Heritage Principles Model
Promotes zero-waste travel, respect for living sacred heritage, and direct community support.
"""

RESPONSIBLE_TRAVEL_PILLARS = [
    {
        "id": 1,
        "pillar_name": "Zero-Trace Heritage Preservation",
        "icon": "🌿",
        "description": "Never deface ancient stone masonry, brick ruins, or stupa terraces. Carry all plastic waste back to municipal collection bins.",
        "action_items": [
            "Do not engrave names or scratch ancient stucco carvings at Nalanda or Vikramshila",
            "Refuse single-use plastic bottles; use refillable stainless steel bottles at verified RO stations",
            "Stay strictly on designated boardwalks and stone pathways"
        ]
    },
    {
        "id": 2,
        "pillar_name": "Sanctity of Living Ritual Spaces",
        "icon": "🪔",
        "description": "Respect active prayer ceremonies, meditation hours, and sacred bathing rituals along holy river ghats and monastic shrines.",
        "action_items": [
            "Dress modestly when entering temple sanctums, stupa parikramas, and mosques",
            "Ask explicit permission before photographing meditating monks or women performing Chhath arghya",
            "Maintain silence in caves (Barabar Caves) and monastic meditation halls"
        ]
    },
    {
        "id": 3,
        "pillar_name": "Direct Local Economy Support",
        "icon": "🤝",
        "description": "Ensure your travel spending directly benefits local village artisans, boatmen, registered guides, and family-run dhabas.",
        "action_items": [
            "Purchase certified GI handicrafts directly from weaver clusters in Jitwarpur and Champanagar",
            "Hire local certified heritage guides at ASI monuments",
            "Savor authentic regional cuisine like Litti Chokha at local family-owned eateries"
        ]
    }
]


def get_responsible_travel_code():
    """Return all eco-heritage preservation pillars and traveler guidelines."""
    return RESPONSIBLE_TRAVEL_PILLARS


def validate_pledge_submission(traveler_name, email, state_origin):
    """Validate traveler pledge form input."""
    if not traveler_name or len(traveler_name.strip()) < 2:
        return False, "Name must be at least 2 characters long."
    if not email or "@" not in email or "." not in email:
        return False, "Please provide a valid email address."
    return True, "Valid"
