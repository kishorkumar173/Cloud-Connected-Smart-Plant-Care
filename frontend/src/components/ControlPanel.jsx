import React from 'react';

export default function ControlPanel({
  device,
  plantProfiles,
  onToggleAutoWater,
  onUpdateThreshold,
  onSelectProfile
}) {
  const currentProfile = plantProfiles.find((p) => p.key === device.plant_type) || {};

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span>⚙️</span> Irrigation Control Engine
        </h3>
        <p className="text-xs text-slate-400">Configure cloud automation thresholds and pump triggers</p>
      </div>

      {/* Auto Water Toggle Switch */}
      <div className="flex items-center justify-between p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
        <div>
          <p className="text-sm font-semibold text-white">Automated Irrigation Engine</p>
          <p className="text-xs text-slate-400">Cloud algorithm waters when soil drops below threshold</p>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={device.auto_water_enabled}
            onChange={(e) => onToggleAutoWater(e.target.checked)}
            className="sr-only peer"
          />
          <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
        </label>
      </div>

      {/* Moisture Threshold Slider */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-300">Moisture Trigger Threshold</label>
          <span className="text-sm font-bold text-emerald-400 font-mono">
            {device.moisture_threshold}%
          </span>
        </div>
        <input
          type="range"
          min="10"
          max="60"
          value={device.moisture_threshold}
          onChange={(e) => onUpdateThreshold(parseFloat(e.target.value))}
          className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
        />
        <div className="flex justify-between text-[11px] text-slate-500">
          <span>10% (Dry / Desert)</span>
          <span>35% (Optimal)</span>
          <span>60% (Wet / Bog)</span>
        </div>
      </div>

      {/* Botanical Preset Selector */}
      <div className="space-y-2">
        <label className="text-xs font-semibold text-slate-300">Botanical Species Preset</label>
        <select
          value={device.plant_type}
          onChange={(e) => onSelectProfile(e.target.value)}
          className="w-full bg-slate-800 border border-slate-700 text-sm font-medium text-slate-200 rounded-xl px-3.5 py-2.5 focus:outline-none focus:border-emerald-500"
        >
          {plantProfiles.map((p) => (
            <option key={p.key} value={p.key}>
              {p.icon} {p.name} (Threshold: {p.threshold}%)
            </option>
          ))}
        </select>
        {currentProfile.rationale && (
          <p className="text-[11px] text-slate-400 italic mt-1.5 leading-relaxed">
            {currentProfile.rationale}
          </p>
        )}
      </div>
    </div>
  );
}
