from typing import List, Dict, Any, Optional, Set
import numpy as np
from scipy import stats
from app.models.lap import Lap
from app.models.stint import Stint
from app.models.race_event import RaceEvent


def calculate_stint_degradation(
    stint: Stint,
    laps: List[Lap],
    sc_vsc_laps: Set[int],
) -> Dict[str, Any]:
    """
    Calculate estimated tyre degradation for a single stint.
    Filters out SC/VSC laps, in-laps (pit lap), out-laps (first lap of stint),
    and anomalous timing spikes.
    """
    stint_laps = [
        l for l in laps
        if stint.start_lap <= l.lap_number <= stint.end_lap
    ]
    sorted_stint_laps = sorted(stint_laps, key=lambda x: x.lap_number)

    valid_lap_points = []
    lap_times = []
    tyre_ages = []

    for i, l in enumerate(sorted_stint_laps):
        # Filter out invalid or missing lap times
        if not l.lap_time or l.lap_time <= 0 or not l.is_valid:
            continue

        # Filter out SC / VSC affected laps
        if l.lap_number in sc_vsc_laps:
            continue

        # In-lap (pit stop lap) or out-lap (first lap of stint after lap 1)
        is_in_lap = l.pit_stop or (i == len(sorted_stint_laps) - 1 and stint.end_lap < (laps[-1].lap_number if laps else 0))
        is_out_lap = (i == 0 and stint.start_lap > 1)
        if is_in_lap or is_out_lap:
            continue

        # Calculate tyre age for this lap
        lap_tyre_age = stint.tyre_age_start + (l.lap_number - stint.start_lap + 1)

        valid_lap_points.append({
            "lap_number": l.lap_number,
            "lap_time": round(l.lap_time, 3),
            "tyre_age": lap_tyre_age,
        })
        lap_times.append(l.lap_time)
        tyre_ages.append(lap_tyre_age)

    # Basic stats
    if not lap_times:
        return {
            "stint_number": stint.stint_number,
            "compound": stint.compound.upper(),
            "laps_count": len(sorted_stint_laps),
            "start_lap": stint.start_lap,
            "end_lap": stint.end_lap,
            "avg_lap_time": 0.0,
            "best_lap_time": 0.0,
            "degradation_rate_per_lap": 0.0,
            "pace_deterioration_total": 0.0,
            "r_squared": 0.0,
            "confidence": 0.0,
            "valid_laps": [],
        }

    # Filter extreme outliers (> 110% of median or < 90%)
    med_time = np.median(lap_times)
    filtered_points = [
        p for p in valid_lap_points
        if 0.85 * med_time <= p["lap_time"] <= 1.15 * med_time
    ]

    if len(filtered_points) >= 3:
        x = np.array([p["tyre_age"] for p in filtered_points])
        y = np.array([p["lap_time"] for p in filtered_points])

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        r_squared = float(r_value ** 2) if not np.isnan(r_value) else 0.0
        deg_rate = float(slope) if not np.isnan(slope) else 0.0
        pace_loss = round(deg_rate * (stint.end_lap - stint.start_lap), 3)

        # Confidence based on number of representative laps & R^2
        sample_conf = min(len(filtered_points) / 15.0, 1.0)
        confidence = round(0.5 * sample_conf + 0.5 * min(r_squared * 1.5, 1.0), 2)
    else:
        deg_rate = 0.0
        pace_loss = 0.0
        r_squared = 0.0
        confidence = 0.2

    avg_time = float(np.mean([p["lap_time"] for p in filtered_points])) if filtered_points else float(np.mean(lap_times))
    best_time = float(np.min([p["lap_time"] for p in filtered_points])) if filtered_points else float(np.min(lap_times))

    return {
        "stint_number": stint.stint_number,
        "compound": stint.compound.upper(),
        "laps_count": len(sorted_stint_laps),
        "start_lap": stint.start_lap,
        "end_lap": stint.end_lap,
        "avg_lap_time": round(avg_time, 3),
        "best_lap_time": round(best_time, 3),
        "degradation_rate_per_lap": round(deg_rate, 4),
        "pace_deterioration_total": max(pace_loss, 0.0),
        "r_squared": round(r_squared, 3),
        "confidence": confidence,
        "valid_laps": filtered_points,
    }


def get_sc_vsc_lap_set(events: List[RaceEvent]) -> Set[int]:
    """
    Return the set of all lap numbers affected by SC or VSC.
    """
    sc_laps = set()
    for e in events:
        if e.event_type in ("SAFETY_CAR", "VSC", "RED_FLAG"):
            start = e.start_lap or e.lap
            end = e.end_lap or e.lap
            for l in range(start, end + 1):
                sc_laps.add(l)
    return sc_laps
