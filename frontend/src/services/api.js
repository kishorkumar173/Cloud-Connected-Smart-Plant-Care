/**
 * API Service Client for Cloud-Connected Smart Plant Care Backend
 */

const API_BASE = window.location.port === "5173" ? "http://localhost:8000" : "";

export const api = {
  async getDevices() {
    const res = await fetch(`${API_BASE}/api/devices`);
    if (!res.ok) throw new Error("Failed to fetch devices");
    return res.json();
  },

  async getDevice(deviceId) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}`);
    if (!res.ok) throw new Error("Failed to fetch device details");
    return res.json();
  },

  async getLatestReading(deviceId) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}/latest`);
    if (!res.ok) return null;
    return res.json();
  },

  async getHistory(deviceId, limit = 30) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}/history?limit=${limit}`);
    if (!res.ok) throw new Error("Failed to fetch reading history");
    return res.json();
  },

  async updateThreshold(deviceId, threshold) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}/threshold`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ moisture_threshold: parseFloat(threshold) })
    });
    if (!res.ok) throw new Error("Failed to update threshold");
    return res.json();
  },

  async triggerWatering(deviceId, durationSeconds = 5) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}/water`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ duration_seconds: durationSeconds })
    });
    if (!res.ok) throw new Error("Failed to trigger watering");
    return res.json();
  },

  async updateDevice(deviceId, updateData) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updateData)
    });
    if (!res.ok) throw new Error("Failed to update device settings");
    return res.json();
  },

  async getWateringHistory(deviceId, limit = 15) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}/watering-history?limit=${limit}`);
    if (!res.ok) throw new Error("Failed to fetch watering history");
    return res.json();
  },

  async getAlerts(deviceId = null) {
    const url = deviceId ? `${API_BASE}/api/alerts?device_id=${deviceId}` : `${API_BASE}/api/alerts`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch alerts");
    return res.json();
  },

  async acknowledgeAlert(alertId) {
    const res = await fetch(`${API_BASE}/api/alerts/${alertId}/acknowledge`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: "ACKNOWLEDGED" })
    });
    if (!res.ok) throw new Error("Failed to acknowledge alert");
    return res.json();
  },

  async getAnalytics(deviceId) {
    const res = await fetch(`${API_BASE}/api/devices/${deviceId}/analytics`);
    if (!res.ok) throw new Error("Failed to fetch analytics");
    return res.json();
  },

  async getPlantProfiles() {
    const res = await fetch(`${API_BASE}/api/plant-profiles`);
    if (!res.ok) throw new Error("Failed to fetch plant profiles");
    return res.json();
  }
};
