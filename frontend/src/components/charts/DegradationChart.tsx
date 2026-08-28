import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import type { DriverDegradation } from '../../types';
import { getCompoundColor, formatLapTime } from '../../utils/formatters';
import { CompoundBadge } from '../common/CompoundBadge';

interface DegradationChartProps {
  degradationData?: DriverDegradation;
}

export const DegradationChart: React.FC<DegradationChartProps> = ({ degradationData }) => {
  const [selectedStintIdx, setSelectedStintIdx] = useState<number>(0);

  if (!degradationData || !degradationData.stints || degradationData.stints.length === 0) {
    return (
      <div className="telemetry-card p-6 text-center text-slate-500 text-sm">
        No tyre degradation records available for this driver.
      </div>
    );
  }

  const stints = degradationData.stints;
  const currentStint = stints[selectedStintIdx] || stints[0];

  const validLaps = currentStint.valid_laps || [];
  const xAges = validLaps.map((l) => l.tyre_age);
  const yTimes = validLaps.map((l) => l.lap_time);

  const compoundColor = getCompoundColor(currentStint.compound);

  // Linear trendline data points
  let trendX: number[] = [];
  let trendY: number[] = [];
  if (xAges.length >= 2) {
    const minAge = Math.min(...xAges);
    const maxAge = Math.max(...xAges);
    const basePace = currentStint.best_lap_time;
    trendX = [minAge, maxAge];
    trendY = [
      basePace + minAge * currentStint.degradation_rate_per_lap,
      basePace + maxAge * currentStint.degradation_rate_per_lap,
    ];
  }

  const traces: any[] = [
    // Stint Lap Scatter
    {
      x: xAges,
      y: yTimes,
      mode: 'markers',
      name: `${currentStint.compound} Stint Pace`,
      marker: {
        color: compoundColor,
        size: 7,
        line: { color: '#111622', width: 1 },
      },
      text: validLaps.map(
        (l) =>
          `Lap ${l.lap_number}<br>Tyre Age: ${l.tyre_age} laps<br>Lap Time: ${formatLapTime(
            l.lap_time
          )}`
      ),
      hoverinfo: 'text',
    },
    // Linear degradation trendline
    {
      x: trendX,
      y: trendY,
      mode: 'lines',
      name: `Degradation Slope (+${(currentStint.degradation_rate_per_lap).toFixed(3)}s/lap)`,
      line: {
        color: '#E10600',
        width: 2.5,
        dash: 'dash',
      },
      hoverinfo: 'name',
    },
  ];

  return (
    <div className="telemetry-card p-5 mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#232B3E] pb-3 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-amber-400"></span>
              Estimated Tyre Degradation & Wear Model
            </h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30">
              Analytical Model
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Statistical tyre degradation rate derived from green-flag stint progression (excluding SC/VSC laps).
          </p>
        </div>

        {/* Stint Switcher Tabs */}
        <div className="flex items-center gap-1.5 bg-[#0E131F] p-1 rounded-lg border border-[#232B3E]">
          {stints.map((st, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedStintIdx(idx)}
              className={`px-3 py-1 text-xs font-bold uppercase rounded flex items-center gap-1.5 transition-colors ${
                selectedStintIdx === idx
                  ? 'bg-[#1D2536] text-white shadow-sm ring-1 ring-f1-red'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <CompoundBadge compound={st.compound} size="sm" />
              <span>Stint {st.stint_number}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Stint Statistics Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
        <div className="bg-[#0E131F] rounded-lg p-2.5 border border-[#232B3E]">
          <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
            Degradation Rate
          </div>
          <div className="text-base font-black text-amber-400 font-mono mt-0.5">
            +{currentStint.degradation_rate_per_lap.toFixed(3)}s / lap
          </div>
        </div>

        <div className="bg-[#0E131F] rounded-lg p-2.5 border border-[#232B3E]">
          <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
            Stint Pace Loss
          </div>
          <div className="text-base font-black text-red-400 font-mono mt-0.5">
            +{currentStint.pace_deterioration_total.toFixed(2)}s total
          </div>
        </div>

        <div className="bg-[#0E131F] rounded-lg p-2.5 border border-[#232B3E]">
          <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
            Avg Stint Pace
          </div>
          <div className="text-base font-black text-white font-mono mt-0.5">
            {formatLapTime(currentStint.avg_lap_time)}
          </div>
        </div>

        <div className="bg-[#0E131F] rounded-lg p-2.5 border border-[#232B3E]">
          <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
            Model Fit (R² Confidence)
          </div>
          <div className="text-base font-black text-cyan-400 font-mono mt-0.5">
            {(currentStint.confidence * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Plotly Scatter with Trend */}
      <div className="w-full h-[340px]">
        <Plot
          data={traces}
          layout={{
            autosize: true,
            margin: { l: 50, r: 25, t: 15, b: 40 },
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
              title: { text: 'Tyre Age (Laps on this Set)', font: { color: '#94A3B8', size: 11 } },
              gridcolor: '#1E2638',
              zerolinecolor: '#1E2638',
              tickfont: { color: '#94A3B8', size: 10 },
            },
            yaxis: {
              title: { text: 'Lap Time (Seconds)', font: { color: '#94A3B8', size: 11 } },
              gridcolor: '#1E2638',
              zerolinecolor: '#1E2638',
              tickfont: { color: '#94A3B8', size: 10 },
            },
            hoverlabel: {
              bgcolor: '#111622',
              bordercolor: '#2E384D',
              font: { color: '#FFFFFF', family: 'JetBrains Mono', size: 11 },
            },
          }}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
          config={{ responsive: true, displayModeBar: false }}
        />
      </div>

      <div className="mt-2 text-[10px] text-slate-500 italic">
        * Estimated Tyre Degradation is influenced by track evolution, traffic, and fuel burn. Not an exact physical tyre simulation.
      </div>
    </div>
  );
};
