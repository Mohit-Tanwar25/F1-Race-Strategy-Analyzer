import React from 'react';
import Plot from 'react-plotly.js';
import type { LapDeltaPoint, DriverScore } from '../../types';
import { formatDelta } from '../../utils/formatters';

interface DeltaComparisonChartProps {
  driver1: DriverScore;
  driver2: DriverScore;
  lapDeltas: LapDeltaPoint[];
}

export const DeltaComparisonChart: React.FC<DeltaComparisonChartProps> = ({
  driver1,
  driver2,
  lapDeltas,
}) => {
  if (!lapDeltas || lapDeltas.length === 0) {
    return (
      <div className="telemetry-card p-6 text-center text-slate-500 text-sm">
        No lap delta telemetry available between these two drivers.
      </div>
    );
  }

  const validPoints = lapDeltas.filter((d) => d.cumulative_gap !== null && d.cumulative_gap !== undefined);
  const xLaps = validPoints.map((d) => d.lap);
  const yGap = validPoints.map((d) => d.cumulative_gap);

  const traces: any[] = [
    {
      x: xLaps,
      y: yGap,
      mode: 'lines',
      name: `Cumulative Gap (${driver1.driver_code} vs ${driver2.driver_code})`,
      line: {
        color: '#00D2BE',
        width: 3,
      },
      fill: 'tozeroy',
      fillcolor: 'rgba(0, 210, 190, 0.08)',
      text: validPoints.map(
        (d) =>
          `Lap ${d.lap}<br>Cumulative Gap: ${formatDelta(d.cumulative_gap)}<br>Lap Delta: ${formatDelta(
            d.delta_seconds
          )}`
      ),
      hoverinfo: 'text',
    },
  ];

  return (
    <div className="telemetry-card p-5 mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#232B3E] pb-3 mb-4">
        <div>
          <h3 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
            Cumulative Race Gap & Lap-by-Lap Delta
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Positive values indicate {driver1.driver_code} is leading {driver2.driver_code}; negative values indicate {driver2.driver_code} is ahead.
          </p>
        </div>
      </div>

      <div className="w-full h-[320px]">
        <Plot
          data={traces}
          layout={{
            autosize: true,
            margin: { l: 50, r: 25, t: 15, b: 40 },
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            showlegend: false,
            xaxis: {
              title: { text: 'Lap Number', font: { color: '#94A3B8', size: 11 } },
              gridcolor: '#1E2638',
              zerolinecolor: '#1E2638',
              tickfont: { color: '#94A3B8', size: 10 },
            },
            yaxis: {
              title: { text: 'Cumulative Gap (Seconds)', font: { color: '#94A3B8', size: 11 } },
              gridcolor: '#1E2638',
              zerolinecolor: '#E10600',
              zerolinewidth: 2,
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
    </div>
  );
};
