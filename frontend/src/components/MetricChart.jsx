import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export function MoistureChart({ readings = [], threshold = 30 }) {
  const labels = readings.map((r) => {
    const d = new Date(r.timestamp);
    return `${d.getHours().toString().padStart(2, '0')}:${d
      .getMinutes()
      .toString()
      .padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
  });

  const moistureData = readings.map((r) => r.soil_moisture);
  const thresholdData = readings.map(() => threshold);

  const data = {
    labels,
    datasets: [
      {
        label: 'Soil Moisture (%)',
        data: moistureData,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
        pointRadius: 2
      },
      {
        label: 'Trigger Threshold (%)',
        data: thresholdData,
        borderColor: '#f43f5e',
        borderWidth: 1.5,
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    scales: {
      y: {
        min: 0,
        max: 100,
        grid: { color: 'rgba(51, 65, 85, 0.4)' },
        ticks: { color: '#94a3b8', font: { size: 10 } }
      },
      x: {
        grid: { display: false },
        ticks: { color: '#64748b', font: { size: 9 }, maxTicksLimit: 8 }
      }
    },
    plugins: {
      legend: { display: false }
    }
  };

  return (
    <div className="h-64 w-full">
      <Line data={data} options={options} />
    </div>
  );
}

export function ClimateChart({ readings = [] }) {
  const labels = readings.map((r) => {
    const d = new Date(r.timestamp);
    return `${d.getHours().toString().padStart(2, '0')}:${d
      .getMinutes()
      .toString()
      .padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
  });

  const tempData = readings.map((r) => r.temperature);
  const humidData = readings.map((r) => r.humidity);

  const data = {
    labels,
    datasets: [
      {
        label: 'Temp (°C)',
        data: tempData,
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        borderWidth: 2,
        tension: 0.35,
        pointRadius: 1,
        yAxisID: 'yTemp'
      },
      {
        label: 'Humidity (%)',
        data: humidData,
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.1)',
        borderWidth: 2,
        tension: 0.35,
        pointRadius: 1,
        yAxisID: 'yHumid'
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    scales: {
      yTemp: {
        position: 'left',
        min: 10,
        max: 45,
        grid: { color: 'rgba(51, 65, 85, 0.3)' },
        ticks: { color: '#f59e0b', font: { size: 10 } }
      },
      yHumid: {
        position: 'right',
        min: 20,
        max: 100,
        grid: { display: false },
        ticks: { color: '#38bdf8', font: { size: 10 } }
      },
      x: {
        grid: { display: false },
        ticks: { color: '#64748b', font: { size: 9 }, maxTicksLimit: 6 }
      }
    },
    plugins: {
      legend: {
        labels: { color: '#94a3b8', boxWidth: 10, font: { size: 10 } }
      }
    }
  };

  return (
    <div className="h-64 w-full">
      <Line data={data} options={options} />
    </div>
  );
}
