"""
Python Virtual IoT Sensor Simulator
Simulates a physical IoT hardware node (e.g., ESP32 connected to Capacitive Soil Moisture Sensor,
DHT22 Temp/Humidity Sensor, Light Dependent Resistor, and Submersible Water Pump Relay).
Features realistic diurnal physics, gradual drying curves, cloud pump feedback actuation,
resilient retry logic, and offline simulation mode.
"""

import math
import random
import sys
import time
from datetime import datetime, timezone
import requests

# Reconfigure stdout for UTF-8 on Windows command prompts to prevent charmap errors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import sensor_simulator.config as cfg



class VirtualPlantNode:
    """Simulates physical plant soil physics and environmental dynamics."""

    def __init__(self, device_id: str = None, initial_moisture: float = None):
        self.device_id = device_id or cfg.DEVICE_ID
        self.soil_moisture = float(initial_moisture if initial_moisture is not None else cfg.INITIAL_SOIL_MOISTURE)
        self.water_tank_level = 88.0
        self.pump_active = False
        self.ticks = 0
        print(f"\n=================================================================")
        print(f"[VIRTUAL IOT NODE] Initialized Node: {self.device_id}")
        print(f"   Initial Moisture: {self.soil_moisture:.1f}%")
        print(f"   Target Ingest Endpoint: {cfg.INGEST_ENDPOINT}")
        print(f"   Reporting Interval: {cfg.SEND_INTERVAL_SECONDS}s")
        print(f"=================================================================\n")

    def update_physics(self) -> None:
        """Advance physical simulation one time tick."""
        self.ticks += 1

        if self.pump_active:
            # Water pump is actively irrigating soil
            boost = cfg.WATERING_BOOST_PER_TICK + random.uniform(-0.3, 0.5)
            self.soil_moisture = min(100.0, self.soil_moisture + boost)
            self.water_tank_level = max(0.0, self.water_tank_level - 0.4)

            # Auto shutoff virtual pump once target moisture reached
            if self.soil_moisture >= cfg.MOISTURE_TARGET_AFTER_WATER:
                self.pump_active = False
                print(f"[VIRTUAL ACTUATOR] Moisture reached target {self.soil_moisture:.1f}%. Virtual pump deactivated.")
        else:
            # Natural soil evaporation and plant transpiration
            loss = cfg.DRYING_RATE_PER_TICK + random.uniform(-0.1, 0.2)
            self.soil_moisture = max(5.0, self.soil_moisture - loss)

    def generate_telemetry(self) -> dict:
        """Construct realistic environmental telemetry packet."""
        # Simulated diurnal cycle (24 ticks = 1 day cycle for demo visibility)
        cycle_angle = (self.ticks % 48) / 48.0 * (2.0 * math.pi)

        # Diurnal temperature (peaks around solar noon)
        temp_curve = math.sin(cycle_angle - math.pi / 2.0)
        temperature = cfg.TEMP_BASE + (cfg.TEMP_VARIATION * temp_curve) + random.uniform(-0.4, 0.4)

        # Humidity inversely correlates with temperature
        humidity = cfg.HUMIDITY_BASE - (cfg.HUMIDITY_VARIATION * temp_curve) + random.uniform(-1.0, 1.0)
        humidity = max(20.0, min(95.0, humidity))

        # Ambient sunlight intensity (0% at night, up to 95% midday)
        sun_intensity = max(0.0, math.sin(cycle_angle))
        light_level = (sun_intensity * 85.0) + (10.0 if sun_intensity > 0 else 2.0) + random.uniform(-1.5, 1.5)
        light_level = max(0.0, min(100.0, light_level))

        return {
            "device_id": self.device_id,
            "soil_moisture": round(self.soil_moisture, 1),
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "light_level": round(light_level, 1),
            "water_tank_level": round(self.water_tank_level, 1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def transmit(self, payload: dict) -> None:
        """Transmits telemetry to cloud API with resilience, retry handling, and command processing."""
        if cfg.OFFLINE_MODE:
            print(f"[OFFLINE SIMULATION] Telemetry generated: {payload}")
            return

        headers = {
            "Content-Type": "application/json",
            "X-Device-API-Key": cfg.DEVICE_API_KEY
        }

        success = False
        for attempt in range(1, cfg.MAX_RETRIES + 1):
            try:
                response = requests.post(
                    cfg.INGEST_ENDPOINT,
                    json=payload,
                    headers=headers,
                    timeout=5.0
                )

                if response.status_code in (200, 201):
                    res_json = response.json()
                    pump_cmd = res_json.get("pump_command", "OFF")
                    triggered = res_json.get("watering_triggered", False)
                    status_text = "DRY (WATERING)" if self.soil_moisture < 30.0 else "HEALTHY"

                    # Print formatted console telemetry log
                    print(
                        f"[TX SUCCESS] Tick #{self.ticks:03d} | "
                        f"Moisture: {payload['soil_moisture']:5.1f}% | "
                        f"Temp: {payload['temperature']:4.1f}C | "
                        f"Humid: {payload['humidity']:4.1f}% | "
                        f"Status: {status_text:<14} | "
                        f"Cloud Pump Command: [{pump_cmd}]"
                    )

                    # Cloud command actuation feedback
                    if pump_cmd == "ON":
                        if not self.pump_active:
                            print(f"\n=======================================================")
                            print(f"[CLOUD COMMAND ACTUATION] >> PUMP COMMAND: ON <<")
                            print(f"   Reason: {res_json.get('decision_metadata', {}).get('reason', 'Moisture low')}")
                            print(f"   Virtual Relay energized! Submersible pump running.")
                            print(f"=======================================================\n")
                            self.pump_active = True
                    else:
                        if self.pump_active:
                            print(f"[CLOUD COMMAND ACTUATION] >> PUMP COMMAND: OFF <<")
                            self.pump_active = False

                    success = True
                    break
                else:
                    print(f"[HTTP ERROR] Server responded with code {response.status_code}: {response.text}")
                    break

            except requests.exceptions.ConnectionError:
                print(f"[NETWORK RETRY {attempt}/{cfg.MAX_RETRIES}] Cannot reach Cloud Backend at {cfg.INGEST_ENDPOINT}.")
                if attempt < cfg.MAX_RETRIES:
                    time.sleep(cfg.RETRY_DELAY_SECONDS)
            except Exception as e:
                print(f"[UNEXPECTED ERROR] {str(e)}")
                break

        if not success and not cfg.OFFLINE_MODE:
            print("[WARN] Telemetry packet dropped after maximum retries. Will retry on next tick.")


def run_simulator(duration_ticks: int = None, interval: float = None) -> None:
    """Main execution loop for the virtual IoT plant node."""
    interval_seconds = interval if interval is not None else cfg.SEND_INTERVAL_SECONDS
    node = VirtualPlantNode()
    ticks_done = 0

    try:
        while True:
            node.update_physics()
            packet = node.generate_telemetry()
            node.transmit(packet)

            ticks_done += 1
            if duration_ticks and ticks_done >= duration_ticks:
                print(f"\nSimulation finished after {ticks_done} ticks.")
                break

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\n[SIMULATOR STOPPED] Exiting Virtual IoT Plant Node simulation gracefully.")
        sys.exit(0)


if __name__ == "__main__":
    run_simulator()
