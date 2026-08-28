from typing import List, Dict, Any, Optional
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.models.race_event import RaceEvent
from app.analysis.strategy_score import calculate_strategy_effectiveness_score
from app.analysis.stints import format_stints_response


def compare_two_drivers(
    driver1: Driver,
    driver2: Driver,
    laps1: List[Lap],
    laps2: List[Lap],
    stints1: List[Stint],
    stints2: List[Stint],
    pits1: List[PitStop],
    pits2: List[PitStop],
    events: List[RaceEvent],
    total_laps: int = 50,
) -> Dict[str, Any]:
    """
    Produce a full head-to-head comparison between two drivers.
    Includes lap-by-lap delta, compound progression, pit stop deltas, and strategy scores.
    """
    # 1. Strategy scores
    score1_data = calculate_strategy_effectiveness_score(driver1, laps1, stints1, pits1, events, total_laps)
    score2_data = calculate_strategy_effectiveness_score(driver2, laps2, stints2, pits2, events, total_laps)

    sorted_laps1 = sorted(laps1, key=lambda x: x.lap_number)
    sorted_laps2 = sorted(laps2, key=lambda x: x.lap_number)

    d1_map = {l.lap_number: l for l in sorted_laps1}
    d2_map = {l.lap_number: l for l in sorted_laps2}

    # Stint compound lookup per lap
    def get_compound_for_lap(stints: List[Stint], lap_num: int) -> str:
        for s in stints:
            if s.start_lap <= lap_num <= s.end_lap:
                return s.compound.upper()
        return "UNKNOWN"

    all_lap_nums = sorted(list(set(d1_map.keys()).union(set(d2_map.keys()))))
    lap_deltas = []
    running_gap = 0.0

    valid_times1 = []
    valid_times2 = []

    for lp in all_lap_nums:
        l1 = d1_map.get(lp)
        l2 = d2_map.get(lp)

        t1 = l1.lap_time if (l1 and l1.lap_time and l1.is_valid) else None
        t2 = l2.lap_time if (l2 and l2.lap_time and l2.is_valid) else None

        if t1:
            valid_times1.append(t1)
        if t2:
            valid_times2.append(t2)

        delta = round(t1 - t2, 3) if (t1 and t2) else None
        if delta is not None:
            running_gap += delta

        lap_deltas.append({
            "lap": lp,
            "driver1_lap_time": round(t1, 3) if t1 else None,
            "driver2_lap_time": round(t2, 3) if t2 else None,
            "delta_seconds": delta,
            "cumulative_gap": round(running_gap, 3) if delta is not None else None,
            "driver1_compound": get_compound_for_lap(stints1, lp),
            "driver2_compound": get_compound_for_lap(stints2, lp),
        })

    avg_pace1 = sum(valid_times1) / len(valid_times1) if valid_times1 else 0.0
    avg_pace2 = sum(valid_times2) / len(valid_times2) if valid_times2 else 0.0

    faster_driver = driver1.driver_code if (avg_pace1 and avg_pace2 and avg_pace1 < avg_pace2) else driver2.driver_code

    # Strategic differences
    diffs = []
    if len(stints1) != len(stints2):
        diffs.append(
            f"{driver1.driver_code} executed a {len(stints1)}-stop strategy vs {driver2.driver_code}'s {len(stints2)}-stop strategy."
        )
    comp1_str = " -> ".join([s.compound.upper() for s in sorted(stints1, key=lambda x: x.stint_number)])
    comp2_str = " -> ".join([s.compound.upper() for s in sorted(stints2, key=lambda x: x.stint_number)])
    diffs.append(f"Tyre plan: {driver1.driver_code} [{comp1_str}] vs {driver2.driver_code} [{comp2_str}].")

    if score1_data["total_score"] > score2_data["total_score"]:
        diffs.append(f"{driver1.driver_code} achieved a higher strategy effectiveness score (+{round(score1_data['total_score'] - score2_data['total_score'], 1)} pts).")
    else:
        diffs.append(f"{driver2.driver_code} achieved a higher strategy effectiveness score (+{round(score2_data['total_score'] - score1_data['total_score'], 1)} pts).")

    return {
        "driver1": {
            "driver_id": driver1.id,
            "driver_code": driver1.driver_code,
            "driver_name": driver1.full_name,
            "team": driver1.team,
            "start_position": sorted_laps1[0].position if sorted_laps1 else None,
            "finish_position": sorted_laps1[-1].position if sorted_laps1 else None,
            "positions_gained": (sorted_laps1[0].position - sorted_laps1[-1].position) if (sorted_laps1 and sorted_laps1[0].position and sorted_laps1[-1].position) else 0,
            "score": score1_data,
            "summary": score1_data["summary"],
        },
        "driver2": {
            "driver_id": driver2.id,
            "driver_code": driver2.driver_code,
            "driver_name": driver2.full_name,
            "team": driver2.team,
            "start_position": sorted_laps2[0].position if sorted_laps2 else None,
            "finish_position": sorted_laps2[-1].position if sorted_laps2 else None,
            "positions_gained": (sorted_laps2[0].position - sorted_laps2[-1].position) if (sorted_laps2 and sorted_laps2[0].position and sorted_laps2[-1].position) else 0,
            "score": score2_data,
            "summary": score2_data["summary"],
        },
        "driver1_stints": format_stints_response(stints1),
        "driver2_stints": format_stints_response(stints2),
        "driver1_pit_stops": [
            {"id": p.id, "race_id": p.race_id, "driver_id": p.driver_id, "driver_code": driver1.driver_code, "lap": p.lap, "duration": p.duration, "stop_number": p.stop_number}
            for p in pits1
        ],
        "driver2_pit_stops": [
            {"id": p.id, "race_id": p.race_id, "driver_id": p.driver_id, "driver_code": driver2.driver_code, "lap": p.lap, "duration": p.duration, "stop_number": p.stop_number}
            for p in pits2
        ],
        "lap_deltas": lap_deltas,
        "faster_driver_code": faster_driver,
        "key_strategic_differences": diffs,
    }
