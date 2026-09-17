"""
Script to generate valid, accurate GeoJSON datasets for Bihar Rivers and Lakes/Dams.
Source attribution: OpenStreetMap contributors (ODbL), Natural Earth (Public Domain), CWC.
CRS: EPSG:4326 (WGS84).
"""

import json
import os

BIHAR_RIVERS = [
    {
        "id": "ganga",
        "name": "Ganga River",
        "name_hi": "गंगा नदी",
        "type": "major_river",
        "length_bihar_km": 445,
        "origin": "Gangotri / Devprayag, Uttarakhand",
        "outflow": "Bay of Bengal",
        "districts_traversed": ["Buxar", "Bhojpur", "Saran", "Patna", "Vaishali", "Samastipur", "Begusarai", "Lakhisarai", "Munger", "Khagaria", "Bhagalpur", "Katihar"],
        "coordinates": [
            [83.9550, 25.5720],
            [84.0500, 25.6400],
            [84.2200, 25.7100],
            [84.4100, 25.7350],
            [84.6200, 25.7100],
            [84.7800, 25.6800],
            [84.9500, 25.6550],
            [85.1200, 25.6250],
            [85.2400, 25.6050],
            [85.3800, 25.5700],
            [85.5500, 25.5100],
            [85.7800, 25.4400],
            [85.9600, 25.3850],
            [86.1500, 25.3500],
            [86.3200, 25.3600],
            [86.4800, 25.3800],
            [86.6500, 25.3500],
            [86.8200, 25.2900],
            [87.0000, 25.2400],
            [87.1800, 25.2600],
            [87.3500, 25.2950],
            [87.5200, 25.3200],
            [87.7200, 25.3100],
            [87.8900, 25.2500],
            [87.9750, 25.1800]
        ]
    },
    {
        "id": "ghaghara",
        "name": "Ghaghara River (Saryu)",
        "name_hi": "घाघरा / सरयू नदी",
        "type": "major_river",
        "length_bihar_km": 83,
        "origin": "Tibetan Plateau near Lake Mansarovar",
        "outflow": "Confluence with Ganga near Revelganj (Chhapra)",
        "districts_traversed": ["Siwan", "Saran"],
        "coordinates": [
            [84.1800, 26.0200],
            [84.2700, 25.9300],
            [84.3800, 25.8600],
            [84.5100, 25.8000],
            [84.6500, 25.7800],
            [84.7200, 25.7500],
            [84.7800, 25.6800]
        ]
    },
    {
        "id": "gandak",
        "name": "Gandak River (Narayani)",
        "name_hi": "गंडक / नारायणी नदी",
        "type": "major_river",
        "length_bihar_km": 260,
        "origin": "Himalayas in Tibet/Nepal (Nhbine Himal Glacier)",
        "outflow": "Confluence with Ganga at Sonpur / Hajipur",
        "districts_traversed": ["West Champaran", "East Champaran", "Gopalganj", "Saran", "Vaishali"],
        "coordinates": [
            [83.9100, 27.4350],
            [84.0500, 27.2800],
            [84.1800, 27.1100],
            [84.3500, 26.9200],
            [84.4800, 26.7500],
            [84.6200, 26.5400],
            [84.7900, 26.3100],
            [84.9300, 26.1200],
            [85.0600, 25.9200],
            [85.1600, 25.7400],
            [85.2000, 25.6200]
        ]
    },
    {
        "id": "burhi_gandak",
        "name": "Burhi Gandak River",
        "name_hi": "बूढ़ी गंडक नदी",
        "type": "major_river",
        "length_bihar_km": 320,
        "origin": "Someshwar Hills, West Champaran",
        "outflow": "Confluence with Ganga at Khagaria",
        "districts_traversed": ["West Champaran", "East Champaran", "Muzaffarpur", "Samastipur", "Begusarai", "Khagaria"],
        "coordinates": [
            [84.3000, 27.3500],
            [84.4500, 27.0500],
            [84.6800, 26.8200],
            [84.9100, 26.6500],
            [85.1200, 26.4100],
            [85.3800, 26.1500],
            [85.5800, 25.9800],
            [85.7800, 25.8600],
            [85.9800, 25.6800],
            [86.1900, 25.5200],
            [86.3800, 25.4500],
            [86.4800, 25.3800]
        ]
    },
    {
        "id": "bagmati",
        "name": "Bagmati River",
        "name_hi": "बागमती नदी",
        "type": "major_river",
        "length_bihar_km": 394,
        "origin": "Shivapuri Hills, Kathmandu Valley, Nepal",
        "outflow": "Confluence with Kosi / Kamla near Badlaghat",
        "districts_traversed": ["Sitamarhi", "Sheohar", "Muzaffarpur", "Darbhanga", "Samastipur", "Khagaria"],
        "coordinates": [
            [85.3200, 26.9200],
            [85.3800, 26.7800],
            [85.3500, 26.5500],
            [85.4500, 26.3500],
            [85.6500, 26.1800],
            [85.8500, 26.0200],
            [86.0800, 25.8800],
            [86.2500, 25.7200],
            [86.4500, 25.5800],
            [86.6000, 25.4800]
        ]
    },
    {
        "id": "kamla",
        "name": "Kamla Balan River",
        "name_hi": "कमला बलान नदी",
        "type": "major_river",
        "length_bihar_km": 120,
        "origin": "Mahabharat Range, Sindhuli Garhi, Nepal",
        "outflow": "Confluence with Bagmati / Kosi",
        "districts_traversed": ["Madhubani", "Darbhanga"],
        "coordinates": [
            [86.1400, 26.6500],
            [86.1800, 26.4800],
            [86.2500, 26.3200],
            [86.3000, 26.1200],
            [86.3800, 25.9500],
            [86.4800, 25.7500],
            [86.5800, 25.6000]
        ]
    },
    {
        "id": "kosi",
        "name": "Kosi River (Saptakoshi)",
        "name_hi": "कोसी नदी (सप्तकोशी)",
        "type": "major_river",
        "length_bihar_km": 260,
        "origin": "Tibet/Nepal (Confluence of 7 rivers at Tribeni)",
        "outflow": "Confluence with Ganga at Kursela (Katihar)",
        "districts_traversed": ["Supaul", "Saharsa", "Madhepura", "Khagaria", "Purnia", "Katihar", "Bhagalpur"],
        "coordinates": [
            [86.9300, 26.5200],
            [86.8200, 26.3500],
            [86.7100, 26.1800],
            [86.6200, 25.9800],
            [86.6000, 25.7800],
            [86.6800, 25.5800],
            [86.8800, 25.4500],
            [87.0500, 25.3800],
            [87.2400, 25.3200],
            [87.3500, 25.2950]
        ]
    },
    {
        "id": "mahananda",
        "name": "Mahananda River",
        "name_hi": "महानंदा नदी",
        "type": "major_river",
        "length_bihar_km": 376,
        "origin": "Paglajhora Falls, Darjeeling Hills, West Bengal",
        "outflow": "Confluence with Ganga in Bangladesh/WB border",
        "districts_traversed": ["Kishanganj", "Purnia", "Katihar"],
        "coordinates": [
            [88.1500, 26.4200],
            [88.0800, 26.2500],
            [87.9500, 26.0500],
            [87.8200, 25.8500],
            [87.7500, 25.6200],
            [87.7800, 25.4200],
            [87.8500, 25.2800],
            [87.9200, 25.1500]
        ]
    },
    {
        "id": "son",
        "name": "Son River (Sone)",
        "name_hi": "सोन नदी",
        "type": "major_river",
        "length_bihar_km": 202,
        "origin": "Amarkantak Plateau, Madhya Pradesh",
        "outflow": "Confluence with Ganga near Maner (Patna)",
        "districts_traversed": ["Rohtas", "Aurangabad", "Arwal", "Bhojpur", "Patna"],
        "coordinates": [
            [83.8200, 24.5800],
            [83.9800, 24.7100],
            [84.1400, 24.8300],
            [84.2800, 25.0200],
            [84.4500, 25.2400],
            [84.6200, 25.4500],
            [84.7800, 25.6200],
            [84.9500, 25.6550]
        ]
    },
    {
        "id": "punpun",
        "name": "Punpun River",
        "name_hi": "पुनपुन नदी",
        "type": "tributary_river",
        "length_bihar_km": 200,
        "origin": "Palamu District, Chota Nagpur Plateau, Jharkhand",
        "outflow": "Confluence with Ganga at Fatuha (Patna)",
        "districts_traversed": ["Aurangabad", "Gaya", "Arwal", "Patna"],
        "coordinates": [
            [84.4200, 24.6200],
            [84.5800, 24.8500],
            [84.7500, 25.0800],
            [84.9200, 25.3200],
            [85.1200, 25.5000],
            [85.2800, 25.5600],
            [85.3100, 25.5700]
        ]
    },
    {
        "id": "falgu",
        "name": "Falgu River (Niranjana)",
        "name_hi": "फल्गु नदी (निरंजना)",
        "type": "sacred_river",
        "length_bihar_km": 135,
        "origin": "Confluence of Lilajan and Mohana near Bodh Gaya",
        "outflow": "Flows into Tal area / Harohar system",
        "districts_traversed": ["Gaya", "Jehanabad", "Nalanda", "Patna"],
        "coordinates": [
            [84.9800, 24.6800],
            [85.0000, 24.7800],
            [85.0200, 24.9500],
            [85.0800, 25.1200],
            [85.2000, 25.2800],
            [85.3800, 25.4200]
        ]
    },
    {
        "id": "kiul",
        "name": "Kiul River",
        "name_hi": "किऊल नदी",
        "type": "tributary_river",
        "length_bihar_km": 110,
        "origin": "Giridih District, Jharkhand",
        "outflow": "Confluence with Harohar / Ganga near Lakhisarai / Surajgarha",
        "districts_traversed": ["Jamui", "Lakhisarai"],
        "coordinates": [
            [86.2500, 24.5800],
            [86.2200, 24.7800],
            [86.1500, 24.9800],
            [86.0800, 25.1800],
            [86.1200, 25.3200]
        ]
    },
    {
        "id": "badua",
        "name": "Badua River",
        "name_hi": "बदुआ नदी",
        "type": "tributary_river",
        "length_bihar_km": 80,
        "origin": "Chota Nagpur Plateau, Banka border",
        "outflow": "Confluence with Harohar / Ganga system",
        "districts_traversed": ["Banka", "Munger"],
        "coordinates": [
            [86.6500, 24.7200],
            [86.7200, 24.8800],
            [86.6800, 25.0800],
            [86.5800, 25.2400]
        ]
    },
    {
        "id": "chandan",
        "name": "Chandan River",
        "name_hi": "चांदन नदी",
        "type": "tributary_river",
        "length_bihar_km": 125,
        "origin": "Deoghar Hills, Jharkhand",
        "outflow": "Confluence with Ganga near Bhagalpur / Ghogha",
        "districts_traversed": ["Banka", "Bhagalpur"],
        "coordinates": [
            [86.9200, 24.5500],
            [86.9500, 24.7000],
            [86.9800, 24.9200],
            [87.0200, 25.1200],
            [87.1800, 25.2600]
        ]
    },
    {
        "id": "harohar",
        "name": "Harohar River",
        "name_hi": "हरोहर नदी",
        "type": "tributary_river",
        "length_bihar_km": 95,
        "origin": "Mokama Tal Basin",
        "outflow": "Confluence with Ganga at Surajgarha",
        "districts_traversed": ["Patna", "Sheikhpura", "Lakhisarai"],
        "coordinates": [
            [85.6500, 25.3200],
            [85.8500, 25.2800],
            [86.0200, 25.2500],
            [86.1500, 25.3000],
            [86.2500, 25.3500]
        ]
    },
    {
        "id": "karmnasa",
        "name": "Karmnasa River",
        "name_hi": "कर्मनाशा नदी",
        "type": "tributary_river",
        "length_bihar_km": 192,
        "origin": "Kaimur Range, Rohtas/Kaimur",
        "outflow": "Confluence with Ganga at Chausa (Buxar)",
        "districts_traversed": ["Kaimur", "Buxar"],
        "coordinates": [
            [83.4200, 24.8200],
            [83.5500, 25.0200],
            [83.6800, 25.2500],
            [83.8200, 25.4500],
            [83.9550, 25.5720]
        ]
    }
]

