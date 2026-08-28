import axios from 'axios';
import type {
  Race,
  Driver,
  Lap,
  DriverStrategy,
  RaceEvent,
  DegradationResponse,
  UndercutDetail,
  OvercutDetail,
  DriverScore,
  DriverComparisonResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const f1Api = {
  getSeasons: async (): Promise<number[]> => {
    const res = await client.get('/seasons');
    return res.data;
  },

  getRacesBySeason: async (year: number): Promise<Race[]> => {
    const res = await client.get(`/seasons/${year}/races`);
    return res.data;
  },

  getRaceDetail: async (raceId: number): Promise<Race> => {
    const res = await client.get(`/races/${raceId}`);
    return res.data;
  },

  getRaceDrivers: async (raceId: number): Promise<Driver[]> => {
    const res = await client.get(`/races/${raceId}/drivers`);
    return res.data;
  },

  getDriverLaps: async (raceId: number, driverId: number): Promise<Lap[]> => {
    const res = await client.get(`/races/${raceId}/laps/${driverId}`);
    return res.data;
  },

  getAllRaceLaps: async (raceId: number, driverIds?: number[]): Promise<Lap[]> => {
    const params = driverIds && driverIds.length ? { drivers: driverIds.join(',') } : {};
    const res = await client.get(`/races/${raceId}/all-laps`, { params });
    return res.data;
  },

  getRaceStrategies: async (raceId: number): Promise<DriverStrategy[]> => {
    const res = await client.get(`/races/${raceId}/strategies`);
    return res.data;
  },

  getRaceEvents: async (raceId: number): Promise<RaceEvent[]> => {
    const res = await client.get(`/races/${raceId}/events`);
    return res.data;
  },

  getDegradationAnalysis: async (raceId: number, driverId?: number): Promise<DegradationResponse> => {
    const params = driverId ? { driver_id: driverId } : {};
    const res = await client.get(`/races/${raceId}/analysis/degradation`, { params });
    return res.data;
  },

  getUndercutAnalysis: async (raceId: number): Promise<UndercutDetail[]> => {
    const res = await client.get(`/races/${raceId}/analysis/undercuts`);
    return res.data;
  },

  getOvercutAnalysis: async (raceId: number): Promise<OvercutDetail[]> => {
    const res = await client.get(`/races/${raceId}/analysis/overcuts`);
    return res.data;
  },

  getStrategyScores: async (raceId: number): Promise<DriverScore[]> => {
    const res = await client.get(`/races/${raceId}/analysis/scores`);
    return res.data;
  },

  getDriverComparison: async (raceId: number, driver1Id: number, driver2Id: number): Promise<DriverComparisonResponse> => {
    const res = await client.get(`/races/${raceId}/compare`, {
      params: { driver1: driver1Id, driver2: driver2Id },
    });
    return res.data;
  },

  triggerIngest: async (season: number, round: number) => {
    const res = await client.post('/ingest', null, { params: { season, round } });
    return res.data;
  },
};
