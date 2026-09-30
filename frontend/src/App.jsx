import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import StatusCard from './components/StatusCard';
import { MoistureChart, ClimateChart } from './components/MetricChart';
import ControlPanel from './components/ControlPanel';
import AlertBanner from './components/AlertBanner';
import WateringHistoryTable from './components/WateringHistoryTable';
import AnalyticsOverview from './components/AnalyticsOverview';
import { api } from './services/api';
import './App.css';

export default function App() {
  const [devices, setDevices] = useState([]);
  const [activeDeviceId, setActiveDeviceId] = useState('PLANT-001');
  const [device, setDevice] = useState(null);
  const [latestReading, setLatestReading] = useState(null);
  const [history, setHistory] = useState([]);
  const [wateringEvents, setWateringEvents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [plantProfiles, setPlantProfiles] = useState([]);
  const [isWateringLoading, setIsWateringLoading] = useState(false);

  // Initial load
  useEffect(() => {
    async function init() {
      try {
        const [devList, profiles] = await Promise.all([
          api.getDevices(),
          api.getPlantProfiles()
        ]);
        setDevices(devList);
        setPlantProfiles(profiles);
        if (devList.length > 0 && !devList.some((d) => d.device_id === activeDeviceId)) {
          setActiveDeviceId(devList[0].device_id);
        }
      } catch (err) {
        console.error('Initialization error:', err);
      }
    }
    init();
  }, []);

  // Polling data refresh
  const loadDeviceData = useCallback(async () => {
    if (!activeDeviceId) return;
    try {
      const [dev, reading, hist, waterHist, alrts, anlyt] = await Promise.all([
        api.getDevice(activeDeviceId),
        api.getLatestReading(activeDeviceId),
        api.getHistory(activeDeviceId, 30),
        api.getWateringHistory(activeDeviceId, 15),
        api.getAlerts(activeDeviceId),
        api.getAnalytics(activeDeviceId)
      ]);
      setDevice(dev);
      setLatestReading(reading);
      setHistory(hist);
      setWateringEvents(waterHist);
      setAlerts(alrts);
      setAnalytics(anlyt);
    } catch (err) {
      console.error('Data polling error:', err);
    }
  }, [activeDeviceId]);

  useEffect(() => {
    loadDeviceData();
    const interval = setInterval(loadDeviceData, 2500);
    return () => clearInterval(interval);
  }, [loadDeviceData]);

  // Actions
  const handleManualWater = async () => {
    setIsWateringLoading(true);
    try {
      await api.triggerWatering(activeDeviceId, 5);
      await loadDeviceData();
    } catch (err) {
      alert(`Watering command failed: ${err.message}`);
    } finally {
      setIsWateringLoading(false);
    }
  };

  const handleToggleAutoWater = async (enabled) => {
    try {
      await api.updateDevice(activeDeviceId, { auto_water_enabled: enabled });
      loadDeviceData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdateThreshold = async (newThreshold) => {
    try {
      await api.updateThreshold(activeDeviceId, newThreshold);
      loadDeviceData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectProfile = async (profileKey) => {
    const profile = plantProfiles.find((p) => p.key === profileKey);
    if (!profile) return;
    try {
      await api.updateDevice(activeDeviceId, {
        plant_type: profileKey,
        moisture_threshold: profile.threshold
      });
      loadDeviceData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleAcknowledgeAlert = async (alertId) => {
    try {
      await api.acknowledgeAlert(alertId);
      loadDeviceData();
    } catch (err) {
      console.error(err);
    }
  };

  const currentProfile = plantProfiles.find((p) => p.key === device?.plant_type) || {};
  const isPumpOn = device?.pump_status === 'ON';
  const isOnline = device?.is_online ?? false;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        devices={devices}
        activeDeviceId={activeDeviceId}
        onSelectDevice={setActiveDeviceId}
        isOnline={isOnline}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 flex-1 w-full">
        {/* Alerts Banner */}
        <AlertBanner alerts={alerts} onAcknowledge={handleAcknowledgeAlert} />

        {/* Hero Plant Header */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xl">
          <div className="flex items-center space-x-5">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/10 border border-emerald-500/30 flex items-center justify-center text-3xl shadow-inner">
              {currentProfile.icon || '🌱'}
            </div>
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-2xl font-bold text-white">
                  {device?.plant_name || 'Loading plant...'}
                </h2>
                <span
                  className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${
                    device?.plant_health_status === 'Healthy'
                      ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                      : device?.plant_health_status === 'Needs Water'
                      ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 animate-pulse'
                      : device?.plant_health_status === 'Watering Active'
                      ? 'bg-blue-500/20 text-blue-300 border-blue-500/40 animate-pulse'
                      : 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                  }`}
                >
                  {device?.plant_health_status || 'Checking status'}
                </span>
              </div>
              <p className="text-sm text-slate-400 mt-1">
                Species: <span className="text-slate-200 font-medium">{device?.plant_type}</span>{' '}
                &bull; Location:{' '}
                <span className="text-slate-200 font-medium">{device?.location}</span> &bull; Node:{' '}
                <span className="text-slate-200 font-mono font-semibold">{device?.device_id}</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleManualWater}
              disabled={isWateringLoading || isPumpOn}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-blue-500/20 active:scale-95 transition disabled:opacity-50 cursor-pointer"
            >
              <span>💧</span>
              <span>{isPumpOn ? 'Watering In Progress...' : 'Water Plant Now'}</span>
            </button>
            <button
              onClick={loadDeviceData}
              className="px-3.5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-sm font-semibold transition cursor-pointer"
              title="Refresh"
            >
              ↻
            </button>
          </div>
        </div>

        {/* 6 Metric KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
          <StatusCard
            title="SOIL MOISTURE"
            value={latestReading?.soil_moisture?.toFixed(1)}
            unit="%"
            icon="🌿"
            subtext={`Target threshold: ${device?.moisture_threshold || 30}%`}
            barPercent={latestReading?.soil_moisture}
            barColor={
              latestReading?.soil_moisture < (device?.moisture_threshold || 30)
                ? 'bg-rose-500'
                : 'bg-emerald-500'
            }
            isAlert={latestReading?.soil_moisture < (device?.moisture_threshold || 30)}
          />

          <StatusCard
            title="TEMPERATURE"
            value={latestReading?.temperature?.toFixed(1)}
            unit="°C"
            icon="🌡️"
            subtext="Ideal: 18°C - 32°C"
            statusLabel={latestReading?.temperature > 34 ? 'High Heat' : 'Optimal'}
            isAlert={latestReading?.temperature > 34}
          />

          <StatusCard
            title="AIR HUMIDITY"
            value={latestReading?.humidity?.toFixed(1)}
            unit="%"
            icon="💨"
            subtext="Relative ambient humidity"
            barPercent={latestReading?.humidity}
            barColor="bg-blue-500"
          />

          <StatusCard
            title="LIGHT LEVEL"
            value={latestReading?.light_level?.toFixed(1)}
            unit="%"
            icon="☀️"
            subtext="Photosynthesis index"
            statusLabel="Sunlight"
          />

          <StatusCard
            title="PUMP STATUS"
            value={device?.pump_status || 'OFF'}
            icon="⚡"
            subtext={
              device?.last_watered_at
                ? `Last: ${new Date(device.last_watered_at).toLocaleTimeString()}`
                : 'Last: --'
            }
            statusLabel={isPumpOn ? 'Submersible pump running' : 'Relay standby'}
            pulseGlow={isPumpOn}
          />

          <StatusCard
            title="WATER TANK"
            value={latestReading?.water_tank_level?.toFixed(0) || 85}
            unit="%"
            icon="🪣"
            subtext="Reservoir capacity"
            barPercent={latestReading?.water_tank_level || 85}
            barColor="bg-cyan-500"
          />
        </div>

        {/* Real-time Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <span>📈</span> Soil Moisture Telemetry Trend
                </h3>
                <p className="text-xs text-slate-400">
                  Real-time capacitive sensor telemetry vs. automated irrigation trigger line
                </p>
              </div>
              <div className="flex items-center space-x-2 text-xs">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span> Moisture %
                </span>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-rose-500/10 text-rose-400 border border-rose-500/20">
                  <span className="w-2 h-0.5 bg-rose-400"></span> Threshold
                </span>
              </div>
            </div>
            <MoistureChart readings={history} threshold={device?.moisture_threshold || 30} />
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <div className="mb-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <span>🌤️</span> Ambient Microclimate
              </h3>
              <p className="text-xs text-slate-400">Temperature (°C) & Humidity (%) history</p>
            </div>
            <ClimateChart readings={history} />
          </div>
        </div>

        {/* Lower Row: Controls & Audit Log */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {device && (
            <ControlPanel
              device={device}
              plantProfiles={plantProfiles}
              onToggleAutoWater={handleToggleAutoWater}
              onUpdateThreshold={handleUpdateThreshold}
              onSelectProfile={handleSelectProfile}
            />
          )}

          <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
                <div>
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <span>📋</span> Watering Audit Log
                  </h3>
                  <p className="text-xs text-slate-400">
                    Immutable cloud audit records of automated & manual watering cycles
                  </p>
                </div>
                <span className="text-xs font-medium text-slate-400">
                  Total: {wateringEvents.length} events
                </span>
              </div>
              <WateringHistoryTable events={wateringEvents} />
            </div>

            <AnalyticsOverview analytics={analytics} />
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800/80 bg-slate-900/60 py-6 text-xs text-slate-500 text-center space-y-1">
        <p className="font-medium text-slate-400">
          Cloud-Connected Smart Plant Care & Watering Platform &bull; Academic & Industrial Proof of Work
        </p>
        <p>
          FastAPI &bull; React &bull; Virtual IoT Telemetry &bull; SQLAlchemy ORM &bull; Automated Decision Engine
        </p>
      </footer>
    </div>
  );
}
