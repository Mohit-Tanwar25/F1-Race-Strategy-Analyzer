import React, { useState, useEffect } from 'react';
import { Navbar } from './components/common/Navbar';
import { RaceFilters } from './components/filters/RaceFilters';
import { RaceSummaryCard } from './components/dashboard/RaceSummaryCard';
import { StrategyTimeline } from './components/dashboard/StrategyTimeline';
import { PlotlyLapTimesChart } from './components/charts/PlotlyLapTimesChart';
import { DegradationChart } from './components/charts/DegradationChart';
import { StrategyScoreCard } from './components/dashboard/StrategyScoreCard';
import { UndercutOvercutSection } from './components/dashboard/UndercutOvercutSection';
import { DriverComparisonView } from './components/dashboard/DriverComparisonView';
import { EventTimeline } from './components/dashboard/EventTimeline';
import { LoadingSkeleton } from './components/common/LoadingSkeleton';
import { ErrorBanner } from './components/common/ErrorBanner';
import {
  useSeasons,
  useRaces,
  useRaceDetail,
  useRaceDrivers,
  useRaceStrategies,
  useRaceEvents,
  useAllRaceLaps,
  useDegradationAnalysis,
  useUndercutAnalysis,
  useOvercutAnalysis,
  useStrategyScores,
  useDriverComparison,
  useIngestMutation,
} from './hooks/useF1Data';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [selectedSeason, setSelectedSeason] = useState<number>(2024);
  const [selectedRaceId, setSelectedRaceId] = useState<number>(1);
  const [selectedDriverId, setSelectedDriverId] = useState<number>(1);
  const [compareDriverId, setCompareDriverId] = useState<number | undefined>(undefined);

  // Queries
  const { data: seasons = [2024, 2023] } = useSeasons();
  const { data: races = [] } = useRaces(selectedSeason);

  // Set default selectedRaceId when races load
  useEffect(() => {
    if (races.length > 0 && (!selectedRaceId || !races.some((r) => r.id === selectedRaceId))) {
      setSelectedRaceId(races[0].id);
    }
  }, [races, selectedRaceId]);

  const {
    data: raceDetail,
    isLoading: loadingDetail,
    error: detailError,
    refetch: refetchRaceDetail,
  } = useRaceDetail(selectedRaceId);

  const { data: drivers = [] } = useRaceDrivers(selectedRaceId);

  // Set default primary driver when drivers load
  useEffect(() => {
    if (drivers.length > 0 && (!selectedDriverId || !drivers.some((d) => d.id === selectedDriverId))) {
      setSelectedDriverId(drivers[0].id);
    }
  }, [drivers, selectedDriverId]);

  const { data: strategies = [], isLoading: loadingStrategies } = useRaceStrategies(selectedRaceId);
  const { data: events = [] } = useRaceEvents(selectedRaceId);

  // Lap times for selected drivers
  const lapDriverIds = compareDriverId ? [selectedDriverId, compareDriverId] : [selectedDriverId];
  const { data: laps = [] } = useAllRaceLaps(selectedRaceId, lapDriverIds);

  const primaryDriverLaps = laps.filter((l) => l.driver_id === selectedDriverId);
  const compareDriverLaps = compareDriverId ? laps.filter((l) => l.driver_id === compareDriverId) : [];

  const primaryDriver = drivers.find((d) => d.id === selectedDriverId);
  const compareDriver = drivers.find((d) => d.id === compareDriverId);

  // Strategy Analysis Queries
  const { data: degradationData } = useDegradationAnalysis(selectedRaceId, selectedDriverId);
  const { data: undercuts = [] } = useUndercutAnalysis(selectedRaceId);
  const { data: overcuts = [] } = useOvercutAnalysis(selectedRaceId);
  const { data: strategyScores = [] } = useStrategyScores(selectedRaceId);
  const selectedDriverScore = strategyScores.find((s) => s.driver_id === selectedDriverId);

  const { data: comparisonData, isLoading: loadingComparison } = useDriverComparison(
    selectedRaceId,
    selectedDriverId,
    compareDriverId
  );

  const ingestMutation = useIngestMutation();

  const handleSyncTelemetry = () => {
    const raceObj = races.find((r) => r.id === selectedRaceId);
    if (raceObj) {
      ingestMutation.mutate({ season: selectedSeason, round: raceObj.round });
    }
  };

  const primaryDriverDeg = degradationData?.drivers?.find((d) => d.driver_id === selectedDriverId);

  return (
    <div className="min-h-screen bg-[#0A0E17] text-slate-100 flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full">
        {/* Global Selectors */}
        <RaceFilters
          seasons={seasons}
          selectedSeason={selectedSeason}
          onSelectSeason={setSelectedSeason}
          races={races}
          selectedRaceId={selectedRaceId}
          onSelectRace={setSelectedRaceId}
          drivers={drivers}
          selectedDriverId={selectedDriverId}
          onSelectDriver={setSelectedDriverId}
          compareDriverId={compareDriverId}
          onSelectCompareDriver={(id) => {
            setCompareDriverId(id);
            if (id) {
              setActiveTab('comparison');
            }
          }}
          onRefreshData={handleSyncTelemetry}
          isIngesting={ingestMutation.isPending}
        />

        {/* Global Error Banner */}
        {detailError && (
          <div className="mb-6">
            <ErrorBanner
              message="Failed to load race strategy telemetry. Please verify backend service status."
              onRetry={() => refetchRaceDetail()}
            />
          </div>
        )}

        {/* Loading Skeleton */}
        {loadingDetail && (
          <div className="mb-6">
            <LoadingSkeleton rows={3} height="h-24" />
          </div>
        )}

        {/* Race Overview Card */}
        {raceDetail && <RaceSummaryCard race={raceDetail} />}

        {/* TAB 1: MAIN DASHBOARD & TELEMETRY */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            {/* Strategy Timeline Gantt */}
            {loadingStrategies ? (
              <LoadingSkeleton rows={5} height="h-10" />
            ) : (
              <StrategyTimeline
                strategies={strategies}
                events={events}
                totalLaps={raceDetail?.total_laps || 50}
                selectedDriverId={selectedDriverId}
                onSelectDriver={setSelectedDriverId}
              />
            )}

            {/* Lap Time Pace Chart */}
            <PlotlyLapTimesChart
              primaryDriverLaps={primaryDriverLaps}
              compareDriverLaps={compareDriverLaps}
              primaryDriver={primaryDriver}
              compareDriver={compareDriver}
              events={events}
            />

            {/* Tyre Degradation & Strategy Score Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <DegradationChart degradationData={primaryDriverDeg} />
              <StrategyScoreCard scoreData={selectedDriverScore} />
            </div>

            {/* Undercut & Overcut Highlights */}
            <UndercutOvercutSection undercuts={undercuts} overcuts={overcuts} />
          </div>
        )}

        {/* TAB 2: HEAD-TO-HEAD COMPARISON */}
        {activeTab === 'comparison' && (
          <div>
            {!compareDriverId ? (
              <div className="telemetry-card p-8 text-center">
                <h3 className="text-lg font-black text-white uppercase tracking-wider mb-2">
                  Select a Comparison Driver
                </h3>
                <p className="text-xs text-slate-400 max-w-md mx-auto mb-4">
                  Choose a second competitor from the dropdown above to unlock full telemetry deltas, stint comparison, and head-to-head strategy effectiveness ratings.
                </p>
              </div>
            ) : loadingComparison ? (
              <LoadingSkeleton rows={6} height="h-20" />
            ) : comparisonData ? (
              <DriverComparisonView comparisonData={comparisonData} />
            ) : null}
          </div>
        )}

        {/* TAB 3: UNDERCUT & OVERCUT TACTICS */}
        {activeTab === 'tactics' && (
          <div className="space-y-6">
            <UndercutOvercutSection undercuts={undercuts} overcuts={overcuts} />
          </div>
        )}

        {/* TAB 4: RACE INCIDENTS & EVENTS */}
        {activeTab === 'events' && (
          <div className="space-y-6">
            <EventTimeline events={events} pitStops={strategies.flatMap((s) => s.pit_stops)} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-[#1C2333] bg-[#0A0E17] py-6 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>F1 Race Strategy Analyzer &copy; 2026 — Professional Motorsport Analytics</span>
          <span className="font-mono text-[11px]">Built with FastAPI, React, TypeScript & Plotly.js</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
