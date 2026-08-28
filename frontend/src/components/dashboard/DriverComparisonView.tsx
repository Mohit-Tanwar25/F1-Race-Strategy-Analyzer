import React from 'react';
import type { DriverComparisonResponse } from '../../types';
import { DeltaComparisonChart } from '../charts/DeltaComparisonChart';
import { CompoundBadge } from '../common/CompoundBadge';
import { ArrowUpRight, ArrowDownRight, Minus, Zap } from 'lucide-react';

interface DriverComparisonViewProps {
  comparisonData: DriverComparisonResponse;
}

export const DriverComparisonView: React.FC<DriverComparisonViewProps> = ({
  comparisonData,
}) => {
  const {
    driver1,
    driver2,
    driver1_stints,
    driver2_stints,
    lap_deltas,
    key_strategic_differences,
  } = comparisonData;

  const renderPositionDelta = (gained?: number) => {
    if (gained === undefined || gained === null || gained === 0) {
      return (
        <span className="inline-flex items-center text-slate-400 text-xs font-bold font-mono">
          <Minus className="w-3 h-3 mr-0.5" /> 0 pos
        </span>
      );
    }
    if (gained > 0) {
      return (
        <span className="inline-flex items-center text-emerald-400 text-xs font-bold font-mono">
          <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> +{gained} pos
        </span>
      );
    }
    return (
      <span className="inline-flex items-center text-red-400 text-xs font-bold font-mono">
        <ArrowDownRight className="w-3.5 h-3.5 mr-0.5" /> {gained} pos
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Head-to-Head Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Driver 1 Card */}
        <div className="telemetry-card p-5 border-t-4 border-t-f1-red">
          <div className="flex items-center justify-between border-b border-[#232B3E] pb-3 mb-4">
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-f1-red">
                Driver A
              </span>
              <h3 className="text-xl font-black text-white font-mono flex items-center gap-2">
                {driver1.driver_code} — {driver1.driver_name}
              </h3>
              <p className="text-xs text-slate-400">{driver1.team}</p>
            </div>
            <div className="text-right">
              <div className="text-xs text-slate-400 font-semibold uppercase">Strategy Score</div>
              <div className="text-2xl font-black text-white font-mono">
                {driver1.score.total_score}
                <span className="text-xs text-slate-400 font-normal">/100</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2 mb-4 text-center">
            <div className="bg-[#0E131F] p-2.5 rounded-lg border border-[#232B3E]">
              <div className="text-[10px] text-slate-400 uppercase font-bold">Start</div>
              <div className="text-base font-black text-white font-mono">P{driver1.start_position || '—'}</div>
            </div>
            <div className="bg-[#0E131F] p-2.5 rounded-lg border border-[#232B3E]">
              <div className="text-[10px] text-slate-400 uppercase font-bold">Finish</div>
              <div className="text-base font-black text-white font-mono">P{driver1.finish_position || '—'}</div>
            </div>
            <div className="bg-[#0E131F] p-2.5 rounded-lg border border-[#232B3E]">
              <div className="text-[10px] text-slate-400 uppercase font-bold">Delta</div>
              <div className="mt-1">{renderPositionDelta(driver1.positions_gained)}</div>
            </div>
          </div>

          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
              Tyre Compound Sequence
            </div>
            <div className="flex flex-wrap gap-1.5">
              {driver1_stints.map((s, idx) => (
                <CompoundBadge
                  key={idx}
                  compound={s.compound}
                  tyreAge={s.end_lap - s.start_lap + 1}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Driver 2 Card */}
        <div className="telemetry-card p-5 border-t-4 border-t-cyan-400">
          <div className="flex items-center justify-between border-b border-[#232B3E] pb-3 mb-4">
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400">
                Driver B (Compare)
              </span>
              <h3 className="text-xl font-black text-white font-mono flex items-center gap-2">
                {driver2.driver_code} — {driver2.driver_name}
              </h3>
              <p className="text-xs text-slate-400">{driver2.team}</p>
            </div>
            <div className="text-right">
              <div className="text-xs text-slate-400 font-semibold uppercase">Strategy Score</div>
              <div className="text-2xl font-black text-white font-mono">
                {driver2.score.total_score}
                <span className="text-xs text-slate-400 font-normal">/100</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2 mb-4 text-center">
            <div className="bg-[#0E131F] p-2.5 rounded-lg border border-[#232B3E]">
              <div className="text-[10px] text-slate-400 uppercase font-bold">Start</div>
              <div className="text-base font-black text-white font-mono">P{driver2.start_position || '—'}</div>
            </div>
            <div className="bg-[#0E131F] p-2.5 rounded-lg border border-[#232B3E]">
              <div className="text-[10px] text-slate-400 uppercase font-bold">Finish</div>
              <div className="text-base font-black text-white font-mono">P{driver2.finish_position || '—'}</div>
            </div>
            <div className="bg-[#0E131F] p-2.5 rounded-lg border border-[#232B3E]">
              <div className="text-[10px] text-slate-400 uppercase font-bold">Delta</div>
              <div className="mt-1">{renderPositionDelta(driver2.positions_gained)}</div>
            </div>
          </div>

          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
              Tyre Compound Sequence
            </div>
            <div className="flex flex-wrap gap-1.5">
              {driver2_stints.map((s, idx) => (
                <CompoundBadge
                  key={idx}
                  compound={s.compound}
                  tyreAge={s.end_lap - s.start_lap + 1}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Delta Chart */}
      <DeltaComparisonChart
        driver1={driver1}
        driver2={driver2}
        lapDeltas={lap_deltas}
      />

      {/* Strategic Insights Breakdown */}
      <div className="telemetry-card p-5">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 mb-3">
          <Zap className="w-4 h-4 text-amber-400" />
          Key Strategic & Telemetry Discrepancies
        </h3>
        <ul className="space-y-2">
          {key_strategic_differences.map((diff, idx) => (
            <li
              key={idx}
              className="text-xs text-slate-300 bg-[#0E131F] p-3 rounded-lg border border-[#232B3E] flex items-start gap-2.5"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-1.5 flex-shrink-0" />
              <span>{diff}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
