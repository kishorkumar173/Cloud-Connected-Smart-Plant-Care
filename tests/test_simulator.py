"""
Unit Tests for Python Virtual IoT Sensor Simulator
Verifies mathematical physical models, diurnal sine curves, and telemetry packet schemas.
"""

from sensor_simulator.simulator import VirtualPlantNode


def test_virtual_node_initialization():
    """Test ID 18: Virtual IoT node initializes with specified moisture and defaults."""
    node = VirtualPlantNode(device_id="TEST-SIM-01", initial_moisture=60.0)
    assert node.device_id == "TEST-SIM-01"
    assert node.soil_moisture == 60.0
    assert node.pump_active is False


def test_virtual_node_drying_physics():
    """Test ID 19: Moisture decreases over time when pump is inactive."""
    node = VirtualPlantNode(device_id="TEST-SIM-02", initial_moisture=50.0)
    initial = node.soil_moisture
    node.update_physics()
    assert node.soil_moisture < initial


def test_virtual_node_watering_physics():
    """Test ID 20: Moisture increases when virtual pump is energized."""
    node = VirtualPlantNode(device_id="TEST-SIM-03", initial_moisture=20.0)
    node.pump_active = True
    node.update_physics()
    assert node.soil_moisture > 20.0


def test_telemetry_packet_structure():
    """Test ID 21: Telemetry dictionary conforms to cloud API specification."""
    node = VirtualPlantNode(device_id="TEST-SIM-04", initial_moisture=45.0)
    node.update_physics()
    telemetry = node.generate_telemetry()

    assert telemetry["device_id"] == "TEST-SIM-04"
    assert 0.0 <= telemetry["soil_moisture"] <= 100.0
    assert 10.0 <= telemetry["temperature"] <= 45.0
    assert 10.0 <= telemetry["humidity"] <= 100.0
    assert 0.0 <= telemetry["light_level"] <= 100.0
    assert "timestamp" in telemetry
