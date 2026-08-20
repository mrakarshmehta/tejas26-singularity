"""
Bihar Traveler Safety, Emergency Contacts & Healthcare Directory Model
Provides statewide emergency helplines, district-wise police control rooms,
24/7 trauma hospitals, disaster relief (SDRF), and traveler safety advisories.
"""

STATEWIDE_HELPLINES = [
    {
        "service": "Emergency Response Support System (ERSS)",
        "number": "112",
        "category": "Universal",
        "description": "Unified 24/7 national emergency number for Police, Fire, and Ambulance.",
        "icon": "shield-alert",
        "priority": 1
    },
    {
        "service": "Women Safety & Helpline",
        "number": "1091",
        "category": "Women Safety",
        "description": "Dedicated toll-free helpline for women in distress or needing immediate protection.",
        "icon": "user-check",
        "priority": 2
    },
    {
        "service": "Women Development Corporation (WDC) Helpline",
        "number": "181",
        "category": "Women Safety",
        "description": "Toll-free 24/7 counseling, crisis intervention, and legal assistance for women travelers.",
        "icon": "heart-handshake",
        "priority": 3
    },
    {
        "service": "Emergency Medical & Ambulance Service",
        "number": "108",
        "category": "Medical",
        "description": "Free 24/7 state-wide government ambulance dispatch across all 38 districts.",
        "icon": "activity",
        "priority": 4
    },
    {
        "service": "Janani Express (Maternal & Child Ambulance)",
        "number": "102",
        "category": "Medical",
        "description": "Emergency transport dedicated for maternal care, infants, and rural medical emergencies.",
        "icon": "plus-circle",
        "priority": 5
    },
    {
        "service": "Bihar State Disaster Management Authority (BSDMA)",
        "number": "1070",
        "category": "Disaster Relief",
        "description": "State disaster control room for flood, earthquake, and extreme weather emergencies.",
        "icon": "alert-triangle",
        "priority": 6
    },
    {
        "service": "Bihar Tourism Tourist Police Assistance Cell",
        "number": "+91-612-2215354",
        "category": "Tourist Police",
        "description": "Bihar State Tourism Development Corporation (BSTDC) dedicated tourist security desk at Patna.",
        "icon": "map-pin",
        "priority": 7
    },
    {
        "service": "National Highway Emergency Assistance",
        "number": "1033",
        "category": "Transit Safety",
        "description": "NHAI 24/7 toll-free helpline for mechanical breakdown, medical aid, or towing on National Highways.",
        "icon": "navigation",
        "priority": 8
    },
    {
        "service": "Cyber Crime Helpline",
        "number": "1930",
        "category": "Cyber & Fraud",
        "description": "National cyber crime reporting portal for travel payment scams and digital fraud.",
        "icon": "lock",
        "priority": 9
    }
]

