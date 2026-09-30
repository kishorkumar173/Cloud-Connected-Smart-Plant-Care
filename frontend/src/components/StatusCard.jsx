import React from 'react';

export default function StatusCard({
  title,
  value,
  unit = '',
  icon,
  subtext,
  barPercent = null,
  barColor = 'bg-emerald-500',
  isAlert = false,
  statusLabel = null,
  pulseGlow = false
}) {
  return (
    <div
      className={`bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between transition-all duration-300 ${
        pulseGlow ? 'pump-active-pulse border-blue-500/50' : ''
      }`}
    >
      <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
        <span>{title}</span>
        <span className="text-lg">{icon}</span>
      </div>

      <div className="mt-4">
        <div className="flex items-baseline space-x-1">
          <span className={`text-3xl font-extrabold ${isAlert ? 'text-rose-400' : 'text-white'}`}>
            {value !== undefined && value !== null ? value : '--'}
          </span>
          {unit && <span className="text-sm text-slate-400">{unit}</span>}
        </div>

        {statusLabel && (
          <p className="text-xs font-semibold text-slate-300 mt-2">{statusLabel}</p>
        )}

        {barPercent !== null && (
          <div className="w-full bg-slate-800 rounded-full h-2 mt-3 overflow-hidden">
            <div
              className={`${barColor} h-2 rounded-full transition-all duration-500`}
              style={{ width: `${Math.min(100, Math.max(0, barPercent))}%` }}
            ></div>
          </div>
        )}
      </div>

      <p className="text-[11px] text-slate-500 mt-3">{subtext}</p>
    </div>
  );
}
