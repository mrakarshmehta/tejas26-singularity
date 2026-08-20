"""
Bihar Weather, Microclimate & Air Quality Advisory Model
Provides district-wise seasonal meteorological norms, AQI classifications,
monsoon/fog travel advisories, and outdoor visibility indices.
"""

DISTRICT_WEATHER_DB = [
    {
        "district": "Patna",
        "slug": "patna",
        "climate_zone": "Subtropical Monsoon Plain",
        "elevation_m": 53,
        "summer_temp": {"min": 26, "max": 42},
        "winter_temp": {"min": 8, "max": 22},
        "monsoon_months": "Mid-June to Late September",
        "annual_rainfall_mm": 1130,
        "current_season_aqi_range": {"min": 90, "max": 240, "typical_category": "Moderate to Poor (Winter Fog)"},
        "best_travel_window": "October to March",
        "clothing_recommendation": {
            "winter": "Medium woolens, thermal innerwear, jacket for evening Ganga riverfront",
            "summer": "Breathable cottons, wide-brim hat, high UV sunscreen",
            "monsoon": "Waterproof umbrella, quick-dry footwear"
        },
        "microclimate_notes": "Riverfront breezes along Ganga Promenade moderate evening temperatures during pre-monsoon."
    },
    {
        "district": "Gaya",
        "slug": "gaya",
        "climate_zone": "Semi-Arid Rocky Valley",
        "elevation_m": 111,
        "summer_temp": {"min": 28, "max": 45},
        "winter_temp": {"min": 4, "max": 24},
        "monsoon_months": "Late June to September",
        "annual_rainfall_mm": 1050,
        "current_season_aqi_range": {"min": 60, "max": 160, "typical_category": "Satisfactory to Moderate"},
        "best_travel_window": "November to February",
        "clothing_recommendation": {
            "winter": "Heavy woolens for early morning Mahabodhi circumambulation",
            "summer": "Light cotton clothing, hydration pack essential",
            "monsoon": "Light rain gear"
        },
        "microclimate_notes": "Surrounding rocky hills (Pretshila, Brahmayoni) create sharp diurnal temperature swings."
    },
    {
        "district": "Nalanda",
        "slug": "nalanda",
        "climate_zone": "Alluvial Lowland & Rajgir Valley Hills",
        "elevation_m": 67,
        "summer_temp": {"min": 25, "max": 41},
        "winter_temp": {"min": 7, "max": 23},
        "monsoon_months": "June to September",
        "annual_rainfall_mm": 1000,
        "current_season_aqi_range": {"min": 50, "max": 140, "typical_category": "Good to Satisfactory in Rajgir Hills"},
        "best_travel_window": "October to March",
        "clothing_recommendation": {
            "winter": "Warm layers for Rajgir ropeway and open ruins walking",
            "summer": "Sun hat, sunglasses, lightweight cotton",
            "monsoon": "Sturdy grip shoes for wet stone pathways"
        },
        "microclimate_notes": "Thermal springs at Rajgir maintain 52-65°C temperatures year-round."
    },
    {
        "district": "West Champaran",
        "slug": "west-champaran",
        "climate_zone": "Sub-Himalayan Terai Sal Forest",
        "elevation_m": 85,
        "summer_temp": {"min": 22, "max": 38},
        "winter_temp": {"min": 5, "max": 20},
        "monsoon_months": "June to October",
        "annual_rainfall_mm": 1540,
        "current_season_aqi_range": {"min": 30, "max": 80, "typical_category": "Good / Clean Mountain Air"},
        "best_travel_window": "November to April",
        "clothing_recommendation": {
            "winter": "Heavy insulated fleece/jackets for early morning open safari",
            "summer": "Earthy toned khaki cottons",
            "monsoon": "Heavy-duty waterproof poncho & leech socks"
        },
        "microclimate_notes": "High humidity and cool mountain downdrafts from neighboring Nepal Himalayan foothills."
    },
    {
        "district": "Madhubani",
        "slug": "madhubani",
        "climate_zone": "North Bihar Floodplain & Wetland",
        "elevation_m": 56,
        "summer_temp": {"min": 24, "max": 39},
        "winter_temp": {"min": 8, "max": 23},
        "monsoon_months": "Mid-June to October",
        "annual_rainfall_mm": 1300,
        "current_season_aqi_range": {"min": 45, "max": 110, "typical_category": "Good to Moderate"},
        "best_travel_window": "October to March",
        "clothing_recommendation": {
            "winter": "Light to medium woolens",
            "summer": "Loose breathable handloom cotton",
            "monsoon": "Waterproof footwear for rural wetland paths"
        },
        "microclimate_notes": "Dense village pond clusters (pokhars) create pleasant local micro-humidity and cool breezes."
    },
    {
        "district": "Rohtas",
        "slug": "rohtas",
        "climate_zone": "Vindhyan Sandstone Plateau & Canyon",
        "elevation_m": 107,
        "summer_temp": {"min": 25, "max": 43},
        "winter_temp": {"min": 6, "max": 22},
        "monsoon_months": "June to September",
        "annual_rainfall_mm": 1100,
        "current_season_aqi_range": {"min": 40, "max": 120, "typical_category": "Good to Satisfactory on Plateau"},
        "best_travel_window": "July to March (Peak waterfalls during Monsoon)",
        "clothing_recommendation": {
            "winter": "Windproof jackets for high plateau forts",
            "summer": "Hydration gear and sun protection",
            "monsoon": "Trekking boots with anti-slip vibram soles"
        },
        "microclimate_notes": "High-altitude waterfall spray at Telhar Kund and Tutla Bhawani reduces ambient temperature by 4-6°C."
    }
]