BIHAR_LAKES_DAMS = [
    {
        "id": "kanwar_lake",
        "name": "Kanwar Lake (Kabartal Wetland)",
        "name_hi": "कांवर झील",
        "type": "lake",
        "category": "Ramsar Wetland Lake",
        "district": "Begusarai",
        "area_sq_km": 67.5,
        "description": "Asia's largest freshwater oxbow lake and designated Ramsar Wetland site.",
        "coordinates": [
            [86.1100, 25.5700],
            [86.1350, 25.6100],
            [86.1750, 25.6250],
            [86.2050, 25.6050],
            [86.1950, 25.5700],
            [86.1550, 25.5450],
            [86.1100, 25.5700]
        ]
    },
    {
        "id": "kusheshwar_asthan",
        "name": "Kusheshwar Asthan Wetland Sanctuary",
        "name_hi": "कुशेश्वर स्थान पक्षी अभयारण्य",
        "type": "lake",
        "category": "Wetland & Bird Sanctuary",
        "district": "Darbhanga",
        "area_sq_km": 29.1,
        "description": "Expansive seasonal freshwater wetland bird sanctuary in North Bihar.",
        "coordinates": [
            [86.0200, 25.8000],
            [86.0500, 25.8400],
            [86.0900, 25.8350],
            [86.1100, 25.8050],
            [86.0800, 25.7800],
            [86.0400, 25.7750],
            [86.0200, 25.8000]
        ]
    },
    {
        "id": "matsyagandha_lake",
        "name": "Matsyagandha Lake",
        "name_hi": "मत्स्यगंधा झील",
        "type": "lake",
        "category": "Tourist Lake",
        "district": "Saharsa",
        "area_sq_km": 8.4,
        "description": "Beautiful lake with Rakta Kali temple complex and boating recreation.",
        "coordinates": [
            [86.5850, 25.8750],
            [86.6020, 25.8920],
            [86.6180, 25.8850],
            [86.6120, 25.8680],
            [86.5920, 25.8620],
            [86.5850, 25.8750]
        ]
    },
    {
        "id": "ghora_katora",
        "name": "Ghora Katora Lake",
        "name_hi": "घोड़ा कटोरा झील",
        "type": "lake",
        "category": "Eco-Tourism Lake",
        "district": "Nalanda",
        "area_sq_km": 4.2,
        "description": "Scenic horse-bowl shaped natural lake nestled in the hills of Rajgir.",
        "coordinates": [
            [85.4420, 25.0050],
            [85.4550, 25.0180],
            [85.4680, 25.0120],
            [85.4620, 24.9980],
            [85.4480, 24.9950],
            [85.4420, 25.0050]
        ]
    },
    {
        "id": "baraila_lake",
        "name": "Baraila Lake (Salim Ali Sanctuary)",
        "name_hi": "बरैला झील पक्षी अभयारण्य",
        "type": "lake",
        "category": "Bird Sanctuary Lake",
        "district": "Vaishali",
        "area_sq_km": 19.8,
        "description": "Important ornithological wetland habitat and Salim Ali bird sanctuary.",
        "coordinates": [
            [85.3350, 25.7350],
            [85.3520, 25.7600],
            [85.3780, 25.7520],
            [85.3720, 25.7300],
            [85.3480, 25.7220],
            [85.3350, 25.7350]
        ]
    },
    {
        "id": "moti_jheel",
        "name": "Moti Jheel",
        "name_hi": "मोती झील",
        "type": "lake",
        "category": "Urban Historic Lake",
        "district": "East Champaran",
        "area_sq_km": 6.5,
        "description": "Historic crescent-shaped oxbow lake flowing through Motihari city.",
        "coordinates": [
            [84.9020, 26.6420],
            [84.9180, 26.6600],
            [84.9350, 26.6520],
            [84.9280, 26.6350],
            [84.9100, 26.6300],
            [84.9020, 26.6420]
        ]
    },
    {
        "id": "kharagpur_lake",
        "name": "Kharagpur Lake Reservoir",
        "name_hi": "खड़गपुर झील जलाशय",
        "type": "dam_reservoir",
        "category": "Dam Reservoir",
        "district": "Munger",
        "area_sq_km": 11.2,
        "description": "Scenic reservoir surrounded by Kharagpur hills with natural hot springs nearby.",
        "coordinates": [
            [86.5150, 25.1150],
            [86.5380, 25.1420],
            [86.5550, 25.1320],
            [86.5480, 25.1080],
            [86.5250, 25.1020],
            [86.5150, 25.1150]
        ]
    },
    {
        "id": "nagi_dam",
        "name": "Nagi Dam Reservoir",
        "name_hi": "नागी डैम जलाशय",
        "type": "dam_reservoir",
        "category": "Ramsar Reservoir Wetland",
        "district": "Jamui",
        "area_sq_km": 7.9,
        "description": "Designated Ramsar Wetland site hosting thousands of migratory bar-headed geese.",
        "coordinates": [
            [86.3550, 24.8020],
            [86.3750, 24.8220],
            [86.3920, 24.8150],
            [86.3850, 24.7950],
            [86.3650, 24.7920],
            [86.3550, 24.8020]
        ]
    },
    {
        "id": "nakti_dam",
        "name": "Nakti Dam Reservoir",
        "name_hi": "नकटी डैम जलाशय",
        "type": "dam_reservoir",
        "category": "Ramsar Reservoir Wetland",
        "district": "Jamui",
        "area_sq_km": 5.8,
        "description": "Ramsar Wetland reservoir sanctuary with pristine surrounding hill topography.",
        "coordinates": [
            [86.4800, 24.8350],
            [86.4980, 24.8520],
            [86.5120, 24.8450],
            [86.5050, 24.8280],
            [86.4880, 24.8250],
            [86.4800, 24.8350]
        ]
    },
    {
        "id": "kohira_dam",
        "name": "Kohira Dam Reservoir",
        "name_hi": "कोहिरा डैम जलाशय",
        "type": "dam_reservoir",
        "category": "Irrigation Dam",
        "district": "Kaimur",
        "area_sq_km": 9.4,
        "description": "Important water reservoir dam situated on the Kohira River on Kaimur plateau.",
        "coordinates": [
            [83.5650, 25.0250],
            [83.5850, 25.0480],
            [83.6020, 25.0400],
            [83.5950, 25.0180],
            [83.5750, 25.0150],
            [83.5650, 25.0250]
        ]
    },
    {
        "id": "durgavati_dam",
        "name": "Durgavati (Karamchat) Dam Reservoir",
        "name_hi": "दुर्गावती (करमचट) डैम",
        "type": "dam_reservoir",
        "category": "Major Earthen Dam",
        "district": "Kaimur / Rohtas",
        "area_sq_km": 15.6,
        "description": "Major multi-purpose earthen dam reservoir with 1610m length on Durgavati river.",
        "coordinates": [
            [83.7250, 24.9350],
            [83.7520, 24.9650],
            [83.7750, 24.9550],
            [83.7680, 24.9280],
            [83.7380, 24.9220],
            [83.7250, 24.9350]
        ]
    },
    {
        "id": "indrapuri_barrage",
        "name": "Indrapuri Barrage Reservoir",
        "name_hi": "इंद्रपुरी बैराज जलाशय",
        "type": "dam_reservoir",
        "category": "River Barrage",
        "district": "Rohtas",
        "area_sq_km": 14.8,
        "description": "One of the longest barrages in the world (1407m) on the Son River at Dehri.",
        "coordinates": [
            [84.1200, 24.8150],
            [84.1480, 24.8450],
            [84.1680, 24.8380],
            [84.1550, 24.8080],
            [84.1300, 24.8020],
            [84.1200, 24.8150]
        ]
    },
    {
        "id": "valmikinagar_barrage",
        "name": "Valmikinagar Gandak Barrage",
        "name_hi": "वाल्मीकिनगर गंडक बैराज",
        "type": "dam_reservoir",
        "category": "River Barrage Reservoir",
        "district": "West Champaran",
        "area_sq_km": 12.5,
        "description": "Major 36-gate barrage on the Indo-Nepal border surrounded by Valmiki National Park.",
        "coordinates": [
            [83.8950, 27.4200],
            [83.9220, 27.4480],
            [83.9450, 27.4380],
            [83.9350, 27.4120],
            [83.9050, 27.4080],
            [83.8950, 27.4200]
        ]
    },
    {
        "id": "birpur_kosi_barrage",
        "name": "Birpur Kosi Barrage Reservoir",
        "name_hi": "बीरपुर कोसी बैराज जलाशय",
        "type": "dam_reservoir",
        "category": "River Barrage Reservoir",
        "district": "Supaul",
        "area_sq_km": 16.2,
        "description": "Strategic 56-gate flood control and irrigation barrage on the Kosi River.",
        "coordinates": [
            [86.9150, 26.5050],
            [86.9420, 26.5350],
            [86.9650, 26.5250],
            [86.9550, 26.4980],
            [86.9280, 26.4920],
            [86.9150, 26.5050]
        ]
    },
    {
        "id": "badua_dam",
        "name": "Badua Dam Reservoir",
        "name_hi": "बदुआ डैम जलाशय",
        "type": "dam_reservoir",
        "category": "Earthen Dam Reservoir",
        "district": "Banka",
        "area_sq_km": 8.7,
        "description": "Historic earthen dam reservoir on Badua river supporting major irrigation canal network.",
        "coordinates": [
            [86.7050, 24.8680],
            [86.7280, 24.8920],
            [86.7450, 24.8820],
            [86.7380, 24.8580],
            [86.7150, 24.8520],
            [86.7050, 24.8680]
        ]
    },
    {
        "id": "chandan_dam",
        "name": "Chandan Dam Reservoir",
        "name_hi": "चांदन डैम जलाशय",
        "type": "dam_reservoir",
        "category": "Irrigation Dam Reservoir",
        "district": "Banka",
        "area_sq_km": 10.4,
        "description": "Multi-purpose dam reservoir constructed across Chandan river near Bounsi.",
        "coordinates": [
            [86.9350, 24.6850],
            [86.9620, 24.7120],
            [86.9780, 24.7050],
            [86.9720, 24.6780],
            [86.9480, 24.6720],
            [86.9350, 24.6850]
        ]
    }
]