DISTRICT_SAFETY_DIRECTORY = {
    "patna": {
        "district": "Patna",
        "police_control_room": "+91-612-2201977",
        "tourist_police_desk": "+91-612-2215354",
        "sp_office": "+91-612-2219406",
        "medical_facilities": [
            {
                "name": "Patna Medical College & Hospital (PMCH)",
                "type": "Government Apex Hospital",
                "phone": "+91-612-2300080",
                "address": "Ashok Rajpath, Patna",
                "emergency_24x7": True,
                "trauma_center": True
            },
            {
                "name": "All India Institute of Medical Sciences (AIIMS Patna)",
                "type": "National Premier Institute",
                "phone": "+91-612-2451070",
                "address": "Phulwari Sharif, Patna",
                "emergency_24x7": True,
                "trauma_center": True
            },
            {
                "name": "Indira Gandhi Institute of Medical Sciences (IGIMS)",
                "type": "Super Specialty Hospital",
                "phone": "+91-612-2297631",
                "address": "Sheikhpura, Bailey Road, Patna",
                "emergency_24x7": True,
                "trauma_center": True
            }
        ]
    },
    "gaya": {
        "district": "Gaya",
        "police_control_room": "+91-631-2225900",
        "tourist_police_desk": "+91-631-2200777",
        "sp_office": "+91-631-2225910",
        "medical_facilities": [
            {
                "name": "Anugrah Narayan Magadh Medical College & Hospital (ANMMCH)",
                "type": "Government Medical College",
                "phone": "+91-631-2400844",
                "address": "Sherghati Road, Gaya",
                "emergency_24x7": True,
                "trauma_center": True
            },
            {
                "name": "Bodh Gaya Primary Health Center & Trauma Care",
                "type": "Tourist Health Center",
                "phone": "+91-631-2200234",
                "address": "Near Mahabodhi Temple Complex, Bodh Gaya",
                "emergency_24x7": True,
                "trauma_center": False
            }
        ]
    },
    "nalanda": {
        "district": "Nalanda (Bihar Sharif & Rajgir)",
        "police_control_room": "+91-6112-235207",
        "tourist_police_desk": "+91-6112-255225",
        "sp_office": "+91-6112-235201",
        "medical_facilities": [
            {
                "name": "Vardhman Institute of Medical Sciences (VIMS Pawapuri)",
                "type": "Government Medical College",
                "phone": "+91-6112-228100",
                "address": "Pawapuri, Nalanda",
                "emergency_24x7": True,
                "trauma_center": True
            },
            {
                "name": "Sub-Divisional Hospital Rajgir",
                "type": "Tourist Sub-Divisional Hospital",
                "phone": "+91-6112-255010",
                "address": "Station Road, Rajgir",
                "emergency_24x7": True,
                "trauma_center": False
            }
        ]
    },
    "vaishali": {
        "district": "Vaishali (Hajipur)",
        "police_control_room": "+91-6224-272202",
        "tourist_police_desk": "+91-6224-273510",
        "sp_office": "+91-6224-272201",
        "medical_facilities": [
            {
                "name": "Sadar Hospital Hajipur",
                "type": "District Headquarters Hospital",
                "phone": "+91-6224-272225",
                "address": "Hospital Road, Hajipur",
                "emergency_24x7": True,
                "trauma_center": True
            }
        ]
    },
    "bhagalpur": {
        "district": "Bhagalpur",
        "police_control_room": "+91-641-2400100",
        "tourist_police_desk": "+91-641-2401210",
        "sp_office": "+91-641-2400105",
        "medical_facilities": [
            {
                "name": "Jawaharlal Nehru Medical College & Hospital (JLNMCH)",
                "type": "Government Medical College",
                "phone": "+91-641-2401078",
                "address": "Mayaganj, Bhagalpur",
                "emergency_24x7": True,
                "trauma_center": True
            }
        ]
    },
    "muzaffarpur": {
        "district": "Muzaffarpur",
        "police_control_room": "+91-621-2212100",
        "tourist_police_desk": "+91-621-2212350",
        "sp_office": "+91-621-2212102",
        "medical_facilities": [
            {
                "name": "Sri Krishna Medical College & Hospital (SKMCH)",
                "type": "Government Medical College",
                "phone": "+91-621-2230050",
                "address": "Umanagar, Muzaffarpur",
                "emergency_24x7": True,
                "trauma_center": True
            }
        ]
    },
    "darbhanga": {
        "district": "Darbhanga",
        "police_control_room": "+91-6272-222200",
        "tourist_police_desk": "+91-6272-223110",
        "sp_office": "+91-6272-222202",
        "medical_facilities": [
            {
                "name": "Darbhanga Medical College & Hospital (DMCH)",
                "type": "Government Medical College",
                "phone": "+91-6272-233055",
                "address": "Laheriasarai, Darbhanga",
                "emergency_24x7": True,
                "trauma_center": True
            }
        ]
    },
    "rohtas": {
        "district": "Rohtas (Sasaram)",
        "police_control_room": "+91-6184-222210",
        "tourist_police_desk": "+91-6184-223400",
        "sp_office": "+91-6184-222212",
        "medical_facilities": [
            {
                "name": "Sadar Hospital Sasaram",
                "type": "District Hospital",
                "phone": "+91-6184-222240",
                "address": "GT Road, Sasaram",
                "emergency_24x7": True,
                "trauma_center": True
            },
            {
                "name": "Narayan Medical College & Hospital (NMCH Jamuhar)",
                "type": "Super Specialty Hospital",
                "phone": "+91-6184-271200",
                "address": "Jamuhar, Rohtas",
                "emergency_24x7": True,
                "trauma_center": True
            }
        ]
    },
    "west-champaran": {
        "district": "West Champaran (Bettiah & Valmiki Nagar)",
        "police_control_room": "+91-6254-242200",
        "tourist_police_desk": "+91-6254-243100",
        "sp_office": "+91-6254-242205",
        "medical_facilities": [
            {
                "name": "Government Medical College Bettiah",
                "type": "Government Medical College",
                "phone": "+91-6254-245000",
                "address": "Bettiah, West Champaran",
                "emergency_24x7": True,
                "trauma_center": True
            },
            {
                "name": "Valmiki Nagar Forest Eco-Clinic & First Aid",
                "type": "Eco-Tourism First Aid Post",
                "phone": "+91-6254-282100",
                "address": "Near Forest Rest House, Valmiki Nagar",
                "emergency_24x7": False,
                "trauma_center": False
            }
        ]
    }
}

