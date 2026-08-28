import React from 'react';
import type { DriverStrategy, RaceEvent } from '../../types';
import { getCompoundColor, getCompoundTextColor } from '../../utils/formatters';

interface StrategyTimelineProps {
  strategies: DriverStrategy[];
  events: RaceEvent[];
  totalLaps: number;
  selectedDriverId?: number;
  onSelectDriver: (driverId: number) => void;
}

export const StrategyTimeline: React.FC<StrategyTimelineProps> = ({
  strategies,
  events,
  totalLaps = 50,
  selectedDriverId,
  onSelectDriver,
}) => {
  const safeTotalLaps = Math.max(totalLaps, 50);

  // Safety Car / VSC intervals
  const scEvents = events.filter(
    (e) => e.event_type === 'SAFETY_CAR' || e.event_type === 'VSC'
  );

  return (
    <div className="telemetry-card p-5 mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div>
          <h2 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-f1-red"></span>
            Tyre Stint & Pit Strategy Timeline
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Compound allocation, stint durations, and pit stop execution across {safeTotalLaps} laps.
          </p>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-2 text-[11px] font-mono">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-[#FF1801]"></span> Soft
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-[#FFD800]"></span> Medium
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-[#FFFFFF]"></span> Hard
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-[#39B54A]"></span> Inter
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-[#00A3E0]"></span> Wet
          </span>
        </div>
      </div>

      {/* Timeline Gantt Chart */}
      <div className="relative overflow-x-auto">
        <div className="min-w-[700px]">
          {/* Lap Tick Header */}
          <div className="flex items-center text-[10px] text-slate-400 font-mono border-b border-[#232B3E] pb-2 mb-3">
            <div className="w-28 flex-shrink-0 font-bold uppercase">Driver</div>
            <div className="flex-1 relative h-4">
              {Array.from({ length: 6 }).map((_, i) => {
                const lapTick = Math.round((i * safeTotalLaps) / 5);
                const percent = (lapTick / safeTotalLaps) * 100;
                return (
                  <span
                    key={i}
                    className="absolute -translate-x-1/2"
                    style={{ left: `${percent}%` }}
                  >
                    L{lapTick === 0 ? 1 : lapTick}
                  </span>
                );
              })}
            </div>
          </div>

          {/* SC / VSC Overlay Background */}
          <div className="relative space-y-2.5">
            {scEvents.map((sc, idx) => {
              const start = sc.start_lap || sc.lap;
              const end = sc.end_lap || sc.lap;
              const leftPct = (start / safeTotalLaps) * 100;
              const widthPct = Math.max(((end - start + 1) / safeTotalLaps) * 100, 2);
              const isSC = sc.event_type === 'SAFETY_CAR';

              return (
                <div
                  key={idx}
                  className={`absolute top-0 bottom-0 pointer-events-none z-0 border-x ${
                    isSC
                      ? 'bg-yellow-500/10 border-yellow-500/40 text-yellow-300'
                      : 'bg-amber-500/10 border-amber-500/30 text-amber-300'
                  }`}
                  style={{ left: `calc(7rem + ${leftPct}%)`, width: `${widthPct}%` }}
                  title={`${sc.event_type}: Laps ${start}-${end}`}
                >
                  <span className="text-[9px] font-bold font-mono px-1 bg-[#10141E]/90 rounded absolute top-0 left-0">
                    {isSC ? 'SC' : 'VSC'}
                  </span>
                </div>
              );
            })}

            {/* Drivers Stint Bars */}
            {strategies.map((d) => {
              const isSelected = d.driver_id === selectedDriverId;

              return (
                <div
                  key={d.driver_id}
                  onClick={() => onSelectDriver(d.driver_id)}
                  className={`relative z-10 flex items-center p-1.5 rounded-lg cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-[#1D2536] ring-1 ring-f1-red shadow-md'
                      : 'hover:bg-[#161D2B]'
                  }`}
                >
                  {/* Driver Label */}
                  <div className="w-28 flex-shrink-0 flex items-center gap-2">
                    <span
                      className="w-1.5 h-6 rounded-full"
                      style={{ backgroundColor: d.team_color || '#E10600' }}
                    />
                    <div>
                      <div className="text-xs font-black text-white font-mono flex items-center gap-1">
                        {d.driver_code}
                      </div>
                      <div className="text-[10px] text-slate-400 truncate max-w-[80px]">
                        {d.team}
                      </div>
                    </div>
                  </div>

                  {/* Stint Track */}
                  <div className="flex-1 relative h-7 bg-[#0B0E16] rounded flex items-center overflow-hidden border border-[#1E2638]">
                    {d.stints.map((stint, sIdx) => {
                      const startLap = Math.max(1, stint.start_lap);
                      const endLap = Math.min(safeTotalLaps, stint.end_lap);
                      const stintLaps = endLap - startLap + 1;
                      const widthPercent = (stintLaps / safeTotalLaps) * 100;
                      const color = getCompoundColor(stint.compound);
                      const textColor = getCompoundTextColor(stint.compound);

                      return (
                        <div
                          key={sIdx}
                          className="h-full flex items-center justify-between px-2 font-mono text-[10px] font-bold border-r border-black/40 relative group transition-opacity hover:opacity-90"
                          style={{
                            width: `${widthPercent}%`,
                            backgroundColor: color,
                            color: textColor,
                          }}
                          title={`Stint ${stint.stint_number}: ${stint.compound} (Laps ${startLap}-${endLap}, ${stintLaps} laps)`}
                        >
                          <span className="truncate">{stint.compound.slice(0, 1)}</span>
                          <span className="text-[9px] opacity-80">{stintLaps}L</span>
                        </div>
                      );
                    })}

                    {/* Pit Stop Markers */}
                    {d.pit_stops.map((pit, pIdx) => {
                      const pitLeftPct = (pit.lap / safeTotalLaps) * 100;
                      return (
                        <div
                          key={pIdx}
                          className="absolute -top-1 -bottom-1 w-2 bg-slate-900 border-2 border-amber-400 rounded-sm -translate-x-1/2 z-20 flex items-center justify-center shadow-lg"
                          style={{ left: `${pitLeftPct}%` }}
                          title={`Pit Stop ${pit.stop_number} on Lap ${pit.lap} (${pit.duration ? pit.duration + 's' : 'Stop'})`}
                        />
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
