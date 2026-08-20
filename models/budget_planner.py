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

def get_all_currencies():
    """Return supported currencies and conversion rates."""
    return CURRENCY_RATES_DB

def get_all_travel_tiers():
    """Return all budget tiers and itemized category breakdown templates."""
    return TRAVEL_TIERS_DB

def convert_currency(amount_inr, target_currency="INR"):
    """Convert an amount in INR to target currency."""
    curr = target_currency.upper().strip() if target_currency else "INR"
    if curr not in CURRENCY_RATES_DB:
        curr = "INR"

    rate = CURRENCY_RATES_DB[curr]["rate_to_inr"]
    converted_value = round(amount_inr / rate, 2)
    return {
        "currency": curr,
        "symbol": CURRENCY_RATES_DB[curr]["symbol"],
        "amount": converted_value,
        "amount_inr": amount_inr
    }

def calculate_trip_budget(tier="heritage", days=3, travelers=2, currency="INR"):
    """Calculate comprehensive itemized trip budget for given duration, travelers, and tier."""
    t_key = tier.lower().strip() if tier else "heritage"
    if t_key not in TRAVEL_TIERS_DB:
        t_key = "heritage"

    t_data = TRAVEL_TIERS_DB[t_key]
    d_count = max(1, min(30, int(days) if str(days).isdigit() else 3))
    tr_count = max(1, min(20, int(travelers) if str(travelers).isdigit() else 2))

    daily_base_inr = t_data["daily_rate_inr"]
    total_inr = daily_base_inr * d_count * tr_count

    # Itemized total calculation
    itemized_totals_inr = {}
    for cat, daily_cat_cost in t_data["breakdown_inr"].items():
        itemized_totals_inr[cat] = daily_cat_cost * d_count * tr_count

    curr_key = currency.upper().strip() if currency else "INR"
    if curr_key not in CURRENCY_RATES_DB:
        curr_key = "INR"

    rate = CURRENCY_RATES_DB[curr_key]["rate_to_inr"]
    sym = CURRENCY_RATES_DB[curr_key]["symbol"]

    itemized_converted = {}
    for cat, amt_inr in itemized_totals_inr.items():
        itemized_converted[cat] = {
            "amount": round(amt_inr / rate, 2),
            "amount_inr": amt_inr
        }

    return {
        "tier": t_key,
        "tier_name": t_data["tier_name"],
        "days": d_count,
        "travelers": tr_count,
        "currency": curr_key,
        "currency_symbol": sym,
        "total_amount": round(total_inr / rate, 2),
        "total_amount_inr": total_inr,
        "daily_per_person": round(daily_base_inr / rate, 2),
        "daily_per_person_inr": daily_base_inr,
        "itemized_breakdown": itemized_converted,
        "stay_type": t_data["stay_type"],
        "transit_type": t_data["transit_type"],
        "dining_type": t_data["dining_type"]
    }

DISTRICT_COST_INDEX_DB = {
    "patna": {"factor": 1.15, "tier": "Metro Hub", "notes": "Higher hotel and private cab rates along Ganga riverfront."},
    "gaya": {"factor": 1.10, "tier": "International Pilgrimage", "notes": "Seasonal surge during Pitripaksha and Kalachakra periods."},
    "nalanda": {"factor": 1.05, "tier": "Heritage Valley", "notes": "Moderate rates for Rajgir ropeway and local tongas."},
    "west-champaran": {"factor": 1.12, "tier": "Wilderness Safari", "notes": "Forest department gypsy permits and remote logistics."},
    "madhubani": {"factor": 0.85, "tier": "Rural Artisan Cluster", "notes": "Highly economical village homestays and organic food."}
}

def get_district_cost_index():
    """Return district relative cost of living and tourism expense multipliers."""
    return DISTRICT_COST_INDEX_DB

def get_district_adjusted_budget(base_daily_inr, district_slug):
    """Adjust daily rate with district-specific price multiplier."""
    if not district_slug:
        return base_daily_inr
    d_clean = district_slug.lower().strip()
    factor = DISTRICT_COST_INDEX_DB.get(d_clean, {}).get("factor", 1.0)
    return round(base_daily_inr * factor, 2)