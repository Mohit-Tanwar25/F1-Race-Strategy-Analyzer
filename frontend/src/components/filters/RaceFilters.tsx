import React from 'react';
import { Calendar, Flag, User, UserPlus, RefreshCw } from 'lucide-react';
import type { Race, Driver } from '../../types';

interface RaceFiltersProps {
  seasons: number[];
  selectedSeason: number;
  onSelectSeason: (season: number) => void;
  races: Race[];
  selectedRaceId: number;
  onSelectRace: (raceId: number) => void;
  drivers: Driver[];
  selectedDriverId?: number;
  onSelectDriver: (driverId: number) => void;
  compareDriverId?: number;
  onSelectCompareDriver: (driverId?: number) => void;
  onRefreshData?: () => void;
  isIngesting?: boolean;
}

export const RaceFilters: React.FC<RaceFiltersProps> = ({
  seasons,
  selectedSeason,
  onSelectSeason,
  races,
  selectedRaceId,
  onSelectRace,
  drivers,
  selectedDriverId,
  onSelectDriver,
  compareDriverId,
  onSelectCompareDriver,
  onRefreshData,
  isIngesting,
}) => {
  return (
    <div className="telemetry-card p-4 mb-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 items-end">
        {/* Season Selector */}
        <div>
          <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5 text-f1-red" />
            Season
          </label>
          <select
            value={selectedSeason}
            onChange={(e) => onSelectSeason(Number(e.target.value))}
            className="w-full bg-[#0E131F] border border-[#232B3E] rounded-lg px-3 py-2 text-sm font-semibold text-white focus:outline-none focus:border-f1-red transition-colors"
          >
            {seasons.map((s) => (
              <option key={s} value={s}>
                {s} Season
              </option>
            ))}
          </select>
        </div>

        {/* Race Selector */}
        <div>
          <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1.5">
            <Flag className="w-3.5 h-3.5 text-f1-red" />
            Grand Prix
          </label>
          <select
            value={selectedRaceId}
            onChange={(e) => onSelectRace(Number(e.target.value))}
            className="w-full bg-[#0E131F] border border-[#232B3E] rounded-lg px-3 py-2 text-sm font-semibold text-white focus:outline-none focus:border-f1-red transition-colors"
          >
            {races.map((r) => (
              <option key={r.id} value={r.id}>
                R{r.round}: {r.name}
              </option>
            ))}
          </select>
        </div>

        {/* Primary Driver Selector */}
        <div>
          <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1.5">
            <User className="w-3.5 h-3.5 text-f1-red" />
            Primary Driver
          </label>
          <select
            value={selectedDriverId || ''}
            onChange={(e) => onSelectDriver(Number(e.target.value))}
            className="w-full bg-[#0E131F] border border-[#232B3E] rounded-lg px-3 py-2 text-sm font-semibold text-white focus:outline-none focus:border-f1-red transition-colors"
          >
            {drivers.map((d) => (
              <option key={d.id} value={d.id}>
                {d.driver_code} - {d.full_name} ({d.team})
              </option>
            ))}
          </select>
        </div>

        {/* Compare Driver Selector */}
        <div>
          <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center gap-1.5">
            <UserPlus className="w-3.5 h-3.5 text-cyan-400" />
            Compare Driver (Optional)
          </label>
          <select
            value={compareDriverId || ''}
            onChange={(e) =>
              onSelectCompareDriver(e.target.value ? Number(e.target.value) : undefined)
            }
            className="w-full bg-[#0E131F] border border-[#232B3E] rounded-lg px-3 py-2 text-sm font-semibold text-white focus:outline-none focus:border-cyan-500 transition-colors"
          >
            <option value="">-- None (Single Analysis) --</option>
            {drivers
              .filter((d) => d.id !== selectedDriverId)
              .map((d) => (
                <option key={d.id} value={d.id}>
                  {d.driver_code} - {d.full_name} ({d.team})
                </option>
              ))}
          </select>
        </div>

        {/* Ingestion & Refresh Action */}
        <div className="flex items-center gap-2">
          {onRefreshData && (
            <button
              onClick={onRefreshData}
              disabled={isIngesting}
              className="w-full bg-[#1F2739] hover:bg-[#2B354C] disabled:opacity-50 text-slate-200 border border-[#2F3950] rounded-lg px-3 py-2 text-xs font-bold uppercase tracking-wider flex items-center justify-center gap-2 transition-all"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isIngesting ? 'animate-spin text-f1-red' : ''}`} />
              {isIngesting ? 'Ingesting...' : 'Sync Telemetry'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