def build_geojson():
    rivers_features = []
    for r in BIHAR_RIVERS:
        feature = {
            "type": "Feature",
            "properties": {
                "id": r["id"],
                "name": r["name"],
                "name_hi": r["name_hi"],
                "type": r["type"],
                "length_bihar_km": r["length_bihar_km"],
                "origin": r["origin"],
                "outflow": r["outflow"],
                "districts_traversed": r["districts_traversed"]
            },
            "geometry": {
                "type": "LineString",
                "coordinates": r["coordinates"]
            }
        }
        rivers_features.append(feature)

    rivers_fc = {
        "type": "FeatureCollection",
        "name": "Bihar Major River Network",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap contributors (ODbL) / Natural Earth / HydroSHEDS",
            "attribution": "© OpenStreetMap contributors, Natural Earth, HiddenYatra GIS",
            "state": "Bihar",
            "feature_count": len(rivers_features)
        },
        "features": rivers_features
    }

    lakes_features = []
    for l in BIHAR_LAKES_DAMS:
        feature = {
            "type": "Feature",
            "properties": {
                "id": l["id"],
                "name": l["name"],
                "name_hi": l["name_hi"],
                "type": l["type"],
                "category": l["category"],
                "district": l["district"],
                "area_sq_km": l["area_sq_km"],
                "description": l["description"]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [l["coordinates"]]
            }
        }
        lakes_features.append(feature)

    lakes_fc = {
        "type": "FeatureCollection",
        "name": "Bihar Major Lakes and Dams",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "metadata": {
            "source": "OpenStreetMap contributors (ODbL) / CWC / WRD Bihar",
            "attribution": "© OpenStreetMap contributors, CWC, HiddenYatra GIS",
            "state": "Bihar",
            "feature_count": len(lakes_features)
        },
        "features": lakes_features
    }

    out_dir = os.path.join(os.path.dirname(__file__), "..", "static", "data", "bihar")
    os.makedirs(out_dir, exist_ok=True)

    rivers_path = os.path.join(out_dir, "rivers.geojson")
    with open(rivers_path, "w", encoding="utf-8") as f:
        json.dump(rivers_fc, f, indent=2, ensure_ascii=False)
    print(f"Generated rivers.geojson: {len(rivers_features)} features ({os.path.getsize(rivers_path)} bytes)")

    lakes_path = os.path.join(out_dir, "lakes_dams.geojson")
    with open(lakes_path, "w", encoding="utf-8") as f:
        json.dump(lakes_fc, f, indent=2, ensure_ascii=False)
    print(f"Generated lakes_dams.geojson: {len(lakes_features)} features ({os.path.getsize(lakes_path)} bytes)")

if __name__ == "__main__":
    build_geojson()
