"""
IoT Sensor Simulator Configuration
Configures simulated telemetry intervals, physical drying/watering rates, and cloud API endpoints.
"""

import os

# Cloud Backend API Endpoint
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
INGEST_ENDPOINT = f"{BACKEND_URL}/api/sensors/data"

# IoT Node Identity
DEVICE_ID = os.getenv("DEVICE_ID", "PLANT-001")
DEVICE_API_KEY = os.getenv("DEVICE_API_KEY", "plant-iot-cloud-api-key-998877")

# Telemetry Frequency (seconds between simulated sensor transmissions)
SEND_INTERVAL_SECONDS = float(os.getenv("SEND_INTERVAL_SECONDS", "3.0"))

# Simulation Physics Parameters
INITIAL_SOIL_MOISTURE = float(os.getenv("INITIAL_SOIL_MOISTURE", "52.0"))  # %
DRYING_RATE_PER_TICK = float(os.getenv("DRYING_RATE_PER_TICK", "1.2"))     # % moisture loss per tick
WATERING_BOOST_PER_TICK = float(os.getenv("WATERING_BOOST_PER_TICK", "6.5"))  # % moisture increase when watering
MOISTURE_TARGET_AFTER_WATER = 58.0                                          # % target level before pump shuts off

# Environmental bounds
TEMP_BASE = 26.0       # °C
TEMP_VARIATION = 5.0   # ± °C
HUMIDITY_BASE = 62.0   # %
HUMIDITY_VARIATION = 12.0

# Network & Fault Tolerance Settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "false").lower() in ("true", "1", "yes")
