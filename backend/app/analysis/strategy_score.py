from typing import List, Dict, Any, Optional
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.models.race_event import RaceEvent


def calculate_strategy_effectiveness_score(
    driver: Driver,
    laps: List[Lap],
    stints: List[Stint],
    pit_stops: List[PitStop],
    events: List[RaceEvent],
    race_total_laps: int = 50,
) -> Dict[str, Any]:
    """
    Calculate the proprietary Strategy Effectiveness Score (0 - 100).
    Components:
      - Pace Efficiency (0 - 35 pts): Consistency, outlier minimization, delta to median pace.
      - Position Gain (0 - 30 pts): Positions gained from grid start to finish, bonus for holding podium.
      - Tyre Efficiency (0 - 20 pts): Compound lifecycle management, stint longevity vs degradation.
      - Pit-Stop Efficiency (0 - 15 pts): Timing stops during SC/VSC windows (cheap pit delta) or optimal windows.
    """
    if not laps:
        return {
            "pace_efficiency": 0.0,
            "position_gain": 0.0,
            "tyre_efficiency": 0.0,
            "pit_stop_efficiency": 0.0,
            "total_score": 0.0,
            "rating": "Inconclusive",
            "summary": "Insufficient lap data for strategy scoring.",
        }

    sorted_laps = sorted(laps, key=lambda x: x.lap_number)
    start_pos = sorted_laps[0].position or 10
    finish_pos = sorted_laps[-1].position or start_pos
    pos_delta = start_pos - finish_pos  # positive means moved forward

    # 1. Pace Efficiency (35 pts max)
    valid_lap_times = [l.lap_time for l in sorted_laps if l.lap_time and l.is_valid and not l.pit_stop]
    if valid_lap_times:
        std_dev = float(np_std := (sum((x - sum(valid_lap_times)/len(valid_lap_times))**2 for x in valid_lap_times)/len(valid_lap_times))**0.5)
        # Standard deviation of pace: lower is better (< 0.8s is exceptional)
        pace_score = max(10.0, min(35.0, 35.0 - (std_dev * 5.0)))
    else:
        pace_score = 20.0

    # 2. Position Gain (30 pts max)
    # Gaining positions adds points; finishing P1-P3 guarantees high floor
    pos_score = 15.0 + (pos_delta * 2.5)
    if finish_pos == 1:
        pos_score = max(pos_score, 28.0)
    elif finish_pos <= 3:
        pos_score = max(pos_score, 25.0)
    pos_score = max(5.0, min(30.0, pos_score))

    # 3. Tyre Efficiency (20 pts max)
    # Having optimal stint distribution without premature wear
    if stints:
        stint_lengths = [s.end_lap - s.start_lap + 1 for s in stints]
        avg_stint_len = sum(stint_lengths) / len(stint_lengths)
        # If stint lengths are well balanced
        tyre_score = min(20.0, 10.0 + (avg_stint_len / (race_total_laps or 50)) * 15.0)
    else:
        tyre_score = 14.0
    tyre_score = max(5.0, min(20.0, tyre_score))

    # 4. Pit Stop Efficiency (15 pts max)
    # Check if pit stops occurred during SC or VSC
    sc_vsc_laps = set()
    for e in events:
        if e.event_type in ("SAFETY_CAR", "VSC"):
            s = e.start_lap or e.lap
            end = e.end_lap or e.lap
            for l in range(s, end + 1):
                sc_vsc_laps.add(l)

    pit_score = 10.0
    if pit_stops:
        sc_pit_count = sum(1 for p in pit_stops if p.lap in sc_vsc_laps)
        if sc_pit_count > 0:
            pit_score += min(5.0, sc_pit_count * 3.0)  # Free pit stop bonus under SC
        avg_duration = sum(p.duration for p in pit_stops if p.duration) / len(pit_stops) if any(p.duration for p in pit_stops) else 22.0
        if avg_duration < 23.0:
            pit_score += 1.5
    pit_score = max(4.0, min(15.0, pit_score))

    total = round(pace_score + pos_score + tyre_score + pit_score, 1)

    if total >= 85:
        rating = "Exceptional"
    elif total >= 72:
        rating = "Highly Effective"
    elif total >= 58:
        rating = "Solid"
    else:
        rating = "Suboptimal"

    summary = (
        f"{driver.driver_code} achieved a Strategy Score of {total}/100 ({rating}). "
        f"Started P{start_pos}, finished P{finish_pos} ({'+' if pos_delta > 0 else ''}{pos_delta} positions). "
        f"Completed {len(stints)} stint(s) with {len(pit_stops)} pit stop(s)."
    )

    return {
        "pace_efficiency": round(pace_score, 1),
        "position_gain": round(pos_score, 1),
        "tyre_efficiency": round(tyre_score, 1),
        "pit_stop_efficiency": round(pit_score, 1),
        "total_score": min(total, 100.0),
        "rating": rating,
        "summary": summary,
    }
