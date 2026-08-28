import React, { useState } from 'react';
import { Zap, CornerUpRight, CheckCircle2, XCircle } from 'lucide-react';
import type { UndercutDetail, OvercutDetail } from '../../types';

interface UndercutOvercutSectionProps {
  undercuts: UndercutDetail[];
  overcuts: OvercutDetail[];
}

export const UndercutOvercutSection: React.FC<UndercutOvercutSectionProps> = ({
  undercuts,
  overcuts,
}) => {
  const [tab, setTab] = useState<'UNDERCUTS' | 'OVERCUTS'>('UNDERCUTS');

  const items = tab === 'UNDERCUTS' ? undercuts : overcuts;

  return (
    <div className="telemetry-card p-5 mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#232B3E] pb-3 mb-4">
        <div>
          <h2 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            Strategic Pit Tactics: Undercut & Overcut Analysis
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Algorithmically detected strategic moves leveraging fresh-tyre out-laps vs extended stint overcuts.
          </p>
        </div>

        {/* Switcher Tabs */}
        <div className="flex items-center gap-2 bg-[#0E131F] p-1 rounded-lg border border-[#232B3E]">
          <button
            onClick={() => setTab('UNDERCUTS')}
            className={`px-3 py-1.5 rounded text-xs font-bold uppercase flex items-center gap-1.5 transition-colors ${
              tab === 'UNDERCUTS'
                ? 'bg-f1-red text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Zap className="w-3.5 h-3.5" />
            Undercuts ({undercuts.length})
          </button>
          <button
            onClick={() => setTab('OVERCUTS')}
            className={`px-3 py-1.5 rounded text-xs font-bold uppercase flex items-center gap-1.5 transition-colors ${
              tab === 'OVERCUTS'
                ? 'bg-f1-red text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <CornerUpRight className="w-3.5 h-3.5" />
            Overcuts ({overcuts.length})
          </button>
        </div>
      </div>

      {items.length === 0 ? (
        <div className="text-center py-8 text-slate-500 text-xs font-medium">
          No confirmed {tab.toLowerCase()} detected in this Grand Prix with the current conservative threshold.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          {items.map((item, idx) => (
            <div
              key={idx}
              className="bg-[#0E131F] border border-[#232B3E] rounded-xl p-4 flex flex-col justify-between hover:border-[#354360] transition-colors shadow-sm"
            >
              <div>
                {/* Header info */}
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-black text-white font-mono">
                      {item.attacker_code}
                    </span>
                    <span className="text-xs text-slate-400 font-medium">vs</span>
                    <span className="text-sm font-bold text-slate-300 font-mono">
                      {item.target_code}
                    </span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    {item.success ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2 py-0.5 rounded">
                        <CheckCircle2 className="w-3 h-3" />
                        Success
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/30 px-2 py-0.5 rounded">
                        <XCircle className="w-3 h-3" />
                        Defended
                      </span>
                    )}
                  </div>
                </div>

                {/* Metrics */}
                <div className="flex items-center gap-4 text-xs font-mono mb-3 bg-[#161D2B] p-2 rounded-lg border border-[#252F44]">
                  <div>
                    <span className="text-slate-400 text-[10px] block uppercase">Pit Lap</span>
                    <span className="font-bold text-white">Lap {item.pit_lap}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 text-[10px] block uppercase">Est. Gain</span>
                    <span className="font-bold text-emerald-400">+{item.estimated_gain_seconds}s</span>
                  </div>
                  <div>
                    <span className="text-slate-400 text-[10px] block uppercase">Confidence</span>
                    <span className="font-bold text-cyan-400">{(item.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed font-sans">
                  {item.explanation}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
