"""
Inter-District Transit Guide & Commute Fare Estimator Model
Provides Bihar airport hubs, major railway terminals, BSRTC bus depots,
inter-district route transit matrices, and local transit fare estimation engines.
"""

AIRPORTS = [
    {
        "code": "PAT",
        "name": "Jay Prakash Narayan International Airport",
        "city": "Patna",
        "district": "Patna",
        "type": "Customs / Domestic International Hub",
        "connectivity": "Direct daily flights to Delhi, Mumbai, Bengaluru, Kolkata, Hyderabad, Chennai, Ahmedabad, Lucknow.",
        "distance_to_center_km": 5,
        "transit_options": ["Prepaid Taxi", "App Cabs (Ola/Uber)", "Auto-rickshaw", "BSRTC Airport Electric AC Bus"]
    },
    {
        "code": "GAY",
        "name": "Gaya International Airport",
        "city": "Gaya",
        "district": "Gaya",
        "type": "International Seasonal / Domestic Hub",
        "connectivity": "Direct flights to Kolkata, Varanasi, Delhi and seasonal international charters to Bangkok, Yangon, Colombo, Paro.",
        "distance_to_center_km": 11,
        "transit_options": ["Prepaid Taxi", "Auto-rickshaw", "Hotel Private Shuttles", "Bodh Gaya E-Rickshaws"]
    },
    {
        "code": "DBR",
        "name": "Darbhanga Airport",
        "city": "Darbhanga",
        "district": "Darbhanga",
        "type": "Regional UDAN Domestic Hub",
        "connectivity": "Direct flights to Delhi, Mumbai, Bengaluru, Kolkata, Hyderabad serving North Bihar & Mithila region.",
        "distance_to_center_km": 6,
        "transit_options": ["Local Taxis", "Shared Auto-rickshaws", "App Cabs"]
    }
]

RAILWAY_JUNCTIONS = [
    {
        "code": "PNBE",
        "name": "Patna Junction & Patliputra (PPTA)",
        "district": "Patna",
        "importance": "Major East Central Railway hub connecting Howrah-Delhi main line and South/West India.",
        "key_trains": ["Vande Bharat Express (Patna-Ranchi, Patna-Howrah, Patna-Lucknow)", "Rajdhani Express", "Sampoorna Kranti Express", "Tejas Express"]
    },
    {
        "code": "GAYA",
        "name": "Gaya Junction",
        "district": "Gaya",
        "importance": "Grand Chord railway route linking Delhi to Kolkata; primary rail gateway for Buddhist pilgrims.",
        "key_trains": ["Vande Bharat Express (Varanasi-Ranchi via Gaya)", "Bodh Gaya Pilgrimage Specials", "Kalka Mail / Netaji Express", "Purushottam Express"]
    },
    {
        "code": "RGD",
        "name": "Rajgir Railway Station",
        "district": "Nalanda",
        "importance": "Terminal for pilgrim trains to Nalanda, Pawapuri, and Vishwa Shanti Stupa.",
        "key_trains": ["Shramjeevi Express (New Delhi - Rajgir)", "Budhpurnima Express", "Rajgir-Howrah Fast Passenger"]
    },
    {
        "code": "MFP",
        "name": "Muzaffarpur Junction",
        "district": "Muzaffarpur",
        "importance": "Principal rail nerve center for North Bihar, Vaishali, and Nepal border access.",
        "key_trains": ["Vaishali Express", "Sapt Kranti Superfast Express", "Bagh Express", "Mithila Express"]
    },
    {
        "code": "BGP",
        "name": "Bhagalpur Junction",
        "district": "Bhagalpur",
        "importance": "Key junction on Sahibganj loop line serving Vikramshila, Anga region, and silk trade.",
        "key_trains": ["Vikramshila Superfast Express", "Vande Bharat Express (Bhagalpur-Howrah)", "Anga Express", "Bhagalpur-Surat Express"]
    }
]

