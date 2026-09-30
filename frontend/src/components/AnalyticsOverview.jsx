import React from 'react';

export default function AnalyticsOverview({ analytics }) {
  if (!analytics) return null;

  return (
    <div className="grid grid-cols-3 gap-3 pt-4 border-t border-slate-800 mt-4 text-center">
      <div className="bg-slate-800/40 rounded-xl p-2.5">
        <p className="text-[11px] text-slate-400 font-medium">Watering Cycles Today</p>
        <p className="text-lg font-bold text-white mt-0.5">{analytics.watering_count_today}</p>
      </div>
      <div className="bg-slate-800/40 rounded-xl p-2.5">
        <p className="text-[11px] text-slate-400 font-medium">Est. Water Dispersed</p>
        <p className="text-lg font-bold text-cyan-400 mt-0.5">
          {analytics.estimated_water_used_liters.toFixed(2)} L
        </p>
      </div>
      <div className="bg-slate-800/40 rounded-xl p-2.5">
        <p className="text-[11px] text-slate-400 font-medium">Cloud Uptime SLA</p>
        <p className="text-lg font-bold text-emerald-400 mt-0.5">
          {analytics.uptime_percentage.toFixed(1)}%
        </p>
      </div>
    </div>
  );
}
