import React from 'react';

export default function WateringHistoryTable({ events = [] }) {
  return (
    <div className="overflow-x-auto max-h-64 overflow-y-auto">
      <table className="w-full text-left text-xs">
        <thead className="text-slate-400 border-b border-slate-800 font-semibold uppercase tracking-wider sticky top-0 bg-slate-900">
          <tr>
            <th className="py-2.5 px-3">Timestamp</th>
            <th className="py-2.5 px-3">Trigger</th>
            <th className="py-2.5 px-3">Moisture Before</th>
            <th className="py-2.5 px-3">Moisture After</th>
            <th className="py-2.5 px-3">Duration</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60 text-slate-300">
          {events.length === 0 ? (
            <tr>
              <td colSpan={5} className="py-4 text-center text-slate-500">
                No watering cycles recorded yet.
              </td>
            </tr>
          ) : (
            events.map((ev) => {
              const timeStr = new Date(ev.timestamp).toLocaleString();
              const isAuto = ev.trigger_type === 'AUTOMATIC';
              return (
                <tr key={ev.event_id} className="hover:bg-slate-800/40 transition">
                  <td className="py-2.5 px-3 text-slate-400 font-mono">{timeStr}</td>
                  <td className="py-2.5 px-3">
                    <span
                      className={`px-2 py-0.5 rounded font-semibold border ${
                        isAuto
                          ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                          : 'bg-blue-500/20 text-blue-300 border-blue-500/30'
                      }`}
                    >
                      {ev.trigger_type}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-semibold text-rose-300">
                    {ev.moisture_before.toFixed(1)}%
                  </td>
                  <td className="py-2.5 px-3 font-semibold text-emerald-300">
                    {ev.moisture_after ? `${ev.moisture_after.toFixed(1)}%` : '--'}
                  </td>
                  <td className="py-2.5 px-3 text-slate-300">{ev.duration_seconds}s</td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}
