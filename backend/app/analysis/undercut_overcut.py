from typing import List, Dict, Any, Optional
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.pit_stop import PitStop
from app.models.race_event import RaceEvent


def analyze_undercuts_and_overcuts(
    drivers: List[Driver],
    laps_by_driver: Dict[int, List[Lap]],
    pit_stops_by_driver: Dict[int, List[PitStop]],
    events: List[RaceEvent],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Dedicated strategy analysis engine detecting Undercuts and Overcuts.
    Considers pit lap deltas, in-lap/out-lap pace differences, and post-cycle track positions.
    """
    undercuts = []
    overcuts = []

    # Map drivers by id
    driver_map = {d.id: d for d in drivers}

    # Map laps for fast position and time lookup: (driver_id, lap_num) -> Lap
    lap_dict = {}
    for d_id, d_laps in laps_by_driver.items():
        for l in d_laps:
            lap_dict[(d_id, l.lap_number)] = l

    driver_ids = list(driver_map.keys())

    # Compare pairs of drivers who had pit stops
    for i in range(len(driver_ids)):
        d1_id = driver_ids[i]
        d1 = driver_map[d1_id]
        d1_pits = sorted(pit_stops_by_driver.get(d1_id, []), key=lambda p: p.lap)

        for j in range(len(driver_ids)):
            if i == j:
                continue
            d2_id = driver_ids[j]
            d2 = driver_map[d2_id]
            d2_pits = sorted(pit_stops_by_driver.get(d2_id, []), key=lambda p: p.lap)

            # Compare each pit stop pair between d1 and d2
            for p1 in d1_pits:
                for p2 in d2_pits:
                    # Same pit cycle window (pit stops within 1 to 4 laps of each other)
                    lap_diff = p2.lap - p1.lap

                    # --- CASE 1: POTENTIAL UNDERCUT (d1 pits earlier than d2: 1 <= lap_diff <= 4) ---
                    if 1 <= lap_diff <= 4:
                        # Pre-pit state check on lap p1.lap - 1
                        pre_lap_num = max(1, p1.lap - 1)
                        l1_pre = lap_dict.get((d1_id, pre_lap_num))
                        l2_pre = lap_dict.get((d2_id, pre_lap_num))

                        # Post-cycle state check on lap p2.lap + 1
                        post_lap_num = p2.lap + 1
                        l1_post = lap_dict.get((d1_id, post_lap_num))
                        l2_post = lap_dict.get((d2_id, post_lap_num))

                        if l1_pre and l2_pre and l1_post and l2_post:
                            pos1_pre = l1_pre.position or 99
                            pos2_pre = l2_pre.position or 99
                            pos1_post = l1_post.position or 99
                            pos2_post = l2_post.position or 99

                            # d2 was ahead or immediately defending before d1 pitted (pos2_pre <= pos1_pre)
                            # and d1 and d2 were in close proximity (position difference <= 3)
                            if abs(pos1_pre - pos2_pre) <= 3 and pos2_pre <= pos1_pre:
                                # Calculate out-lap fresh tyre pace benefit of d1 during the offset laps
                                d1_inter_laps = [
                                    lap_dict.get((d1_id, lp))
                                    for lp in range(p1.lap + 1, p2.lap + 1)
                                    if lap_dict.get((d1_id, lp)) and lap_dict.get((d1_id, lp)).lap_time
                                ]
                                d2_inter_laps = [
                                    lap_dict.get((d2_id, lp))
                                    for lp in range(p1.lap + 1, p2.lap + 1)
                                    if lap_dict.get((d2_id, lp)) and lap_dict.get((d2_id, lp)).lap_time
                                ]

                                d1_pace = sum(l.lap_time for l in d1_inter_laps) / len(d1_inter_laps) if d1_inter_laps else 0
                                d2_pace = sum(l.lap_time for l in d2_inter_laps) / len(d2_inter_laps) if d2_inter_laps else 0
                                pace_delta = max(0.0, d2_pace - d1_pace) if (d1_pace and d2_pace) else 1.5

                                # Track position gain achieved?
                                success = (pos1_post < pos2_post)
                                estimated_gain = round(pace_delta * lap_diff + (1.2 if success else 0.4), 2)
                                confidence = 0.85 if success else 0.65

                                undercuts.append({
                                    "type": "UNDERCUT",
                                    "attacker_id": d1.id,
                                    "attacker_code": d1.driver_code,
                                    "attacker_name": d1.full_name,
                                    "attacker_team": d1.team,
                                    "target_id": d2.id,
                                    "target_code": d2.driver_code,
                                    "target_name": d2.full_name,
                                    "target_team": d2.team,
                                    "pit_lap": p1.lap,
                                    "target_pit_lap": p2.lap,
                                    "estimated_gain_seconds": estimated_gain,
                                    "confidence": confidence,
                                    "success": success,
                                    "explanation": (
                                        f"{d1.driver_code} pitted on Lap {p1.lap} onto fresh tyres while {d2.driver_code} stayed out until Lap {p2.lap}. "
                                        + (f"{d1.driver_code} successfully jumped {d2.driver_code} for track position (P{pos1_post} vs P{pos2_post})."
                                           if success else f"{d1.driver_code} closed down the margin by ~{estimated_gain}s but {d2.driver_code} retained position.")
                                    ),
                                })

                    # --- CASE 2: POTENTIAL OVERCUT (d1 pits later than d2: 1 <= -lap_diff <= 4) ---
                    elif -4 <= lap_diff <= -1:
                        # d2 pitted first (p2.lap), d1 stayed out and pitted on p1.lap
                        stay_out_laps = p1.lap - p2.lap
                        pre_lap_num = max(1, p2.lap - 1)
                        l1_pre = lap_dict.get((d1_id, pre_lap_num))
                        l2_pre = lap_dict.get((d2_id, pre_lap_num))

                        post_lap_num = p1.lap + 1
                        l1_post = lap_dict.get((d1_id, post_lap_num))
                        l2_post = lap_dict.get((d2_id, post_lap_num))

                        if l1_pre and l2_pre and l1_post and l2_post:
                            pos1_pre = l1_pre.position or 99
                            pos2_pre = l2_pre.position or 99
                            pos1_post = l1_post.position or 99
                            pos2_post = l2_post.position or 99

                            # d1 was in close competition with d2
                            if abs(pos1_pre - pos2_pre) <= 3:
                                success = (pos1_post < pos2_post and pos1_pre >= pos2_pre)
                                if success:
                                    overcuts.append({
                                        "type": "OVERCUT",
                                        "attacker_id": d1.id,
                                        "attacker_code": d1.driver_code,
                                        "attacker_name": d1.full_name,
                                        "attacker_team": d1.team,
                                        "target_id": d2.id,
                                        "target_code": d2.driver_code,
                                        "target_name": d2.full_name,
                                        "target_team": d2.team,
                                        "pit_lap": p1.lap,
                                        "target_pit_lap": p2.lap,
                                        "estimated_gain_seconds": round(1.8 * stay_out_laps, 2),
                                        "confidence": 0.80,
                                        "success": True,
                                        "explanation": (
                                            f"{d1.driver_code} extended stint until Lap {p1.lap} in clean air after {d2.driver_code} pitted on Lap {p2.lap}, successfully executing an overcut into P{pos1_post}."
                                        ),
                                    })

    return {
        "undercuts": undercuts,
        "overcuts": overcuts,
    }
