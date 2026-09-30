import React from 'react';

export default function WateringHistoryTable({ events = [] }) {
  return (
    <div className="overflow-x-auto max-h-64 overflow-y-auto rounded-lg">
      <table className="audit-table">
        <thead className="sticky top-0 bg-slate-900 shadow-sm">
          <tr>
            <th style={{ width: '30%' }}>Timestamp</th>
            <th style={{ width: '18%' }}>Trigger</th>
            <th style={{ width: '18%' }}>Moisture Before</th>
            <th style={{ width: '18%' }}>Moisture After</th>
            <th style={{ width: '16%' }}>Duration</th>
          </tr>
        </thead>
        <tbody>
          {events.length === 0 ? (
            <tr>
              <td colSpan={5} className="py-6 text-center text-slate-500 italic">
                No watering cycles recorded yet.
              </td>
            </tr>
          ) : (
            events.map((ev) => {
              const timeStr = new Date(ev.timestamp).toLocaleString();
              const isAuto = ev.trigger_type === 'AUTOMATIC';
              return (
                <tr key={ev.event_id}>
                  <td className="text-slate-400 font-mono text-[11px]">{timeStr}</td>
                  <td>
                    <span
                      className={`inline-block px-2 py-0.5 rounded text-[11px] font-semibold border ${
                        isAuto
                          ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                          : 'bg-blue-500/20 text-blue-300 border-blue-500/30'
                      }`}
                    >
                      {ev.trigger_type}
                    </span>
                  </td>
                  <td className="font-semibold text-rose-300">
                    {ev.moisture_before.toFixed(1)}%
                  </td>
                  <td className="font-semibold text-emerald-300">
                    {ev.moisture_after ? `${ev.moisture_after.toFixed(1)}%` : '--'}
                  </td>
                  <td className="text-slate-300 font-medium">{ev.duration_seconds}s</td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}