BUS_TERMINALS = [
    {
        "name": "Patliputra ISBT (Bairiya, Patna)",
        "district": "Patna",
        "type": "Inter-State & Regional Mega Terminal",
        "services": "24/7 BSRTC & private luxury AC sleeper buses to all 38 Bihar districts, Ranchi, Kolkata, Siliguri, Varanasi, Gorakhpur, Kathmandu."
    },
    {
        "name": "Bankipore Bus Depot (Gandhi Maidan, Patna)",
        "district": "Patna",
        "type": "City & Regional Transit Hub",
        "services": "BSRTC electric city buses, Nalanda/Rajgir day tour shuttles, and airport feeder coaches."
    },
    {
        "name": "Gaya BSRTC Bus Stand",
        "district": "Gaya",
        "type": "Regional Pilgrim Hub",
        "services": "Frequent buses to Bodh Gaya, Rajgir, Nawada, Sasaram, Hazaribagh, and Varanasi."
    },
    {
        "name": "Imli Chatti Bus Stand (Muzaffarpur)",
        "district": "Muzaffarpur",
        "type": "North Bihar Hub",
        "services": "Direct coach links to Sitamarhi, Motihari, Bettiah, Raxaul (Nepal Gate), and Darbhanga."
    }
]

INTERDISTRICT_TRANSIT_ROUTES = [
    {
        "id": "patna-gaya",
        "origin": "Patna",
        "destination": "Gaya / Bodh Gaya",
        "distance_km": 105,
        "train_time_hrs": "1.75 - 2.5 hrs",
        "road_time_hrs": "2.5 - 3.0 hrs",
        "recommended_mode": "Train (Vande Bharat / Jan Shatabdi) or Four-Lane NH-22 Expressway",
        "freq_daily": "25+ trains, 50+ buses daily"
    },
    {
        "id": "patna-rajgir",
        "origin": "Patna",
        "destination": "Rajgir / Nalanda",
        "distance_km": 102,
        "train_time_hrs": "2.0 - 2.75 hrs",
        "road_time_hrs": "2.25 - 2.5 hrs",
        "recommended_mode": "NH-20 State Highway or Shramjeevi / Rajgir Passenger Trains",
        "freq_daily": "6 trains, 40+ buses daily"
    },
    {
        "id": "patna-vaishali",
        "origin": "Patna",
        "destination": "Vaishali / Hajipur",
        "distance_km": 55,
        "train_time_hrs": "0.5 hr to Hajipur",
        "road_time_hrs": "1.25 - 1.5 hrs",
        "recommended_mode": "Road via JP Ganga Setu / NH-22 to Hajipur then SH to Vaishali",
        "freq_daily": "Continuous shared taxis, autos, and local buses"
    },
    {
        "id": "patna-sasaram",
        "origin": "Patna",
        "destination": "Sasaram (Rohtas)",
        "distance_km": 155,
        "train_time_hrs": "2.5 - 3.0 hrs via Pt Deen Dayal Upadhyaya Junction or Ara-Sasaram line",
        "road_time_hrs": "3.5 - 4.0 hrs via NH-119",
        "recommended_mode": "Direct Train via Ara / Buxar or Private Taxi via NH-119",
        "freq_daily": "8 trains, 20+ buses daily"
    },
    {
        "id": "patna-bhagalpur",
        "origin": "Patna",
        "destination": "Bhagalpur",
        "distance_km": 225,
        "train_time_hrs": "3.5 - 4.5 hrs",
        "road_time_hrs": "5.0 - 6.0 hrs",
        "recommended_mode": "Intercity Superfast Express / Vande Bharat Express",
        "freq_daily": "12 trains, 30+ buses daily"
    },
    {
        "id": "patna-darbhanga",
        "origin": "Patna",
        "destination": "Darbhanga / Madhubani",
        "distance_km": 140,
        "train_time_hrs": "3.0 - 4.0 hrs",
        "road_time_hrs": "3.0 - 3.5 hrs via NH-27 expressway",
        "recommended_mode": "Road via NH-27 Expressway or Direct Intercity Express",
        "freq_daily": "10 trains, 35+ buses daily"
    },
    {
        "id": "gaya-rajgir",
        "origin": "Gaya",
        "destination": "Rajgir",
        "distance_km": 68,
        "train_time_hrs": "1.5 - 2.0 hrs",
        "road_time_hrs": "1.5 - 1.75 hrs",
        "recommended_mode": "Direct Road / Tourist Taxi via Hisua-Nawada Route",
        "freq_daily": "4 trains, 20+ buses daily"
    }
]

