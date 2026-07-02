"""City coordinates and route definitions for all of Northeast India.

Covers all 8 NE states:
  - Arunachal Pradesh (Itanagar)
  - Assam (Guwahati, Silchar, Tezpur, Jorhat, Dibrugarh)
  - Manipur (Imphal)
  - Meghalaya (Shillong)
  - Mizoram (Aizawl)
  - Nagaland (Kohima, Dimapur)
  - Sikkim (Gangtok)
  - Tripura (Agartala)
"""

# ──────────────── All NE India Cities ────────────────

CITIES = {
    # Mizoram
    "Aizawl": {"lat": 23.7271, "lng": 92.7176, "state": "Mizoram", "elevation": 1132},
    # Assam
    "Silchar": {"lat": 24.8333, "lng": 92.7789, "state": "Assam", "elevation": 35},
    "Guwahati": {"lat": 26.1445, "lng": 91.7362, "state": "Assam", "elevation": 55},
    "Tezpur": {"lat": 26.6338, "lng": 92.8006, "state": "Assam", "elevation": 48},
    "Jorhat": {"lat": 26.7509, "lng": 94.2037, "state": "Assam", "elevation": 116},
    "Dibrugarh": {"lat": 27.4728, "lng": 94.9120, "state": "Assam", "elevation": 108},
    # Manipur
    "Imphal": {"lat": 24.8170, "lng": 93.9368, "state": "Manipur", "elevation": 786},
    # Meghalaya
    "Shillong": {"lat": 25.5788, "lng": 91.8933, "state": "Meghalaya", "elevation": 1496},
    # Nagaland
    "Kohima": {"lat": 25.6751, "lng": 94.1086, "state": "Nagaland", "elevation": 1444},
    "Dimapur": {"lat": 25.9065, "lng": 93.7272, "state": "Nagaland", "elevation": 260},
    # Tripura
    "Agartala": {"lat": 23.8315, "lng": 91.2868, "state": "Tripura", "elevation": 16},
    # Arunachal Pradesh
    "Itanagar": {"lat": 27.0844, "lng": 93.6053, "state": "Arunachal Pradesh", "elevation": 440},
    # Sikkim
    "Gangtok": {"lat": 27.3389, "lng": 88.6065, "state": "Sikkim", "elevation": 1650},
}


# ──────────────── All NE India Routes ────────────────