AQI_LEVELS = [
    {"range": [0, 50], "label": "Good", "color": "#16a34a", "advisory": "Air quality is ideal for outdoor monuments and heritage walks."},
    {"range": [51, 100], "label": "Satisfactory", "color": "#84cc16", "advisory": "Minor discomfort for sensitive individuals; excellent for general travel."},
    {"range": [101, 200], "label": "Moderate", "color": "#eab308", "advisory": "Breathing discomfort possible for children and elderly; carry water."},
    {"range": [201, 300], "label": "Poor", "color": "#f97316", "advisory": "Consider wearing an N95 mask during peak traffic or heavy morning fog."},
    {"range": [301, 500], "label": "Severe", "color": "#dc2626", "advisory": "Avoid strenuous outdoor exertion; visit indoor museums and galleries."}
]

def get_all_district_weather():
    """Return weather normals and microclimatic data for all cataloged districts."""
    return DISTRICT_WEATHER_DB

def get_district_weather_by_slug(slug):
    """Retrieve district weather by slug or name."""
    if not slug:
        return None
    s = slug.lower().strip()
    for w in DISTRICT_WEATHER_DB:
        if w["slug"] == s or w["district"].lower() == s:
            return w
    return None

def classify_aqi_level(aqi_value):
    """Return health category and advisory string for a given numeric AQI."""
    try:
        val = int(aqi_value)
    except (ValueError, TypeError):
        return {"label": "Unknown", "color": "#64748b", "advisory": "No AQI data available."}

    for lvl in AQI_LEVELS:
        if lvl["range"][0] <= val <= lvl["range"][1]:
            return lvl
    return AQI_LEVELS[-1]

def get_seasonal_packing_advice(slug, month=None):
    """Return packing and clothing advisory tailored to district microclimate and season."""
    weather = get_district_weather_by_slug(slug)
    if not weather:
        return {"general": "Light cottons in summer, warm woolens in winter, rain protection in monsoon."}

    month_num = int(month) if str(month).isdigit() else 11
    if month_num in [11, 12, 1, 2]:
        season = "winter"
    elif month_num in [6, 7, 8, 9]:
        season = "monsoon"
    else:
        season = "summer"

    return {
        "season_detected": season,
        "recommendation": weather["clothing_recommendation"].get(season, ""),
        "microclimate": weather.get("microclimate_notes", ""),
        "best_window": weather.get("best_travel_window", "")
    }

SEASONAL_PHENOMENA_DB = [
    {
        "id": "phenom-winter-fog",
        "name": "Winter Gangetic Radiation Fog & Dawn Visibility",
        "active_months": ["December", "January"],
        "affected_regions": ["Patna", "Vaishali", "Begusarai", "Bhagalpur"],
        "visibility_impact": "Morning visibility 50m - 300m until 09:30 AM",
        "travel_tip": "Schedule river cruises and highway driving between 10:00 AM and 04:30 PM for clear panoramic vistas.",
        "photography_rating": "Spectacular misty dawn silhouette shots over ancient stupas and river ghats."
    },
    {
        "id": "phenom-monsoon-waterfalls",
        "name": "Monsoon Rohtas-Kaimur Waterfall Surge",
        "active_months": ["July", "August", "September", "October"],
        "affected_regions": ["Rohtas", "Kaimur", "Nawada"],
        "visibility_impact": "High cascade volume; crystal-clear canyon air",
        "travel_tip": "Visit Telhar Kund and Kakolat Falls during post-rain sunny mornings. Follow marked safety railings.",
        "photography_rating": "Peak emerald green vegetation and thunderous multi-tiered waterfall cascades."
    },
    {
        "id": "phenom-summer-heatwave",
        "name": "Mid-Summer 'Loo' Heatwave & Evening Micro-Breeze",
        "active_months": ["May", "June"],
        "affected_regions": ["Gaya", "Aurangabad", "Bhojpur", "Buxar"],
        "visibility_impact": "Intense afternoon solar irradiance; high thermal contrast",
        "travel_tip": "Explore open monuments at sunrise (05:30 AM - 08:30 AM); enjoy chilled Sattu Sherbet and Aam Panna coolers.",
        "photography_rating": "Golden hour twilight illumination on sandstone monuments."
    }
]

def get_all_seasonal_phenomena():
    """Return all special meteorological and seasonal travel phenomena."""
    return SEASONAL_PHENOMENA_DB

def get_phenomena_by_month(month_name):
    """Filter seasonal phenomena by current or planned travel month."""
    if not month_name:
        return SEASONAL_PHENOMENA_DB
    m_clean = month_name.capitalize().strip()
    return [p for p in SEASONAL_PHENOMENA_DB if m_clean in p.get("active_months", [])]