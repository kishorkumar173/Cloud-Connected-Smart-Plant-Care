"""Automation package exports."""
from automation.watering_engine import WateringEngine
from automation.plant_profiles import PLANT_PROFILES, get_plant_profile, list_available_profiles

__all__ = ["WateringEngine", "PLANT_PROFILES", "get_plant_profile", "list_available_profiles"]
