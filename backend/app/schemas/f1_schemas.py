from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class DriverBase(BaseModel):
    driver_code: str
    full_name: str
    permanent_number: Optional[int] = None
    team: str
    team_color: Optional[str] = "#E10600"


class DriverResponse(DriverBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RaceBase(BaseModel):
    season: int
    round: int
    name: str
    circuit: str
    country: str
    date: str
    total_laps: Optional[int] = None
    winner_name: Optional[str] = None


class RaceResponse(RaceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RaceSummaryResponse(RaceResponse):
    drivers_count: int = 0
    total_pit_stops: int = 0
    safety_car_periods: int = 0
    vsc_periods: int = 0
    fastest_lap: Optional[Dict[str, Any]] = None


class LapResponse(BaseModel):
    id: int
    race_id: int
    driver_id: int
    driver_code: Optional[str] = None
    lap_number: int
    lap_time: Optional[float] = None
    sector_1: Optional[float] = None
    sector_2: Optional[float] = None
    sector_3: Optional[float] = None
    position: Optional[int] = None
    pit_stop: bool = False
    is_valid: bool = True
    model_config = ConfigDict(from_attributes=True)


class PitStopResponse(BaseModel):
    id: int
    race_id: int
    driver_id: int
    driver_code: Optional[str] = None
    lap: int
    duration: Optional[float] = None
    stop_number: int
    model_config = ConfigDict(from_attributes=True)


class StintResponse(BaseModel):
    id: Optional[int] = None
    driver_id: Optional[int] = None
    driver_code: Optional[str] = None
    stint_number: int
    start_lap: int
    end_lap: int
    compound: str
    tyre_age_start: int = 0
    tyre_age_end: int = 0
    stint_length: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class DriverStrategyResponse(BaseModel):
    driver_id: int
    driver_code: str
    driver_name: str
    team: str
    team_color: str
    stints: List[StintResponse]
    pit_stops: List[PitStopResponse]


class RaceEventResponse(BaseModel):
    id: int
    race_id: int
    lap: int
    start_lap: Optional[int] = None
    end_lap: Optional[int] = None
    event_type: str  # SAFETY_CAR, VSC, RED_FLAG, RAIN, OTHER
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# Analysis Schemas
class StintDegradation(BaseModel):
    stint_number: int
    compound: str
    laps_count: int
    start_lap: int
    end_lap: int
    avg_lap_time: float
    best_lap_time: float
    degradation_rate_per_lap: float  # seconds/lap (+ means getting slower)
    pace_deterioration_total: float  # total seconds lost over stint
    r_squared: float
    confidence: float
    valid_laps: List[Dict[str, Any]]


class DriverDegradation(BaseModel):
    driver_id: int
    driver_code: str
    driver_name: str
    team: str
    overall_avg_pace: float
    stints: List[StintDegradation]


class DegradationAnalysisResponse(BaseModel):
    race_id: int
    race_name: str
    drivers: List[DriverDegradation]
    disclaimer: str = "Estimated Tyre Degradation: Derived from statistical stint lap time progression excluding SC/VSC and in/out laps. Not a physical tyre simulation."


class UndercutDetail(BaseModel):
    type: str = "UNDERCUT"
    attacker_id: int
    attacker_code: str
    attacker_name: str
    attacker_team: str
    target_id: int
    target_code: str
    target_name: str
    target_team: str
    pit_lap: int
    target_pit_lap: Optional[int] = None
    estimated_gain_seconds: float
    confidence: float
    success: bool
    explanation: str


class OvercutDetail(BaseModel):
    type: str = "OVERCUT"
    attacker_id: int
    attacker_code: str
    attacker_name: str
    attacker_team: str
    target_id: int
    target_code: str
    target_name: str
    target_team: str
    pit_lap: int
    target_pit_lap: Optional[int] = None
    estimated_gain_seconds: float
    confidence: float
    success: bool
    explanation: str


class StrategyScoreBreakdown(BaseModel):
    pace_efficiency: float = Field(..., description="Out of 35 points")
    position_gain: float = Field(..., description="Out of 30 points")
    tyre_efficiency: float = Field(..., description="Out of 20 points")
    pit_stop_efficiency: float = Field(..., description="Out of 15 points")
    total_score: float = Field(..., description="Total score out of 100")
    rating: str = "Effective"


class DriverScore(BaseModel):
    driver_id: int
    driver_code: str
    driver_name: str
    team: str
    start_position: Optional[int] = None
    finish_position: Optional[int] = None
    positions_gained: Optional[int] = None
    score: StrategyScoreBreakdown
    summary: str


class LapDeltaPoint(BaseModel):
    lap: int
    driver1_lap_time: Optional[float] = None
    driver2_lap_time: Optional[float] = None
    delta_seconds: Optional[float] = None  # driver1 - driver2
    cumulative_gap: Optional[float] = None  # gap in seconds between d1 and d2
    driver1_compound: Optional[str] = None
    driver2_compound: Optional[str] = None


class DriverComparisonResponse(BaseModel):
    race_id: int
    race_name: str
    driver1: DriverScore
    driver2: DriverScore
    driver1_stints: List[StintResponse]
    driver2_stints: List[StintResponse]
    driver1_pit_stops: List[PitStopResponse]
    driver2_pit_stops: List[PitStopResponse]
    lap_deltas: List[LapDeltaPoint]
    faster_driver_code: str
    key_strategic_differences: List[str]