ROUTES = {
    # ═══════════ EXISTING ROUTES (Mizoram / South Assam) ═══════════

    "aizawl-silchar": {
        "from": "Aizawl",
        "to": "Silchar",
        "distance_km": 180,
        "estimated_time": "6-7 hours",
        "risk_factors": ["Heavy rainfall zone", "Steep terrain", "Mountain roads"],
        "segments": [
            {
                "from": {"name": "Aizawl", "lat": 23.7271, "lng": 92.7176},
                "to": {"name": "Vairengte", "lat": 24.2637, "lng": 92.7915},
                "slope": 32, "max_elevation": 1132, "road_type": 1,
                "historical_blockages": 12, "length_km": 65,
            },
            {
                "from": {"name": "Vairengte", "lat": 24.2637, "lng": 92.7915},
                "to": {"name": "Lailapur", "lat": 24.6120, "lng": 92.7547},
                "slope": 28, "max_elevation": 800, "road_type": 1,
                "historical_blockages": 8, "length_km": 55,
            },
            {
                "from": {"name": "Lailapur", "lat": 24.6120, "lng": 92.7547},
                "to": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "slope": 18, "max_elevation": 350, "road_type": 0,
                "historical_blockages": 3, "length_km": 60,
            },
        ],
    },

    "aizawl-guwahati": {
        "from": "Aizawl",
        "to": "Guwahati",
        "distance_km": 480,
        "estimated_time": "14-16 hours",
        "risk_factors": ["Landslide prone", "Long route", "Multiple terrain types"],
        "segments": [
            {
                "from": {"name": "Aizawl", "lat": 23.7271, "lng": 92.7176},
                "to": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "slope": 30, "max_elevation": 1132, "road_type": 1,
                "historical_blockages": 10, "length_km": 180,
            },
            {
                "from": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "to": {"name": "Haflong", "lat": 25.1656, "lng": 93.0170},
                "slope": 35, "max_elevation": 680, "road_type": 1,
                "historical_blockages": 15, "length_km": 80,
            },
            {
                "from": {"name": "Haflong", "lat": 25.1656, "lng": 93.0170},
                "to": {"name": "Lumding", "lat": 25.7500, "lng": 93.1667},
                "slope": 22, "max_elevation": 450, "road_type": 1,
                "historical_blockages": 7, "length_km": 60,
            },
            {
                "from": {"name": "Lumding", "lat": 25.7500, "lng": 93.1667},
                "to": {"name": "Guwahati", "lat": 26.1445, "lng": 91.7362},
                "slope": 10, "max_elevation": 60, "road_type": 0,
                "historical_blockages": 2, "length_km": 160,
            },
        ],
    },

    "imphal-guwahati": {
        "from": "Imphal",
        "to": "Guwahati",
        "distance_km": 450,
        "estimated_time": "12-14 hours",
        "risk_factors": ["NH-2 landslide zones", "Very steep terrain", "Remote areas"],
        "segments": [
            {
                "from": {"name": "Imphal", "lat": 24.8170, "lng": 93.9368},
                "to": {"name": "Kohima", "lat": 25.6751, "lng": 94.1086},
                "slope": 38, "max_elevation": 1500, "road_type": 1,
                "historical_blockages": 18, "length_km": 140,
            },
            {
                "from": {"name": "Kohima", "lat": 25.6751, "lng": 94.1086},
                "to": {"name": "Dimapur", "lat": 25.9065, "lng": 93.7272},
                "slope": 25, "max_elevation": 1261, "road_type": 1,
                "historical_blockages": 10, "length_km": 70,
            },
            {
                "from": {"name": "Dimapur", "lat": 25.9065, "lng": 93.7272},
                "to": {"name": "Guwahati", "lat": 26.1445, "lng": 91.7362},
                "slope": 8, "max_elevation": 60, "road_type": 0,
                "historical_blockages": 2, "length_km": 240,
            },
        ],
    },

    "shillong-guwahati": {
        "from": "Shillong",
        "to": "Guwahati",
        "distance_km": 100,
        "estimated_time": "2.5-3 hours",
        "risk_factors": ["Fog prone", "Steep curves", "Heavy traffic"],
        "segments": [
            {
                "from": {"name": "Shillong", "lat": 25.5788, "lng": 91.8933},
                "to": {"name": "Nongpoh", "lat": 25.9167, "lng": 91.8833},
                "slope": 22, "max_elevation": 1496, "road_type": 0,
                "historical_blockages": 5, "length_km": 50,
            },
            {
                "from": {"name": "Nongpoh", "lat": 25.9167, "lng": 91.8833},
                "to": {"name": "Guwahati", "lat": 26.1445, "lng": 91.7362},
                "slope": 15, "max_elevation": 600, "road_type": 0,
                "historical_blockages": 2, "length_km": 50,
            },
        ],
    },

    "agartala-silchar": {
        "from": "Agartala",
        "to": "Silchar",
        "distance_km": 170,
        "estimated_time": "5-6 hours",
        "risk_factors": ["Flooding prone", "Low-lying areas", "River crossings"],
        "segments": [
            {
                "from": {"name": "Agartala", "lat": 23.8315, "lng": 91.2868},
                "to": {"name": "Karimganj", "lat": 24.8649, "lng": 92.3560},
                "slope": 12, "max_elevation": 300, "road_type": 0,
                "historical_blockages": 6, "length_km": 80,
            },
            {
                "from": {"name": "Karimganj", "lat": 24.8649, "lng": 92.3560},
                "to": {"name": "Badarpur", "lat": 24.8686, "lng": 92.5967},
                "slope": 8, "max_elevation": 200, "road_type": 0,
                "historical_blockages": 9, "length_km": 50,
            },
            {
                "from": {"name": "Badarpur", "lat": 24.8686, "lng": 92.5967},
                "to": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "slope": 10, "max_elevation": 350, "road_type": 0,
                "historical_blockages": 4, "length_km": 40,
            },
        ],
    },

    "imphal-silchar": {
        "from": "Imphal",
        "to": "Silchar",
        "distance_km": 200,
        "estimated_time": "7-8 hours",
        "risk_factors": ["Mountain roads", "Heavy rainfall", "Landslide zones"],
        "segments": [
            {
                "from": {"name": "Imphal", "lat": 24.8170, "lng": 93.9368},
                "to": {"name": "Bishnupur", "lat": 24.6281, "lng": 93.7650},
                "slope": 25, "max_elevation": 900, "road_type": 1,
                "historical_blockages": 14, "length_km": 30,
            },
            {
                "from": {"name": "Bishnupur", "lat": 24.6281, "lng": 93.7650},
                "to": {"name": "Churachandpur", "lat": 24.3333, "lng": 93.6833},
                "slope": 35, "max_elevation": 1200, "road_type": 1,
                "historical_blockages": 16, "length_km": 50,
            },
            {
                "from": {"name": "Churachandpur", "lat": 24.3333, "lng": 93.6833},
                "to": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "slope": 30, "max_elevation": 350, "road_type": 1,
                "historical_blockages": 8, "length_km": 120,
            },
        ],
    },

    # ═══════════ NEW: NAGALAND ROUTES ═══════════

    "dimapur-kohima": {
        "from": "Dimapur",
        "to": "Kohima",
        "distance_km": 74,
        "estimated_time": "2.5-3 hours",
        "risk_factors": ["Extremely steep ascent", "Narrow mountain road", "Landslide zone"],
        "segments": [
            {
                "from": {"name": "Dimapur", "lat": 25.9065, "lng": 93.7272},
                "to": {"name": "Chumukedima", "lat": 25.8500, "lng": 93.7500},
                "slope": 15, "max_elevation": 400, "road_type": 0,
                "historical_blockages": 4, "length_km": 20,
            },
            {
                "from": {"name": "Chumukedima", "lat": 25.8500, "lng": 93.7500},
                "to": {"name": "Zubza", "lat": 25.7200, "lng": 94.0000},
                "slope": 35, "max_elevation": 1100, "road_type": 1,
                "historical_blockages": 12, "length_km": 30,
            },
            {
                "from": {"name": "Zubza", "lat": 25.7200, "lng": 94.0000},
                "to": {"name": "Kohima", "lat": 25.6751, "lng": 94.1086},
                "slope": 30, "max_elevation": 1444, "road_type": 1,
                "historical_blockages": 9, "length_km": 24,
            },
        ],
    },

    "kohima-imphal": {
        "from": "Kohima",
        "to": "Imphal",
        "distance_km": 135,
        "estimated_time": "4-5 hours",
        "risk_factors": ["NH-2 most dangerous stretch", "Steep terrain", "Armed conflict zones"],
        "segments": [
            {
                "from": {"name": "Kohima", "lat": 25.6751, "lng": 94.1086},
                "to": {"name": "Mao", "lat": 25.3500, "lng": 94.1000},
                "slope": 33, "max_elevation": 1500, "road_type": 1,
                "historical_blockages": 15, "length_km": 50,
            },
            {
                "from": {"name": "Mao", "lat": 25.3500, "lng": 94.1000},
                "to": {"name": "Senapati", "lat": 25.0700, "lng": 94.0200},
                "slope": 28, "max_elevation": 1200, "road_type": 1,
                "historical_blockages": 11, "length_km": 40,
            },
            {
                "from": {"name": "Senapati", "lat": 25.0700, "lng": 94.0200},
                "to": {"name": "Imphal", "lat": 24.8170, "lng": 93.9368},
                "slope": 20, "max_elevation": 786, "road_type": 1,
                "historical_blockages": 6, "length_km": 45,
            },
        ],
    },

    # ═══════════ NEW: ASSAM CORRIDOR (NH-37 / NH-27) ═══════════

    "guwahati-tezpur": {
        "from": "Guwahati",
        "to": "Tezpur",
        "distance_km": 180,
        "estimated_time": "3.5-4 hours",
        "risk_factors": ["Brahmaputra flood plain", "Fog in winter", "Heavy traffic"],
        "segments": [
            {
                "from": {"name": "Guwahati", "lat": 26.1445, "lng": 91.7362},
                "to": {"name": "Nagaon", "lat": 26.3500, "lng": 92.6840},
                "slope": 5, "max_elevation": 65, "road_type": 0,
                "historical_blockages": 3, "length_km": 120,
            },
            {
                "from": {"name": "Nagaon", "lat": 26.3500, "lng": 92.6840},
                "to": {"name": "Tezpur", "lat": 26.6338, "lng": 92.8006},
                "slope": 6, "max_elevation": 55, "road_type": 0,
                "historical_blockages": 4, "length_km": 60,
            },
        ],
    },

    "guwahati-jorhat": {
        "from": "Guwahati",
        "to": "Jorhat",
        "distance_km": 310,
        "estimated_time": "6-7 hours",
        "risk_factors": ["Flood-prone areas", "Long highway stretch", "Kaziranga wildlife zone"],
        "segments": [
            {
                "from": {"name": "Guwahati", "lat": 26.1445, "lng": 91.7362},
                "to": {"name": "Nagaon", "lat": 26.3500, "lng": 92.6840},
                "slope": 5, "max_elevation": 65, "road_type": 0,
                "historical_blockages": 3, "length_km": 120,
            },
            {
                "from": {"name": "Nagaon", "lat": 26.3500, "lng": 92.6840},
                "to": {"name": "Bokakhat", "lat": 26.6200, "lng": 93.6000},
                "slope": 4, "max_elevation": 70, "road_type": 0,
                "historical_blockages": 5, "length_km": 110,
            },
            {
                "from": {"name": "Bokakhat", "lat": 26.6200, "lng": 93.6000},
                "to": {"name": "Jorhat", "lat": 26.7509, "lng": 94.2037},
                "slope": 5, "max_elevation": 116, "road_type": 0,
                "historical_blockages": 4, "length_km": 80,
            },
        ],
    },

    "jorhat-dibrugarh": {
        "from": "Jorhat",
        "to": "Dibrugarh",
        "distance_km": 130,
        "estimated_time": "2.5-3 hours",
        "risk_factors": ["River flooding", "Tea garden area roads", "Seasonal fog"],
        "segments": [
            {
                "from": {"name": "Jorhat", "lat": 26.7509, "lng": 94.2037},
                "to": {"name": "Sibsagar", "lat": 26.9840, "lng": 94.6380},
                "slope": 4, "max_elevation": 95, "road_type": 0,
                "historical_blockages": 3, "length_km": 60,
            },
            {
                "from": {"name": "Sibsagar", "lat": 26.9840, "lng": 94.6380},
                "to": {"name": "Dibrugarh", "lat": 27.4728, "lng": 94.9120},
                "slope": 5, "max_elevation": 108, "road_type": 0,
                "historical_blockages": 4, "length_km": 70,
            },
        ],
    },

    # ═══════════ NEW: ARUNACHAL PRADESH ROUTES ═══════════

    "tezpur-itanagar": {
        "from": "Tezpur",
        "to": "Itanagar",
        "distance_km": 280,
        "estimated_time": "8-10 hours",
        "risk_factors": ["Mountain roads", "River crossings", "Remote terrain", "Landslide zones"],
        "segments": [
            {
                "from": {"name": "Tezpur", "lat": 26.6338, "lng": 92.8006},
                "to": {"name": "Bhalukpong", "lat": 27.0167, "lng": 92.6500},
                "slope": 18, "max_elevation": 200, "road_type": 0,
                "historical_blockages": 6, "length_km": 60,
            },
            {
                "from": {"name": "Bhalukpong", "lat": 27.0167, "lng": 92.6500},
                "to": {"name": "Bomdila", "lat": 27.2645, "lng": 92.4214},
                "slope": 40, "max_elevation": 2400, "road_type": 1,
                "historical_blockages": 20, "length_km": 100,
            },
            {
                "from": {"name": "Bomdila", "lat": 27.2645, "lng": 92.4214},
                "to": {"name": "Itanagar", "lat": 27.0844, "lng": 93.6053},
                "slope": 30, "max_elevation": 1800, "road_type": 1,
                "historical_blockages": 14, "length_km": 120,
            },
        ],
    },

    "dibrugarh-itanagar": {
        "from": "Dibrugarh",
        "to": "Itanagar",
        "distance_km": 480,
        "estimated_time": "12-14 hours",
        "risk_factors": ["Remote mountain roads", "River flooding", "Limited rescue access"],
        "segments": [
            {
                "from": {"name": "Dibrugarh", "lat": 27.4728, "lng": 94.9120},
                "to": {"name": "North Lakhimpur", "lat": 27.2353, "lng": 94.1047},
                "slope": 6, "max_elevation": 100, "road_type": 0,
                "historical_blockages": 5, "length_km": 110,
            },
            {
                "from": {"name": "North Lakhimpur", "lat": 27.2353, "lng": 94.1047},
                "to": {"name": "Ziro", "lat": 27.5883, "lng": 93.8311},
                "slope": 35, "max_elevation": 1780, "road_type": 1,
                "historical_blockages": 16, "length_km": 120,
            },
            {
                "from": {"name": "Ziro", "lat": 27.5883, "lng": 93.8311},
                "to": {"name": "Daporijo", "lat": 27.9833, "lng": 93.8833},
                "slope": 32, "max_elevation": 1600, "road_type": 1,
                "historical_blockages": 18, "length_km": 130,
            },
            {
                "from": {"name": "Daporijo", "lat": 27.9833, "lng": 93.8833},
                "to": {"name": "Itanagar", "lat": 27.0844, "lng": 93.6053},
                "slope": 28, "max_elevation": 1200, "road_type": 1,
                "historical_blockages": 12, "length_km": 120,
            },
        ],
    },

    # ═══════════ NEW: SIKKIM ROUTE ═══════════

    "guwahati-gangtok": {
        "from": "Guwahati",
        "to": "Gangtok",
        "distance_km": 560,
        "estimated_time": "14-16 hours",
        "risk_factors": ["Mountain passes", "Teesta river valley", "Heavy monsoon rainfall", "Long route"],
        "segments": [
            {
                "from": {"name": "Guwahati", "lat": 26.1445, "lng": 91.7362},
                "to": {"name": "Cooch Behar", "lat": 26.3252, "lng": 89.4482},
                "slope": 4, "max_elevation": 50, "road_type": 0,
                "historical_blockages": 3, "length_km": 200,
            },
            {
                "from": {"name": "Cooch Behar", "lat": 26.3252, "lng": 89.4482},
                "to": {"name": "Siliguri", "lat": 26.7271, "lng": 88.3953},
                "slope": 5, "max_elevation": 130, "road_type": 0,
                "historical_blockages": 2, "length_km": 140,
            },
            {
                "from": {"name": "Siliguri", "lat": 26.7271, "lng": 88.3953},
                "to": {"name": "Rangpo", "lat": 27.1753, "lng": 88.5333},
                "slope": 28, "max_elevation": 800, "road_type": 1,
                "historical_blockages": 10, "length_km": 100,
            },
            {
                "from": {"name": "Rangpo", "lat": 27.1753, "lng": 88.5333},
                "to": {"name": "Gangtok", "lat": 27.3389, "lng": 88.6065},
                "slope": 35, "max_elevation": 1650, "road_type": 1,
                "historical_blockages": 14, "length_km": 120,
            },
        ],
    },

    # ═══════════ NEW: CROSS-STATE CONNECTORS ═══════════

    "silchar-shillong": {
        "from": "Silchar",
        "to": "Shillong",
        "distance_km": 330,
        "estimated_time": "9-11 hours",
        "risk_factors": ["Mountain roads", "Jaintia Hills", "Heavy rainfall zone"],
        "segments": [
            {
                "from": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "to": {"name": "Haflong", "lat": 25.1656, "lng": 93.0170},
                "slope": 28, "max_elevation": 680, "road_type": 1,
                "historical_blockages": 12, "length_km": 80,
            },
            {
                "from": {"name": "Haflong", "lat": 25.1656, "lng": 93.0170},
                "to": {"name": "Jowai", "lat": 25.4520, "lng": 92.2030},
                "slope": 25, "max_elevation": 1380, "road_type": 1,
                "historical_blockages": 10, "length_km": 130,
            },
            {
                "from": {"name": "Jowai", "lat": 25.4520, "lng": 92.2030},
                "to": {"name": "Shillong", "lat": 25.5788, "lng": 91.8933},
                "slope": 20, "max_elevation": 1496, "road_type": 0,
                "historical_blockages": 6, "length_km": 120,
            },
        ],
    },

    "agartala-guwahati": {
        "from": "Agartala",
        "to": "Guwahati",
        "distance_km": 590,
        "estimated_time": "16-18 hours",
        "risk_factors": ["Very long route", "Flooding", "Mountain passes", "Multiple states"],
        "segments": [
            {
                "from": {"name": "Agartala", "lat": 23.8315, "lng": 91.2868},
                "to": {"name": "Karimganj", "lat": 24.8649, "lng": 92.3560},
                "slope": 12, "max_elevation": 300, "road_type": 0,
                "historical_blockages": 6, "length_km": 130,
            },
            {
                "from": {"name": "Karimganj", "lat": 24.8649, "lng": 92.3560},
                "to": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "slope": 8, "max_elevation": 200, "road_type": 0,
                "historical_blockages": 7, "length_km": 90,
            },
            {
                "from": {"name": "Silchar", "lat": 24.8333, "lng": 92.7789},
                "to": {"name": "Shillong", "lat": 25.5788, "lng": 91.8933},
                "slope": 25, "max_elevation": 1496, "road_type": 1,
                "historical_blockages": 11, "length_km": 270,
            },
            {
                "from": {"name": "Shillong", "lat": 25.5788, "lng": 91.8933},
                "to": {"name": "Guwahati", "lat": 26.1445, "lng": 91.7362},
                "slope": 18, "max_elevation": 1496, "road_type": 0,
                "historical_blockages": 4, "length_km": 100,
            },
        ],
    },

    "jorhat-kohima": {
        "from": "Jorhat",
        "to": "Kohima",
        "distance_km": 190,
        "estimated_time": "6-7 hours",
        "risk_factors": ["Mountain ascent", "Narrow roads", "Remote sections"],
        "segments": [
            {
                "from": {"name": "Jorhat", "lat": 26.7509, "lng": 94.2037},
                "to": {"name": "Mariani", "lat": 26.6600, "lng": 94.3100},
                "slope": 5, "max_elevation": 120, "road_type": 0,
                "historical_blockages": 2, "length_km": 30,
            },
            {
                "from": {"name": "Mariani", "lat": 26.6600, "lng": 94.3100},
                "to": {"name": "Wokha", "lat": 26.1000, "lng": 94.2700},
                "slope": 30, "max_elevation": 1310, "road_type": 1,
                "historical_blockages": 13, "length_km": 80,
            },
            {
                "from": {"name": "Wokha", "lat": 26.1000, "lng": 94.2700},
                "to": {"name": "Kohima", "lat": 25.6751, "lng": 94.1086},
                "slope": 28, "max_elevation": 1444, "road_type": 1,
                "historical_blockages": 10, "length_km": 80,
            },
        ],
    },

    "dimapur-jorhat": {
        "from": "Dimapur",
        "to": "Jorhat",
        "distance_km": 150,
        "estimated_time": "3.5-4 hours",
        "risk_factors": ["Naga Hills foothills", "River crossings", "Seasonal flooding"],
        "segments": [
            {
                "from": {"name": "Dimapur", "lat": 25.9065, "lng": 93.7272},
                "to": {"name": "Golaghat", "lat": 26.5220, "lng": 93.9600},
                "slope": 10, "max_elevation": 100, "road_type": 0,
                "historical_blockages": 4, "length_km": 80,
            },
            {
                "from": {"name": "Golaghat", "lat": 26.5220, "lng": 93.9600},
                "to": {"name": "Jorhat", "lat": 26.7509, "lng": 94.2037},
                "slope": 6, "max_elevation": 116, "road_type": 0,
                "historical_blockages": 3, "length_km": 70,
            },
        ],
    },
}


