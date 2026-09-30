import React from 'react';

export default function AlertBanner({ alerts = [], onAcknowledge }) {
  const activeAlerts = alerts.filter((a) => a.status === 'ACTIVE');

  if (activeAlerts.length === 0) return null;

  return (
    <div className="space-y-2">
      {activeAlerts.map((alert) => {
        const isCritical = alert.severity === 'CRITICAL';
        return (
          <div
            key={alert.alert_id}
            className={`border rounded-xl p-3 flex items-center justify-between shadow-lg transition-all ${
              isCritical
                ? 'bg-rose-950/80 border-rose-800/80 text-rose-200'
                : 'bg-amber-950/80 border-amber-800/80 text-amber-200'
            }`}
          >
            <div className="flex items-center space-x-3">
              <span className="text-xl">{isCritical ? '🚨' : '⚠️'}</span>
              <div>
                <p className="text-xs font-bold uppercase tracking-wider">
                  {alert.alert_type} &bull; {alert.severity}
                </p>
                <p className="text-xs mt-0.5">{alert.message}</p>
              </div>
            </div>
            <button
              onClick={() => onAcknowledge(alert.alert_id)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                isCritical
                  ? 'bg-rose-800 hover:bg-rose-700 text-rose-100'
                  : 'bg-amber-800 hover:bg-amber-700 text-amber-100'
              }`}
            >
              Acknowledge
            </button>
          </div>
        );
      })}
    </div>
  );
}
