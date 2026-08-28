from typing import List, Dict, Any, Optional
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.models.lap import Lap


def detect_stints_from_laps_and_pits(
    laps: List[Lap],
    pit_stops: List[PitStop],
    default_compound: str = "MEDIUM"
) -> List[Dict[str, Any]]:
    """
    Detect stints given a sorted sequence of laps and pit stops for a driver.
    """
    if not laps:
        return []

    sorted_laps = sorted(laps, key=lambda x: x.lap_number)
    sorted_pits = sorted(pit_stops, key=lambda x: x.lap)
    pit_laps = {p.lap for p in sorted_pits}

    stints = []
    stint_num = 1
    current_start = sorted_laps[0].lap_number

    for i, lap in enumerate(sorted_laps):
        # A pit stop ends the current stint on that lap
        is_last_lap = (i == len(sorted_laps) - 1)
        if lap.lap_number in pit_laps or lap.pit_stop or is_last_lap:
            end_lap = lap.lap_number
            stints.append({
                "stint_number": stint_num,
                "start_lap": current_start,
                "end_lap": end_lap,
                "stint_length": end_lap - current_start + 1,
                "compound": default_compound,
                "tyre_age_start": 0,
                "tyre_age_end": end_lap - current_start + 1,
            })
            stint_num += 1
            current_start = end_lap + 1

    return stints


def format_stints_response(stints: List[Stint]) -> List[Dict[str, Any]]:
    """
    Format Stint ORM objects into standardized dictionary structure.
    """
    res = []
    for s in sorted(stints, key=lambda x: x.stint_number):
        res.append({
            "id": s.id,
            "driver_id": s.driver_id,
            "stint_number": s.stint_number,
            "start_lap": s.start_lap,
            "end_lap": s.end_lap,
            "stint_length": s.end_lap - s.start_lap + 1,
            "compound": s.compound.upper(),
            "tyre_age_start": s.tyre_age_start,
            "tyre_age_end": s.tyre_age_end,
        })
    return res