# ──────────────── Helper Functions ────────────────

def get_cities():
    """Get all cities with their data."""
    return [{"name": name, **data} for name, data in CITIES.items()]


def get_routes():
    """Get all available routes."""
    return [{"id": route_id, **data} for route_id, data in ROUTES.items()]


def get_route(from_city: str, to_city: str):
    """Find a route between two cities (supports reverse direction)."""
    # Try direct match
    route_id = f"{from_city.lower()}-{to_city.lower()}"
    if route_id in ROUTES:
        return {"id": route_id, **ROUTES[route_id]}

    # Try reverse match
    route_id = f"{to_city.lower()}-{from_city.lower()}"
    if route_id in ROUTES:
        route = ROUTES[route_id]
        reversed_segments = []
        for seg in reversed(route["segments"]):
            reversed_segments.append({
                "from": seg["to"],
                "to": seg["from"],
                "slope": seg["slope"],
                "max_elevation": seg["max_elevation"],
                "road_type": seg["road_type"],
                "historical_blockages": seg["historical_blockages"],
                "length_km": seg["length_km"],
            })
        return {
            "id": route_id + "-reversed",
            "from": from_city,
            "to": to_city,
            "distance_km": route["distance_km"],
            "estimated_time": route["estimated_time"],
            "risk_factors": route["risk_factors"],
            "segments": reversed_segments,
        }
    return None


def get_available_routes_for_city(city_name: str):
    """Get all cities reachable from a given city."""
    available = set()
    for route_id, route in ROUTES.items():
        if route["from"] == city_name:
            available.add(route["to"])
        elif route["to"] == city_name:
            available.add(route["from"])
    return sorted(available)
