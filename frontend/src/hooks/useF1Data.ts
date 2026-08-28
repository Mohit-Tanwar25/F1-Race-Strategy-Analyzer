import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { f1Api } from '../services/api';

export const useSeasons = () => {
  return useQuery({
    queryKey: ['seasons'],
    queryFn: f1Api.getSeasons,
  });
};

export const useRaces = (season: number) => {
  return useQuery({
    queryKey: ['races', season],
    queryFn: () => f1Api.getRacesBySeason(season),
    enabled: !!season,
  });
};

export const useRaceDetail = (raceId: number) => {
  return useQuery({
    queryKey: ['race', raceId],
    queryFn: () => f1Api.getRaceDetail(raceId),
    enabled: !!raceId,
  });
};

export const useRaceDrivers = (raceId: number) => {
  return useQuery({
    queryKey: ['raceDrivers', raceId],
    queryFn: () => f1Api.getRaceDrivers(raceId),
    enabled: !!raceId,
  });
};

export const useRaceStrategies = (raceId: number) => {
  return useQuery({
    queryKey: ['strategies', raceId],
    queryFn: () => f1Api.getRaceStrategies(raceId),
    enabled: !!raceId,
  });
};

export const useRaceEvents = (raceId: number) => {
  return useQuery({
    queryKey: ['events', raceId],
    queryFn: () => f1Api.getRaceEvents(raceId),
    enabled: !!raceId,
  });
};

export const useAllRaceLaps = (raceId: number, driverIds?: number[]) => {
  return useQuery({
    queryKey: ['allLaps', raceId, driverIds],
    queryFn: () => f1Api.getAllRaceLaps(raceId, driverIds),
    enabled: !!raceId,
  });
};

export const useDegradationAnalysis = (raceId: number, driverId?: number) => {
  return useQuery({
    queryKey: ['degradation', raceId, driverId],
    queryFn: () => f1Api.getDegradationAnalysis(raceId, driverId),
    enabled: !!raceId,
  });
};

export const useUndercutAnalysis = (raceId: number) => {
  return useQuery({
    queryKey: ['undercuts', raceId],
    queryFn: () => f1Api.getUndercutAnalysis(raceId),
    enabled: !!raceId,
  });
};

export const useOvercutAnalysis = (raceId: number) => {
  return useQuery({
    queryKey: ['overcuts', raceId],
    queryFn: () => f1Api.getOvercutAnalysis(raceId),
    enabled: !!raceId,
  });
};

export const useStrategyScores = (raceId: number) => {
  return useQuery({
    queryKey: ['scores', raceId],
    queryFn: () => f1Api.getStrategyScores(raceId),
    enabled: !!raceId,
  });
};

export const useDriverComparison = (raceId: number, driver1Id?: number, driver2Id?: number) => {
  return useQuery({
    queryKey: ['comparison', raceId, driver1Id, driver2Id],
    queryFn: () => f1Api.getDriverComparison(raceId, driver1Id!, driver2Id!),
    enabled: !!raceId && !!driver1Id && !!driver2Id,
  });
};

export const useIngestMutation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ season, round }: { season: number; round: number }) =>
      f1Api.triggerIngest(season, round),
    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });
};
