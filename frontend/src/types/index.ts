export interface Race {
  id: number;
  season: number;
  round: number;
  name: string;
  circuit: string;
  country: string;
  date: string;
  total_laps?: number;
  winner_name?: string;
  drivers_count?: number;
  total_pit_stops?: number;
  safety_car_periods?: number;
  vsc_periods?: number;
  fastest_lap?: {
    driver_code: string;
    driver_name: string;
    team: string;
    lap_number: number;
    lap_time: number;
    formatted_time: string;
  };
}

export interface Driver {
  id: number;
  driver_code: string;
  full_name: string;
  permanent_number?: number;
  team: string;
  team_color: string;
}

export interface Lap {
  id: number;
  race_id: number;
  driver_id: number;
  driver_code?: string;
  lap_number: number;
  lap_time?: number;
  sector_1?: number;
  sector_2?: number;
  sector_3?: number;
  position?: number;
  pit_stop: boolean;
  is_valid: boolean;
}

export interface Stint {
  id?: number;
  driver_id?: number;
  driver_code?: string;
  stint_number: number;
  start_lap: number;
  end_lap: number;
  compound: string;
  tyre_age_start: number;
  tyre_age_end: number;
  stint_length?: number;
}

export interface PitStop {
  id: number;
  race_id: number;
  driver_id: number;
  driver_code?: string;
  lap: number;
  duration?: number;
  stop_number: number;
}

export interface DriverStrategy {
  driver_id: number;
  driver_code: string;
  driver_name: string;
  team: string;
  team_color: string;
  stints: Stint[];
  pit_stops: PitStop[];
}

export interface RaceEvent {
  id: number;
  race_id: number;
  lap: number;
  start_lap?: number;
  end_lap?: number;
  event_type: 'SAFETY_CAR' | 'VSC' | 'RED_FLAG' | 'RAIN' | 'OTHER';
  description?: string;
}

export interface StintDegradation {
  stint_number: number;
  compound: string;
  laps_count: number;
  start_lap: number;
  end_lap: number;
  avg_lap_time: number;
  best_lap_time: number;
  degradation_rate_per_lap: number;
  pace_deterioration_total: number;
  r_squared: number;
  confidence: number;
  valid_laps: {
    lap_number: number;
    lap_time: number;
    tyre_age: number;
  }[];
}

export interface DriverDegradation {
  driver_id: number;
  driver_code: string;
  driver_name: string;
  team: string;
  overall_avg_pace: number;
  stints: StintDegradation[];
}

export interface DegradationResponse {
  race_id: number;
  race_name: string;
  drivers: DriverDegradation[];
  disclaimer: string;
}

export interface UndercutDetail {
  type: string;
  attacker_id: number;
  attacker_code: string;
  attacker_name: string;
  attacker_team: string;
  target_id: number;
  target_code: string;
  target_name: string;
  target_team: string;
  pit_lap: number;
  target_pit_lap?: number;
  estimated_gain_seconds: number;
  confidence: number;
  success: boolean;
  explanation: string;
}

export interface OvercutDetail {
  type: string;
  attacker_id: number;
  attacker_code: string;
  attacker_name: string;
  attacker_team: string;
  target_id: number;
  target_code: string;
  target_name: string;
  target_team: string;
  pit_lap: number;
  target_pit_lap?: number;
  estimated_gain_seconds: number;
  confidence: number;
  success: boolean;
  explanation: string;
}

export interface StrategyScoreBreakdown {
  pace_efficiency: number;
  position_gain: number;
  tyre_efficiency: number;
  pit_stop_efficiency: number;
  total_score: number;
  rating: string;
}

export interface DriverScore {
  driver_id: number;
  driver_code: string;
  driver_name: string;
  team: string;
  start_position?: number;
  finish_position?: number;
  positions_gained?: number;
  score: StrategyScoreBreakdown;
  summary: string;
}

export interface LapDeltaPoint {
  lap: number;
  driver1_lap_time?: number;
  driver2_lap_time?: number;
  delta_seconds?: number;
  cumulative_gap?: number;
  driver1_compound?: string;
  driver2_compound?: string;
}

export interface DriverComparisonResponse {
  race_id: number;
  race_name: string;
  driver1: DriverScore;
  driver2: DriverScore;
  driver1_stints: Stint[];
  driver2_stints: Stint[];
  driver1_pit_stops: PitStop[];
  driver2_pit_stops: PitStop[];
  lap_deltas: LapDeltaPoint[];
  faster_driver_code: string;
  key_strategic_differences: string[];
}
