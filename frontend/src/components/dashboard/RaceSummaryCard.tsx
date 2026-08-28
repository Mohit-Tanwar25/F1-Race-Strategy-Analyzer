import React from 'react';
import { Trophy, Timer, ShieldAlert, Wrench, MapPin, Flag } from 'lucide-react';
import type { Race } from '../../types';

interface RaceSummaryCardProps {
  race: Race;
}

export const RaceSummaryCard: React.FC<RaceSummaryCardProps> = ({ race }) => {
  return (
    <div className="telemetry-card p-5 mb-6 border-l-4 border-l-f1-red">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#232B3E] pb-4 mb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-f1-red uppercase tracking-wider">
            <span>Round {race.round}</span>
            <span>•</span>
            <span>{race.season} FIA Formula One World Championship</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-black text-white tracking-tight mt-1 flex items-center gap-2">
            {race.name}
          </h1>
          <div className="flex items-center gap-4 text-xs text-slate-400 mt-1 font-medium">
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              {race.circuit}, {race.country}
            </span>
            <span>•</span>
            <span>{race.date}</span>
          </div>
        </div>

        {/* Winner Highlight */}
        {race.winner_name && (
          <div className="bg-[#1C2333] border border-[#2B354C] rounded-xl px-4 py-3 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
              <Trophy className="w-5 h-5" />
            </div>
            <div>
              <div className="text-[10px] font-bold uppercase tracking-wider text-amber-400">
                Race Winner
              </div>
              <div className="text-base font-black text-white">
                {race.winner_name}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Quick Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-[#0E131F] rounded-lg p-3 border border-[#232B3E]">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Flag className="w-3.5 h-3.5 text-slate-400" />
            Total Laps
          </div>
          <div className="text-xl font-black text-white font-mono mt-1">
            {race.total_laps || 50} Laps
          </div>
        </div>

        <div className="bg-[#0E131F] rounded-lg p-3 border border-[#232B3E]">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Wrench className="w-3.5 h-3.5 text-amber-400" />
            Total Pit Stops
          </div>
          <div className="text-xl font-black text-white font-mono mt-1">
            {race.total_pit_stops || 0} Stops
          </div>
        </div>

        <div className="bg-[#0E131F] rounded-lg p-3 border border-[#232B3E]">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <ShieldAlert className="w-3.5 h-3.5 text-yellow-400" />
            SC / VSC Neutralizations
          </div>
          <div className="text-xl font-black text-white font-mono mt-1">
            {(race.safety_car_periods || 0) + (race.vsc_periods || 0)} Periods
          </div>
        </div>

        <div className="bg-[#0E131F] rounded-lg p-3 border border-[#232B3E]">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Timer className="w-3.5 h-3.5 text-purple-400" />
            Fastest Lap
          </div>
          <div className="text-sm font-black text-purple-300 font-mono mt-1">
            {race.fastest_lap
              ? `${race.fastest_lap.driver_code} (${race.fastest_lap.formatted_time})`
              : 'Data unavailable'}
          </div>
        </div>
      </div>
    </div>
  );
};
