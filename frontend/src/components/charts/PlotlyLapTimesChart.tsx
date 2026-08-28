import React from 'react';
import Plot from 'react-plotly.js';
import type { Lap, RaceEvent, Driver } from '../../types';
import { formatLapTime } from '../../utils/formatters';

interface PlotlyLapTimesChartProps {
  primaryDriverLaps: Lap[];
  compareDriverLaps?: Lap[];
  primaryDriver?: Driver;
  compareDriver?: Driver;
  events?: RaceEvent[];
}

export const PlotlyLapTimesChart: React.FC<PlotlyLapTimesChartProps> = ({
  primaryDriverLaps,
  compareDriverLaps = [],
  primaryDriver,
  compareDriver,
  events = [],
}) => {
  if (!primaryDriverLaps || primaryDriverLaps.length === 0) {
    return (
      <div className="telemetry-card p-6 text-center text-slate-500 text-sm">
        No lap timing data available for selected driver.
      </div>
    );
  }

  // Build SC/VSC shapes
  const scShapes: any[] = events
    .filter((e) => e.event_type === 'SAFETY_CAR' || e.event_type === 'VSC')
    .map((e) => ({
      type: 'rect',
      xref: 'x',
      yref: 'paper',
      x0: e.start_lap || e.lap,
      x1: (e.end_lap || e.lap) + 0.9,
      y0: 0,
      y1: 1,
      fillcolor: e.event_type === 'SAFETY_CAR' ? 'rgba(234, 179, 8, 0.15)' : 'rgba(245, 158, 11, 0.12)',
      line: { width: 1, color: e.event_type === 'SAFETY_CAR' ? '#eab308' : '#f59e0b' },
    }));

  const traces: any[] = [];

  // Primary Driver trace
  const d1X = primaryDriverLaps.map((l) => l.lap_number);
  const d1Y = primaryDriverLaps.map((l) => l.lap_time);
  const d1Hover = primaryDriverLaps.map(
    (l) =>
      `<b>${primaryDriver?.driver_code || 'Driver 1'}</b><br>Lap: ${l.lap_number}<br>Pace: ${formatLapTime(
        l.lap_time
      )}<br>Position: P${l.position || '—'}${l.pit_stop ? '<br><b>[PIT STOP]</b>' : ''}`
  );

  traces.push({
    x: d1X,
    y: d1Y,
    text: d1Hover,
    hoverinfo: 'text',
    mode: 'lines+markers',
    name: `${primaryDriver?.driver_code || 'Primary'} (${primaryDriver?.team || 'Driver'})`,
    line: { color: primaryDriver?.team_color || '#E10600', width: 2.5 },
    marker: {
      size: primaryDriverLaps.map((l) => (l.pit_stop ? 9 : 4)),
      symbol: primaryDriverLaps.map((l) => (l.pit_stop ? 'diamond' : 'circle')),
      color: primaryDriverLaps.map((l) => (l.pit_stop ? '#FFD800' : primaryDriver?.team_color || '#E10600')),
    },
  });

  // Compare Driver trace
  if (compareDriverLaps && compareDriverLaps.length > 0) {
    const d2X = compareDriverLaps.map((l) => l.lap_number);
    const d2Y = compareDriverLaps.map((l) => l.lap_time);
    const d2Hover = compareDriverLaps.map(
      (l) =>
        `<b>${compareDriver?.driver_code || 'Compare'}</b><br>Lap: ${l.lap_number}<br>Pace: ${formatLapTime(
          l.lap_time
        )}<br>Position: P${l.position || '—'}${l.pit_stop ? '<br><b>[PIT STOP]</b>' : ''}`
    );

    traces.push({
      x: d2X,
      y: d2Y,
      text: d2Hover,
      hoverinfo: 'text',
      mode: 'lines+markers',
      name: `${compareDriver?.driver_code || 'Compare'} (${compareDriver?.team || 'Driver'})`,
      line: { color: compareDriver?.team_color || '#00D2BE', width: 2.5, dash: 'dot' },
      marker: {
        size: compareDriverLaps.map((l) => (l.pit_stop ? 9 : 4)),
        symbol: compareDriverLaps.map((l) => (l.pit_stop ? 'diamond' : 'circle')),
        color: compareDriverLaps.map((l) => (l.pit_stop ? '#FFD800' : compareDriver?.team_color || '#00D2BE')),
      },
    });
  }

  // Calculate suitable Y range avoiding extreme pit-in outlier truncation
  const allValidY = [...d1Y, ...(compareDriverLaps.map((l) => l.lap_time) || [])].filter(
    (t): t is number => typeof t === 'number' && t > 40 && t < 180
  );
  const minY = allValidY.length ? Math.min(...allValidY) - 1.5 : 70;
  const maxY = allValidY.length ? Math.max(...allValidY) + 3.0 : 130;

  return (
    <div className="telemetry-card p-5 mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
        <div>
          <h2 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
            Race Pace & Lap Time Progression
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Lap-by-lap flying pace, pit stop spikes, and Safety Car / VSC intervals.
          </p>
        </div>
      </div>

      <div className="w-full h-[400px]">
        <Plot
          data={traces}
          layout={{
            autosize: true,
            margin: { l: 50, r: 25, t: 20, b: 45 },
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            showlegend: true,
            legend: {
              orientation: 'h',
              y: 1.1,
              x: 0,
              font: { color: '#E2E8F0', size: 11, family: 'Inter' },
            },
            xaxis: {
              title: { text: 'Lap Number', font: { color: '#94A3B8', size: 11 } },
              gridcolor: '#1E2638',
              zerolinecolor: '#1E2638',
              tickfont: { color: '#94A3B8', size: 10 },
            },
            yaxis: {
              title: { text: 'Lap Time (Seconds)', font: { color: '#94A3B8', size: 11 } },
              range: [minY, maxY],
              gridcolor: '#1E2638',
              zerolinecolor: '#1E2638',
              tickfont: { color: '#94A3B8', size: 10 },
            },
            shapes: scShapes,
            hoverlabel: {
              bgcolor: '#111622',
              bordercolor: '#2E384D',
              font: { color: '#FFFFFF', family: 'JetBrains Mono', size: 11 },
            },
          }}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
          config={{ responsive: true, displayModeBar: true, displaylogo: false }}
        />
      </div>
    </div>
  );
};