TRAVELER_SAFETY_GUIDELINES = [
    {
        "category": "General Travel & Transit",
        "tips": [
            "Keep emergency contact numbers (112, 108, 1091) saved offline on your phone or printed.",
            "For inter-district night travel, prefer verified Indian Railways trains, BSRTC Volvo buses, or authorized taxi services.",
            "Ensure pre-paid SIM connectivity; BSNL, Jio, and Airtel offer broad 4G/5G coverage along all major tourist circuits.",
            "While exploring rural heritage ruins (e.g. Rohtasgarh, Telhar Kund), begin return journeys before sunset."
        ]
    },
    {
        "category": "Monsoon & Weather Precautions",
        "tips": [
            "Check BSDMA flood advisories during the peak monsoon season (July to September) when traveling near Kosi and Gandak river plains.",
            "In waterfalls and hilly gorges (Kakolat, Tutla Bhawani, Karkatgarh), follow forest guard advisories during sudden flash floods.",
            "Carry sufficient drinking water and electrolytes during peak summer months (April to June)."
        ]
    },
    {
        "category": "Cultural & Heritage Respect",
        "tips": [
            "Remove shoes and dress modestly before entering temple sanctorum, monasteries, and Sufi dargahs.",
            "Ask for permission before photographing local artisans, monks, or village residents.",
            "Avoid purchasing uncertified wildlife products in forest reserves like Valmiki National Park or Kanwar Lake."
        ]
    }
]

def get_statewide_helplines():
    """Return list of all statewide emergency contact numbers sorted by priority."""
    return sorted(STATEWIDE_HELPLINES, key=lambda x: x["priority"])

def get_all_district_safety():
    """Return dictionary of all district safety and medical directories."""
    return DISTRICT_SAFETY_DIRECTORY

def get_district_safety(district_slug):
    """Retrieve safety contacts and hospitals for a specific district slug."""
    if not district_slug:
        return None
    slug = district_slug.lower().strip().replace(" ", "-")
    return DISTRICT_SAFETY_DIRECTORY.get(slug)

def get_medical_facilities(district_slug=None):
    """Get medical facilities, optionally filtered by district."""
    if district_slug:
        d = get_district_safety(district_slug)
        return d.get("medical_facilities", []) if d else []
    
    all_facilities = []
    for slug, d in DISTRICT_SAFETY_DIRECTORY.items():
        for fac in d.get("medical_facilities", []):
            item = dict(fac)
            item["district"] = d["district"]
            item["district_slug"] = slug
            all_facilities.append(item)
    return all_facilities

def get_safety_guidelines():
    """Return traveler safety tips and seasonal advisories."""
    return TRAVELER_SAFETY_GUIDELINES