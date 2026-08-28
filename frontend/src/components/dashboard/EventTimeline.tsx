import React, { useState } from 'react';
import { ShieldAlert, CloudRain, AlertTriangle, Info, Wrench } from 'lucide-react';
import type { RaceEvent, PitStop } from '../../types';

interface EventTimelineProps {
  events: RaceEvent[];
  pitStops?: PitStop[];
}

export const EventTimeline: React.FC<EventTimelineProps> = ({ events, pitStops = [] }) => {
  const [filter, setFilter] = useState<string>('ALL');

  // Combine race events and pit stop events
  const combined = [
    ...events.map((e) => ({
      lap: e.lap,
      start_lap: e.start_lap || e.lap,
      end_lap: e.end_lap || e.lap,
      type: e.event_type,
      title: `${e.event_type.replace('_', ' ')} (Laps ${e.start_lap || e.lap}-${e.end_lap || e.lap})`,
      description: e.description || '',
    })),
    ...pitStops.map((p) => ({
      lap: p.lap,
      start_lap: p.lap,
      end_lap: p.lap,
      type: 'PIT_STOP',
      title: `${p.driver_code} — Pit Stop #${p.stop_number}`,
      description: `Duration: ${p.duration ? p.duration + 's' : 'N/A'}`,
    })),
  ].sort((a, b) => a.lap - b.lap);

  const filtered = combined.filter((item) => {
    if (filter === 'ALL') return true;
    if (filter === 'NEUTRALIZATIONS') return item.type === 'SAFETY_CAR' || item.type === 'VSC';
    if (filter === 'WEATHER') return item.type === 'RAIN';
    if (filter === 'PITS') return item.type === 'PIT_STOP';
    return true;
  });

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'SAFETY_CAR':
      case 'VSC':
        return <ShieldAlert className="w-4 h-4 text-yellow-400" />;
      case 'RAIN':
        return <CloudRain className="w-4 h-4 text-cyan-400" />;
      case 'RED_FLAG':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'PIT_STOP':
        return <Wrench className="w-4 h-4 text-amber-400" />;
      default:
        return <Info className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="telemetry-card p-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#232B3E] pb-3 mb-4">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-yellow-400"></span>
            Race Incident & Strategy Log
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Chronological record of Safety Cars, VSC neutralizations, weather, and pit stops.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 text-xs">
          {['ALL', 'NEUTRALIZATIONS', 'WEATHER', 'PITS'].map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-2.5 py-1 rounded font-semibold transition-colors ${
                filter === cat
                  ? 'bg-f1-red text-white'
                  : 'bg-[#1C2333] text-slate-400 hover:text-white hover:bg-[#252E42]'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Events List */}
      <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
        {filtered.length === 0 ? (
          <div className="text-xs text-slate-500 text-center py-6">
            No events found for the selected category.
          </div>
        ) : (
          filtered.map((item, idx) => (
            <div
              key={idx}
              className="bg-[#0E131F] border border-[#232B3E] rounded-lg p-3 flex items-start gap-3 hover:border-[#34405D] transition-colors"
            >
              <div className="p-1.5 bg-[#171E2D] rounded border border-[#2A344C] flex-shrink-0 mt-0.5">
                {getEventIcon(item.type)}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-bold text-white uppercase tracking-wider">
                    {item.title}
                  </span>
                  <span className="text-[10px] font-mono font-bold bg-[#1C2333] text-slate-300 px-2 py-0.5 rounded">
                    Lap {item.lap}
                  </span>
                </div>
                {item.description && (
                  <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">
                    {item.description}
                  </p>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
