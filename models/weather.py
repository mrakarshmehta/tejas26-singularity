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