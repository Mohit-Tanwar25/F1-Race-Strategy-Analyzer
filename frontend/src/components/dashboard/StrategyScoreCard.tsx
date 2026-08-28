import React from 'react';
import { Target, Activity, Award, Wrench } from 'lucide-react';
import type { DriverScore } from '../../types';

interface StrategyScoreCardProps {
  scoreData?: DriverScore;
}

export const StrategyScoreCard: React.FC<StrategyScoreCardProps> = ({ scoreData }) => {
  if (!scoreData) {
    return (
      <div className="telemetry-card p-5">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
          Strategy Effectiveness Score
        </h3>
        <p className="text-xs text-slate-500 mt-2">Select a driver to view strategy scoring.</p>
      </div>
    );
  }

  const { score, driver_code, driver_name, team, positions_gained } = scoreData;

  const getRatingColor = (rating: string) => {
    switch (rating.toLowerCase()) {
      case 'exceptional':
        return 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10';
      case 'highly effective':
        return 'text-cyan-400 border-cyan-500/40 bg-cyan-500/10';
      case 'solid':
        return 'text-amber-400 border-amber-500/40 bg-amber-500/10';
      default:
        return 'text-red-400 border-red-500/40 bg-red-500/10';
    }
  };

  return (
    <div className="telemetry-card p-5">
      <div className="flex items-center justify-between border-b border-[#232B3E] pb-3 mb-4">
        <div>
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Target className="w-3.5 h-3.5 text-f1-red" />
            Strategy Effectiveness Score
          </div>
          <div className="text-sm font-bold text-white mt-0.5">
            {driver_code} — {driver_name} ({team})
          </div>
        </div>

        <div
          className={`px-3 py-1 rounded-full border text-xs font-bold uppercase tracking-wider ${getRatingColor(
            score.rating
          )}`}
        >
          {score.rating}
        </div>
      </div>

      {/* Main Score Radial / Number */}
      <div className="flex items-center gap-6 mb-6">
        <div className="flex-shrink-0 text-center">
          <div className="text-4xl font-black font-mono text-white tracking-tight">
            {score.total_score}
            <span className="text-lg font-normal text-slate-400">/100</span>
          </div>
          <div className="text-[11px] font-semibold text-slate-400 uppercase mt-0.5">
            Composite Index
          </div>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed">
          {scoreData.summary}
        </p>
      </div>

      {/* 4 Component Bars */}
      <div className="space-y-3.5">
        {/* Pace Efficiency */}
        <div>
          <div className="flex items-center justify-between text-xs font-medium mb-1">
            <span className="flex items-center gap-1.5 text-slate-300">
              <Activity className="w-3.5 h-3.5 text-cyan-400" />
              Pace Efficiency (Consistency & Stint Pace)
            </span>
            <span className="font-mono font-bold text-white">
              {score.pace_efficiency} <span className="text-slate-500 font-normal">/ 35</span>
            </span>
          </div>
          <div className="w-full h-2 bg-[#0E131F] rounded-full overflow-hidden">
            <div
              className="h-full bg-cyan-400 rounded-full transition-all duration-500"
              style={{ width: `${(score.pace_efficiency / 35) * 100}%` }}
            />
          </div>
        </div>

        {/* Position Gain */}
        <div>
          <div className="flex items-center justify-between text-xs font-medium mb-1">
            <span className="flex items-center gap-1.5 text-slate-300">
              <Award className="w-3.5 h-3.5 text-emerald-400" />
              Track Position Gain ({positions_gained !== undefined && positions_gained >= 0 ? `+${positions_gained}` : positions_gained} pos)
            </span>
            <span className="font-mono font-bold text-white">
              {score.position_gain} <span className="text-slate-500 font-normal">/ 30</span>
            </span>
          </div>
          <div className="w-full h-2 bg-[#0E131F] rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-400 rounded-full transition-all duration-500"
              style={{ width: `${(score.position_gain / 30) * 100}%` }}
            />
          </div>
        </div>

        {/* Tyre Management */}
        <div>
          <div className="flex items-center justify-between text-xs font-medium mb-1">
            <span className="flex items-center gap-1.5 text-slate-300">
              <Target className="w-3.5 h-3.5 text-amber-400" />
              Tyre Compound Efficiency & Life Management
            </span>
            <span className="font-mono font-bold text-white">
              {score.tyre_efficiency} <span className="text-slate-500 font-normal">/ 20</span>
            </span>
          </div>
          <div className="w-full h-2 bg-[#0E131F] rounded-full overflow-hidden">
            <div
              className="h-full bg-amber-400 rounded-full transition-all duration-500"
              style={{ width: `${(score.tyre_efficiency / 20) * 100}%` }}
            />
          </div>
        </div>

        {/* Pit Stop Timing */}
        <div>
          <div className="flex items-center justify-between text-xs font-medium mb-1">
            <span className="flex items-center gap-1.5 text-slate-300">
              <Wrench className="w-3.5 h-3.5 text-purple-400" />
              Pit-Stop Execution & Neutralization Timing
            </span>
            <span className="font-mono font-bold text-white">
              {score.pit_stop_efficiency} <span className="text-slate-500 font-normal">/ 15</span>
            </span>
          </div>
          <div className="w-full h-2 bg-[#0E131F] rounded-full overflow-hidden">
            <div
              className="h-full bg-purple-400 rounded-full transition-all duration-500"
              style={{ width: `${(score.pit_stop_efficiency / 15) * 100}%` }}
            />
          </div>
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-[#232B3E] text-[10px] text-slate-400">
        Proprietary analytical index measuring execution efficiency. Not an official FIA/F1 metric.
      </div>
    </div>
  );
};