VEHICLE_RATE_CARDS = {
    "auto_shared": {
        "title": "Shared Auto-rickshaw (Tempo / Vikram)",
        "base_fare": 10,
        "base_km": 3,
        "per_km": 4.0,
        "unit": "per passenger",
        "description": "Fixed route stage-carriage shared transit common across all towns."
    },
    "auto_reserved": {
        "title": "Reserved Auto-rickshaw (Full Auto)",
        "base_fare": 40,
        "base_km": 2,
        "per_km": 14.0,
        "unit": "entire vehicle (up to 3 passengers)",
        "description": "Private door-to-door auto hire for local sightseeing or station transfers."
    },
    "e_rickshaw": {
        "title": "E-Rickshaw (Toto / Mayuri)",
        "base_fare": 10,
        "base_km": 2,
        "per_km": 5.0,
        "unit": "per passenger (local hops)",
        "description": "Zero-emission quiet local transport ideal for temple circuits (Bodh Gaya, Rajgir, Patna Old City)."
    },
    "cab_hatchback": {
        "title": "App / AC Taxi (Hatchback / Compact Sedan)",
        "base_fare": 100,
        "base_km": 4,
        "per_km": 16.0,
        "unit": "entire vehicle (up to 4 passengers)",
        "description": "AC private cab service suitable for city transit and airport drops."
    },
    "cab_suv": {
        "title": "Outstation / Tourist SUV (Innova / Ertiga)",
        "base_fare": 160,
        "base_km": 4,
        "per_km": 22.0,
        "unit": "entire vehicle (up to 6-7 passengers)",
        "description": "Comfortable long-distance touring vehicle for inter-district circuits."
    },
    "bus_bsrtc": {
        "title": "BSRTC State Transport Bus",
        "base_fare": 15,
        "base_km": 10,
        "per_km": 1.4,
        "unit": "per passenger",
        "description": "Economical government passenger bus service between towns and district centers."
    }
}

def get_airports():
    """Return all commercial airports in Bihar."""
    return AIRPORTS

def get_railway_junctions():
    """Return major railway junctions."""
    return RAILWAY_JUNCTIONS

def get_bus_terminals():
    """Return major bus depots."""
    return BUS_TERMINALS

def get_all_transport_hubs():
    """Return dictionary of all transport hubs categorized."""
    return {
        "airports": AIRPORTS,
        "railway_junctions": RAILWAY_JUNCTIONS,
        "bus_terminals": BUS_TERMINALS
    }

def get_interdistrict_routes(origin=None, destination=None):
    """Retrieve inter-district routes, optionally filtered by origin/destination."""
    routes = INTERDISTRICT_TRANSIT_ROUTES
    if origin:
        o_clean = origin.lower().strip()
        routes = [r for r in routes if o_clean in r["origin"].lower()]
    if destination:
        d_clean = destination.lower().strip()
        routes = [r for r in routes if d_clean in r["destination"].lower()]
    return routes

def get_vehicle_rate_cards():
    """Return standard rate cards for all commute options."""
    return VEHICLE_RATE_CARDS

def estimate_commute_fare(vehicle_type, distance_km, is_night=False, is_shared=False):
    """
    Calculate estimated commute fare for given vehicle type and distance.
    Returns breakdown with base fare, distance charge, night surcharge, and total.
    """
    v_type = vehicle_type.lower().strip() if vehicle_type else "auto_reserved"
    if v_type not in VEHICLE_RATE_CARDS:
        v_type = "auto_reserved"

    card = VEHICLE_RATE_CARDS[v_type]
    dist = max(1.0, float(distance_km or 1.0))
    base_km = float(card["base_km"])
    base_fare = float(card["base_fare"])
    per_km = float(card["per_km"])

    extra_km = max(0.0, dist - base_km)
    dist_fare = round(extra_km * per_km, 2)
    subtotal = base_fare + dist_fare

    night_surcharge = round(subtotal * 0.25, 2) if is_night else 0.0
    total = round(subtotal + night_surcharge)

    return {
        "vehicle_type": v_type,
        "vehicle_title": card["title"],
        "distance_km": dist,
        "base_fare_inr": base_fare,
        "base_km_included": base_km,
        "additional_distance_fare_inr": dist_fare,
        "night_surcharge_inr": night_surcharge,
        "total_estimated_fare_inr": total,
        "pricing_unit": card["unit"],
        "description": card["description"]
    }