"""
Smart Plant Species Botanical Profiles & Agronomic Thresholds
Defines optimal environmental parameters, moisture thresholds, and botanical rationale
for precision cloud irrigation across plant families.
"""

from typing import Dict, Any, List

PLANT_PROFILES: Dict[str, Dict[str, Any]] = {
    "TOMATO": {
        "common_name": "Tomato (Solanum lycopersicum)",
        "default_threshold": 40.0,
        "recommended_min_moisture": 35.0,
        "recommended_max_moisture": 75.0,
        "ideal_temp_min": 18.0,
        "ideal_temp_max": 32.0,
        "ideal_humidity_min": 50.0,
        "ideal_humidity_max": 75.0,
        "watering_duration_seconds": 8,
        "botanical_rationale": (
            "Tomatoes require consistent, deep moisture during fruit formation. "
            "Erratic moisture cycles cause blossom end rot and fruit splitting."
        ),
        "icon": "🍅"
    },
    "SUCCULENT": {
        "common_name": "Succulent / Cactus (Echeveria, Aloe, Haworthia)",
        "default_threshold": 20.0,
        "recommended_min_moisture": 15.0,
        "recommended_max_moisture": 45.0,
        "ideal_temp_min": 15.0,
        "ideal_temp_max": 35.0,
        "ideal_humidity_min": 25.0,
        "ideal_humidity_max": 50.0,
        "watering_duration_seconds": 3,
        "botanical_rationale": (
            "Desert xerophytes store water in flesh parenchyma tissues. "
            "Excessive moisture or poor drainage rapidly leads to lethal fungal root rot."
        ),
        "icon": "🌵"
    },
    "HERB": {
        "common_name": "Herbs (Basil, Mint, Oregano, Cilantro)",
        "default_threshold": 35.0,
        "recommended_min_moisture": 30.0,
        "recommended_max_moisture": 70.0,
        "ideal_temp_min": 16.0,
        "ideal_temp_max": 30.0,
        "ideal_humidity_min": 45.0,
        "ideal_humidity_max": 70.0,
        "watering_duration_seconds": 5,
        "botanical_rationale": (
            "Culinary herbs require aerated, moderately moist loam. "
            "Too dry causes early flowering (bolting), while waterlogging dilutes essential oils."
        ),
        "icon": "🌿"
    },
    "INDOOR PLANT": {
        "common_name": "Foliage Houseplant (Snake Plant, Pothos, Peace Lily)",
        "default_threshold": 30.0,
        "recommended_min_moisture": 25.0,
        "recommended_max_moisture": 65.0,
        "ideal_temp_min": 18.0,
        "ideal_temp_max": 28.0,
        "ideal_humidity_min": 40.0,
        "ideal_humidity_max": 65.0,
        "watering_duration_seconds": 5,
        "botanical_rationale": (
            "Indoor microclimates have lower transpiration rates due to reduced air velocity. "
            "A balanced 30% threshold maintains vibrant green leaf turgor without mold growth."
        ),
        "icon": "🪴"
    },
    "TROPICAL": {
        "common_name": "Tropical Rainforest (Monstera, Fern, Calathea)",
        "default_threshold": 50.0,
        "recommended_min_moisture": 45.0,
        "recommended_max_moisture": 85.0,
        "ideal_temp_min": 20.0,
        "ideal_temp_max": 32.0,
        "ideal_humidity_min": 60.0,
        "ideal_humidity_max": 90.0,
        "watering_duration_seconds": 7,
        "botanical_rationale": (
            "Understory tropical species thrive in high ambient humidity and damp organic substrate. "
            "Dry soil causes leaf tip necrosis and curled fronds."
        ),
        "icon": "🌴"
    },
    "BONSAI": {
        "common_name": "Bonsai Tree (Ficus, Juniper, Elm)",
        "default_threshold": 45.0,
        "recommended_min_moisture": 40.0,
        "recommended_max_moisture": 75.0,
        "ideal_temp_min": 15.0,
        "ideal_temp_max": 28.0,
        "ideal_humidity_min": 50.0,
        "ideal_humidity_max": 80.0,
        "watering_duration_seconds": 4,
        "botanical_rationale": (
            "Shallow bonsai pots hold extremely limited soil volume with fast drying times. "
            "Frequent, gentle irrigation is vital to prevent root desiccation."
        ),
        "icon": "🎋"
    }
}


def get_plant_profile(plant_type: str) -> Dict[str, Any]:
    """Retrieve botanical profile for given species key, with fallback to INDOOR PLANT."""
    key = plant_type.upper().strip()
    return PLANT_PROFILES.get(key, PLANT_PROFILES["INDOOR PLANT"])


def list_available_profiles() -> List[Dict[str, Any]]:
    """Return all configured species profiles for UI selection dropdowns."""
    results = []
    for key, data in PLANT_PROFILES.items():
        results.append({
            "key": key,
            "name": data["common_name"],
            "threshold": data["default_threshold"],
            "duration": data["watering_duration_seconds"],
            "icon": data["icon"],
            "rationale": data["botanical_rationale"]
        })
    return results
