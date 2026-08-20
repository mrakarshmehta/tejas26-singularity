"""
Bihar Multi-Currency Trip Budget Planner & Cost Estimator Model
Provides multi-tier travel cost estimations (Backpacker, Heritage Explorer, Luxury),
itemized daily expense breakdowns, and real-time currency conversion indices.
"""

CURRENCY_RATES_DB = {
    "INR": {"symbol": "₹", "rate_to_inr": 1.0, "name": "Indian Rupee"},
    "USD": {"symbol": "$", "rate_to_inr": 86.50, "name": "US Dollar"},
    "EUR": {"symbol": "€", "rate_to_inr": 92.00, "name": "Euro"},
    "GBP": {"symbol": "£", "rate_to_inr": 109.50, "name": "British Pound"},
    "JPY": {"symbol": "¥", "rate_to_inr": 0.58, "name": "Japanese Yen"},
    "AUD": {"symbol": "A$", "rate_to_inr": 56.20, "name": "Australian Dollar"},
    "SGD": {"symbol": "S$", "rate_to_inr": 64.80, "name": "Singapore Dollar"}
}

TRAVEL_TIERS_DB = {
    "backpacker": {
        "tier_name": "Backpacker / Budget Explorer",
        "daily_rate_inr": 1600,
        "description": "Ideal for solo travelers, backpackers, and cultural researchers staying in heritage homestays and dharamshalas.",
        "breakdown_inr": {
            "stay": 700,
            "food": 450,
            "local_transit": 250,
            "entry_permits": 100,
            "misc": 100
        },
        "stay_type": "Heritage Dharamshala / Eco-Homestay / Hostel",
        "transit_type": "Shared Auto-rickshaws, E-Rickshaws & Local Trains",
        "dining_type": "Traditional Dhaba Thalis, Litti Chokha & Sattu Sherbet"
    },
    "heritage": {
        "tier_name": "Comfort Heritage Explorer",
        "daily_rate_inr": 4500,
        "description": "Recommended for couples, families, and cultural tourists seeking 3-star boutique heritage hotels and private auto/cab hires.",
        "breakdown_inr": {
            "stay": 2400,
            "food": 1100,
            "local_transit": 600,
            "entry_permits": 250,
            "guide_share": 150
        },
        "stay_type": "Boutique Heritage Hotel / Certified Guest House",
        "transit_type": "Private AC Cab & Dedicated Auto Hires",
        "dining_type": "Heritage Hotel Dining, Mithila Sweets & Regional Thalis"
    },
    "luxury": {
        "tier_name": "Luxury Maharaja & Eco-Resort",
        "daily_rate_inr": 12500,
        "description": "Premium experience with 5-star palace hotels, private licensed historian guides, and AC SUV transfers.",
        "breakdown_inr": {
            "stay": 7500,
            "food": 2500,
            "local_transit": 1500,
            "entry_permits": 500,
            "private_guide": 500
        },
        "stay_type": "5-Star Luxury Palace / Valmiki Forest Luxury Resort",
        "transit_type": "Private Chauffeur-Driven AC SUV / Luxury Innova",
        "dining_type": "Fine Dining Bihari Royal Cuisine & Gourmet Experiences"
    }
}