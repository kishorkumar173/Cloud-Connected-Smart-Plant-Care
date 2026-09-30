import React from 'react';

export default function Navbar({ devices, activeDeviceId, onSelectDevice, isOnline }) {
  return (
    <nav className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 text-2xl">
            🌱
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
              Smart Plant Cloud
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                IoT Telemetry
              </span>
            </h1>
            <p className="text-xs text-slate-400">Cloud-Connected Precision Irrigation & Plant Care</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400 font-medium">Node:</span>
            <select
              value={activeDeviceId}
              onChange={(e) => onSelectDevice(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-emerald-500"
            >
              {devices.map((d) => (
                <option key={d.device_id} value={d.device_id}>
                  {d.device_id} ({d.plant_name})
                </option>
              ))}
            </select>
          </div>

          <div
            className={`flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold ${
              isOnline
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                isOnline ? 'bg-emerald-400 animate-ping' : 'bg-rose-400'
              }`}
            ></span>
            <span>{isOnline ? 'Cloud Online' : 'Node Offline'}</span>
          </div>

          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          >
            API Docs ↗
          </a>
        </div>
      </div>
    </nav>
  );
}
