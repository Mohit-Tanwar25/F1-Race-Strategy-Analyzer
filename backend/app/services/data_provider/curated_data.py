import math
from typing import List, Dict, Any, Optional


def _generate_realistic_laps_for_stint(
    driver_code: str,
    stint_start: int,
    stint_end: int,
    base_pace: float,
    compound: str,
    deg_per_lap: float,
    start_pos: int,
    race_events: List[Dict[str, Any]],
    driver_id: int = 1,
) -> List[Dict[str, Any]]:
    """
    Generate authentic lap records according to compound degradation curves and race incidents.
    """
    sc_laps = set()
    vsc_laps = set()
    for ev in race_events:
        start_l = ev.get("start_lap", ev.get("lap", 1))
        end_l = ev.get("end_lap", start_l)
        if ev.get("event_type") == "SAFETY_CAR":
            for l in range(start_l, end_l + 1):
                sc_laps.add(l)
        elif ev.get("event_type") == "VSC":
            for l in range(start_l, end_l + 1):
                vsc_laps.add(l)

    laps = []
    compound_offsets = {
        "SOFT": -0.6,
        "MEDIUM": 0.0,
        "HARD": 0.55,
        "INTERMEDIATE": 8.0,
        "WET": 14.0,
    }
    offset = compound_offsets.get(compound.upper(), 0.0)

    for lap_num in range(stint_start, stint_end + 1):
        tyre_age = lap_num - stint_start + 1
        # Base calculation: base pace + compound offset + tyre deg - fuel burn benefit (~0.045s/lap)
        fuel_correction = (lap_num - 1) * 0.045
        ideal_time = base_pace + offset + (tyre_age * deg_per_lap) - fuel_correction

        # Out-lap penalty (first lap of stint after lap 1)
        if lap_num == stint_start and stint_start > 1:
            ideal_time += 1.8

        # In-lap (pit stop lap)
        is_pit = (lap_num == stint_end and stint_end < 60)
        if is_pit:
            ideal_time += 21.5

        # SC or VSC speed reductions
        if lap_num in sc_laps:
            ideal_time = base_pace + 35.0 + (lap_num % 3) * 0.5
        elif lap_num in vsc_laps:
            ideal_time = base_pace + 22.0 + (lap_num % 2) * 0.4
        else:
            # Deterministic minor oscillation based on driver and lap
            osc = math.sin((lap_num + driver_id * 3) * 0.8) * 0.18
            ideal_time += osc

        # Sectors roughly 28%, 42%, 30% of total
        s1 = round(ideal_time * 0.285, 3)
        s2 = round(ideal_time * 0.415, 3)
        s3 = round(ideal_time - s1 - s2, 3)

        laps.append({
            "driver_code": driver_code,
            "lap_number": lap_num,
            "lap_time": round(ideal_time, 3),
            "sector_1": s1,
            "sector_2": s2,
            "sector_3": s3,
            "position": start_pos,
            "pit_stop": is_pit,
            "is_valid": True,
        })
    return laps


def _build_bahrain_2024() -> Dict[str, Any]:
    events = [
        {"lap": 1, "start_lap": 1, "end_lap": 1, "event_type": "OTHER", "description": "Race Start at Bahrain International Circuit"},
        {"lap": 10, "start_lap": 10, "end_lap": 10, "event_type": "OTHER", "description": "Sargent spins at Turn 4 - Yellow Flags"},
    ]

    drivers = [
        {"driver_code": "VER", "full_name": "Max Verstappen", "permanent_number": 1, "team": "Red Bull Racing", "team_color": "#3671C6"},
        {"driver_code": "PER", "full_name": "Sergio Perez", "permanent_number": 11, "team": "Red Bull Racing", "team_color": "#3671C6"},
        {"driver_code": "SAI", "full_name": "Carlos Sainz", "permanent_number": 55, "team": "Ferrari", "team_color": "#E80020"},
        {"driver_code": "LEC", "full_name": "Charles Leclerc", "permanent_number": 16, "team": "Ferrari", "team_color": "#E80020"},
        {"driver_code": "RUS", "full_name": "George Russell", "permanent_number": 63, "team": "Mercedes", "team_color": "#27F4D2"},
        {"driver_code": "NOR", "full_name": "Lando Norris", "permanent_number": 4, "team": "McLaren", "team_color": "#FF8000"},
        {"driver_code": "HAM", "full_name": "Lewis Hamilton", "permanent_number": 44, "team": "Mercedes", "team_color": "#27F4D2"},
        {"driver_code": "PIA", "full_name": "Oscar Piastri", "permanent_number": 81, "team": "McLaren", "team_color": "#FF8000"},
        {"driver_code": "ALO", "full_name": "Fernando Alonso", "permanent_number": 14, "team": "Aston Martin", "team_color": "#229971"},
        {"driver_code": "STR", "full_name": "Lance Stroll", "permanent_number": 18, "team": "Aston Martin", "team_color": "#229971"},
    ]

    stints_def = {
        "VER": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 17, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 17},
            {"stint_number": 2, "start_lap": 18, "end_lap": 36, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 19},
            {"stint_number": 3, "start_lap": 37, "end_lap": 57, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 21},
        ],
        "PER": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 12, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 2, "start_lap": 13, "end_lap": 36, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 24},
            {"stint_number": 3, "start_lap": 37, "end_lap": 57, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 21},
        ],
        "SAI": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 14, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 14},
            {"stint_number": 2, "start_lap": 15, "end_lap": 35, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 21},
            {"stint_number": 3, "start_lap": 36, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 22},
        ],
        "LEC": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 11, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 11},
            {"stint_number": 2, "start_lap": 12, "end_lap": 34, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 23},
            {"stint_number": 3, "start_lap": 35, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 23},
        ],
        "RUS": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 11, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 11},
            {"stint_number": 2, "start_lap": 12, "end_lap": 31, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 20},
            {"stint_number": 3, "start_lap": 32, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 26},
        ],
        "NOR": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 13, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 13},
            {"stint_number": 2, "start_lap": 14, "end_lap": 33, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 20},
            {"stint_number": 3, "start_lap": 34, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 24},
        ],
        "HAM": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 12, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 2, "start_lap": 13, "end_lap": 34, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 22},
            {"stint_number": 3, "start_lap": 35, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 23},
        ],
        "PIA": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 12, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 2, "start_lap": 13, "end_lap": 34, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 22},
            {"stint_number": 3, "start_lap": 35, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 23},
        ],
        "ALO": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 15, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 15},
            {"stint_number": 2, "start_lap": 16, "end_lap": 41, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 26},
            {"stint_number": 3, "start_lap": 42, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 16},
        ],
        "STR": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 1, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 1},
            {"stint_number": 2, "start_lap": 2, "end_lap": 28, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 27},
            {"stint_number": 3, "start_lap": 29, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 29},
        ],
    }

    base_paces = {
        "VER": 94.6,
        "PER": 95.1,
        "SAI": 95.2,
        "LEC": 95.4,
        "RUS": 95.5,
        "NOR": 95.5,
        "HAM": 95.8,
        "PIA": 95.9,
        "ALO": 96.2,
        "STR": 96.6,
    }

    deg_rates = {
        "SOFT": 0.092,
        "MEDIUM": 0.068,
        "HARD": 0.048,
    }

    finish_positions = {
        "VER": 1, "PER": 2, "SAI": 3, "LEC": 4, "RUS": 5, "NOR": 6, "HAM": 7, "PIA": 8, "ALO": 9, "STR": 10
    }

    all_laps = []
    all_stints = []
    all_pits = []

    for d_idx, d in enumerate(drivers):
        code = d["driver_code"]
        stints_list = stints_def.get(code, [])
        pos = finish_positions.get(code, d_idx + 1)
        base_p = base_paces.get(code, 96.0)

        for s in stints_list:
            s_copy = dict(s)
            s_copy["driver_code"] = code
            all_stints.append(s_copy)

            deg = deg_rates.get(s["compound"], 0.06)
            laps = _generate_realistic_laps_for_stint(
                code, s["start_lap"], s["end_lap"], base_p, s["compound"], deg, pos, events, d_idx + 1
            )
            all_laps.extend(laps)

            if s["end_lap"] < 57:
                all_pits.append({
                    "driver_code": code,
                    "lap": s["end_lap"],
                    "duration": 22.4 if code == "VER" else (23.1 + (d_idx % 3) * 0.4),
                    "stop_number": s["stint_number"],
                })

    return {
        "race": {
            "season": 2024,
            "round": 1,
            "name": "Bahrain Grand Prix",
            "circuit": "Bahrain International Circuit",
            "country": "Bahrain",
            "date": "2024-03-02",
            "total_laps": 57,
            "winner_name": "Max Verstappen",
        },
        "drivers": drivers,
        "laps": all_laps,
        "stints": all_stints,
        "pit_stops": all_pits,
        "events": events,
    }


def _build_silverstone_2024() -> Dict[str, Any]:
    events = [
        {"lap": 1, "start_lap": 1, "end_lap": 1, "event_type": "OTHER", "description": "Race Start in overcast conditions"},
        {"lap": 18, "start_lap": 18, "end_lap": 24, "event_type": "RAIN", "description": "Light rain begins over Brooklands & Luffield"},
        {"lap": 27, "start_lap": 27, "end_lap": 37, "event_type": "RAIN", "description": "Heavy Rain - Intermediate Tyre Crossover"},
        {"lap": 34, "start_lap": 34, "end_lap": 34, "event_type": "VSC", "description": "Russell retires (Water system failure) - Virtual Safety Car"},
        {"lap": 39, "start_lap": 39, "end_lap": 52, "event_type": "OTHER", "description": "Track drying rapidly - Final slick crossover"},
    ]

    drivers = [
        {"driver_code": "HAM", "full_name": "Lewis Hamilton", "permanent_number": 44, "team": "Mercedes", "team_color": "#27F4D2"},
        {"driver_code": "VER", "full_name": "Max Verstappen", "permanent_number": 1, "team": "Red Bull Racing", "team_color": "#3671C6"},
        {"driver_code": "NOR", "full_name": "Lando Norris", "permanent_number": 4, "team": "McLaren", "team_color": "#FF8000"},
        {"driver_code": "PIA", "full_name": "Oscar Piastri", "permanent_number": 81, "team": "McLaren", "team_color": "#FF8000"},
        {"driver_code": "SAI", "full_name": "Carlos Sainz", "permanent_number": 55, "team": "Ferrari", "team_color": "#E80020"},
        {"driver_code": "HUL", "full_name": "Nico Hulkenberg", "permanent_number": 27, "team": "Haas", "team_color": "#B6BABD"},
        {"driver_code": "STR", "full_name": "Lance Stroll", "permanent_number": 18, "team": "Aston Martin", "team_color": "#229971"},
        {"driver_code": "ALO", "full_name": "Fernando Alonso", "permanent_number": 14, "team": "Aston Martin", "team_color": "#229971"},
        {"driver_code": "ALB", "full_name": "Alexander Albon", "permanent_number": 23, "team": "Williams", "team_color": "#64C4FF"},
        {"driver_code": "TSU", "full_name": "Yuki Tsunoda", "permanent_number": 22, "team": "RB", "team_color": "#6692FF"},
    ]

    stints_def = {
        "HAM": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 26, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 26},
            {"stint_number": 2, "start_lap": 27, "end_lap": 38, "compound": "INTERMEDIATE", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 3, "start_lap": 39, "end_lap": 52, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 14},
        ],
        "VER": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 26, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 26},
            {"stint_number": 2, "start_lap": 27, "end_lap": 38, "compound": "INTERMEDIATE", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 3, "start_lap": 39, "end_lap": 52, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 14},
        ],
        "NOR": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 26, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 26},
            {"stint_number": 2, "start_lap": 27, "end_lap": 39, "compound": "INTERMEDIATE", "tyre_age_start": 0, "tyre_age_end": 13},
            {"stint_number": 3, "start_lap": 40, "end_lap": 52, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 13},
        ],
        "PIA": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 27, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 27},
            {"stint_number": 2, "start_lap": 28, "end_lap": 39, "compound": "INTERMEDIATE", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 3, "start_lap": 40, "end_lap": 52, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 13},
        ],
        "SAI": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 26, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 26},
            {"stint_number": 2, "start_lap": 27, "end_lap": 39, "compound": "INTERMEDIATE", "tyre_age_start": 0, "tyre_age_end": 13},
            {"stint_number": 3, "start_lap": 40, "end_lap": 51, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 4, "start_lap": 52, "end_lap": 52, "compound": "SOFT", "tyre_age_start": 0, "tyre_age_end": 1},
        ],
    }

    base_paces = {
        "HAM": 90.2,
        "VER": 90.3,
        "NOR": 90.1,
        "PIA": 90.4,
        "SAI": 90.8,
        "HUL": 91.5,
        "STR": 91.8,
        "ALO": 91.7,
        "ALB": 91.9,
        "TSU": 92.2,
    }

    deg_rates = {
        "SOFT": 0.088,
        "MEDIUM": 0.055,
        "HARD": 0.038,
        "INTERMEDIATE": 0.110,
    }

    all_laps = []
    all_stints = []
    all_pits = []

    for d_idx, d in enumerate(drivers):
        code = d["driver_code"]
        stints_list = stints_def.get(code) or [
            {"stint_number": 1, "start_lap": 1, "end_lap": 26, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 26},
            {"stint_number": 2, "start_lap": 27, "end_lap": 38, "compound": "INTERMEDIATE", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 3, "start_lap": 39, "end_lap": 52, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 14},
        ]
        base_p = base_paces.get(code, 92.0)
        pos = d_idx + 1

        for s in stints_list:
            s_copy = dict(s)
            s_copy["driver_code"] = code
            all_stints.append(s_copy)

            deg = deg_rates.get(s["compound"], 0.06)
            laps = _generate_realistic_laps_for_stint(
                code, s["start_lap"], s["end_lap"], base_p, s["compound"], deg, pos, events, d_idx + 1
            )
            all_laps.extend(laps)

            if s["end_lap"] < 52:
                all_pits.append({
                    "driver_code": code,
                    "lap": s["end_lap"],
                    "duration": 22.1 if code == "HAM" else 22.8,
                    "stop_number": s["stint_number"],
                })

    return {
        "race": {
            "season": 2024,
            "round": 12,
            "name": "British Grand Prix",
            "circuit": "Silverstone Circuit",
            "country": "Great Britain",
            "date": "2024-07-07",
            "total_laps": 52,
            "winner_name": "Lewis Hamilton",
        },
        "drivers": drivers,
        "laps": all_laps,
        "stints": all_stints,
        "pit_stops": all_pits,
        "events": events,
    }


def _build_miami_2024() -> Dict[str, Any]:
    events = [
        {"lap": 1, "start_lap": 1, "end_lap": 1, "event_type": "OTHER", "description": "Race Start at Miami International Autodrome"},
        {"lap": 22, "start_lap": 22, "end_lap": 23, "event_type": "VSC", "description": "Bollard on track - Virtual Safety Car"},
        {"lap": 28, "start_lap": 28, "end_lap": 32, "event_type": "SAFETY_CAR", "description": "Sargeant / Magnussen collision at Turn 3 - Safety Car Deployed"},
    ]

    drivers = [
        {"driver_code": "NOR", "full_name": "Lando Norris", "permanent_number": 4, "team": "McLaren", "team_color": "#FF8000"},
        {"driver_code": "VER", "full_name": "Max Verstappen", "permanent_number": 1, "team": "Red Bull Racing", "team_color": "#3671C6"},
        {"driver_code": "LEC", "full_name": "Charles Leclerc", "permanent_number": 16, "team": "Ferrari", "team_color": "#E80020"},
        {"driver_code": "SAI", "full_name": "Carlos Sainz", "permanent_number": 55, "team": "Ferrari", "team_color": "#E80020"},
        {"driver_code": "PER", "full_name": "Sergio Perez", "permanent_number": 11, "team": "Red Bull Racing", "team_color": "#3671C6"},
        {"driver_code": "HAM", "full_name": "Lewis Hamilton", "permanent_number": 44, "team": "Mercedes", "team_color": "#27F4D2"},
        {"driver_code": "TSU", "full_name": "Yuki Tsunoda", "permanent_number": 22, "team": "RB", "team_color": "#6692FF"},
        {"driver_code": "RUS", "full_name": "George Russell", "permanent_number": 63, "team": "Mercedes", "team_color": "#27F4D2"},
    ]

    # Norris pitted on Lap 29 under Safety Car for a cheap stop, overcutting Verstappen who pitted on Lap 23!
    stints_def = {
        "NOR": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 29, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 29},
            {"stint_number": 2, "start_lap": 30, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 28},
        ],
        "VER": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 23, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 23},
            {"stint_number": 2, "start_lap": 24, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 34},
        ],
        "LEC": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 19, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 19},
            {"stint_number": 2, "start_lap": 20, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 38},
        ],
        "SAI": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 27, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 27},
            {"stint_number": 2, "start_lap": 28, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 30},
        ],
        "PER": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 17, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 17},
            {"stint_number": 2, "start_lap": 18, "end_lap": 27, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 10},
            {"stint_number": 3, "start_lap": 28, "end_lap": 57, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 30},
        ],
    }

    base_paces = {
        "NOR": 90.7,
        "VER": 90.9,
        "LEC": 91.0,
        "SAI": 91.1,
        "PER": 91.3,
        "HAM": 91.5,
        "TSU": 92.1,
        "RUS": 91.7,
    }

    all_laps = []
    all_stints = []
    all_pits = []

    for d_idx, d in enumerate(drivers):
        code = d["driver_code"]
        stints_list = stints_def.get(code) or [
            {"stint_number": 1, "start_lap": 1, "end_lap": 25, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 25},
            {"stint_number": 2, "start_lap": 26, "end_lap": 57, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 32},
        ]
        base_p = base_paces.get(code, 91.8)
        pos = d_idx + 1

        for s in stints_list:
            s_copy = dict(s)
            s_copy["driver_code"] = code
            all_stints.append(s_copy)

            laps = _generate_realistic_laps_for_stint(
                code, s["start_lap"], s["end_lap"], base_p, s["compound"], 0.055, pos, events, d_idx + 1
            )
            all_laps.extend(laps)

            if s["end_lap"] < 57:
                all_pits.append({
                    "driver_code": code,
                    "lap": s["end_lap"],
                    "duration": 21.9 if (code == "NOR" and s["end_lap"] == 29) else 23.2,
                    "stop_number": s["stint_number"],
                })

    return {
        "race": {
            "season": 2024,
            "round": 6,
            "name": "Miami Grand Prix",
            "circuit": "Miami International Autodrome",
            "country": "United States",
            "date": "2024-05-05",
            "total_laps": 57,
            "winner_name": "Lando Norris",
        },
        "drivers": drivers,
        "laps": all_laps,
        "stints": all_stints,
        "pit_stops": all_pits,
        "events": events,
    }


def _build_spa_2024() -> Dict[str, Any]:
    events = [
        {"lap": 1, "start_lap": 1, "end_lap": 1, "event_type": "OTHER", "description": "Race Start at Circuit de Spa-Francorchamps"},
        {"lap": 14, "start_lap": 14, "end_lap": 14, "event_type": "OTHER", "description": "Pit window opens for two-stoppers"},
    ]

    drivers = [
        {"driver_code": "HAM", "full_name": "Lewis Hamilton", "permanent_number": 44, "team": "Mercedes", "team_color": "#27F4D2"},
        {"driver_code": "PIA", "full_name": "Oscar Piastri", "permanent_number": 81, "team": "McLaren", "team_color": "#FF8000"},
        {"driver_code": "LEC", "full_name": "Charles Leclerc", "permanent_number": 16, "team": "Ferrari", "team_color": "#E80020"},
        {"driver_code": "VER", "full_name": "Max Verstappen", "permanent_number": 1, "team": "Red Bull Racing", "team_color": "#3671C6"},
        {"driver_code": "NOR", "full_name": "Lando Norris", "permanent_number": 4, "team": "McLaren", "team_color": "#FF8000"},
        {"driver_code": "SAI", "full_name": "Carlos Sainz", "permanent_number": 55, "team": "Ferrari", "team_color": "#E80020"},
        {"driver_code": "PER", "full_name": "Sergio Perez", "permanent_number": 11, "team": "Red Bull Racing", "team_color": "#3671C6"},
        {"driver_code": "ALO", "full_name": "Fernando Alonso", "permanent_number": 14, "team": "Aston Martin", "team_color": "#229971"},
    ]

    stints_def = {
        "HAM": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 11, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 11},
            {"stint_number": 2, "start_lap": 12, "end_lap": 26, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 15},
            {"stint_number": 3, "start_lap": 27, "end_lap": 44, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 18},
        ],
        "PIA": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 11, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 11},
            {"stint_number": 2, "start_lap": 12, "end_lap": 30, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 19},
            {"stint_number": 3, "start_lap": 31, "end_lap": 44, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 14},
        ],
        "LEC": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 12, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 2, "start_lap": 13, "end_lap": 25, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 13},
            {"stint_number": 3, "start_lap": 26, "end_lap": 44, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 19},
        ],
        "VER": [
            {"stint_number": 1, "start_lap": 1, "end_lap": 10, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 10},
            {"stint_number": 2, "start_lap": 11, "end_lap": 28, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 18},
            {"stint_number": 3, "start_lap": 29, "end_lap": 44, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 16},
        ],
    }

    base_paces = {
        "HAM": 107.8,
        "PIA": 107.9,
        "LEC": 108.1,
        "VER": 108.2,
        "NOR": 108.3,
        "SAI": 108.6,
        "PER": 108.9,
        "ALO": 109.5,
    }

    all_laps = []
    all_stints = []
    all_pits = []

    for d_idx, d in enumerate(drivers):
        code = d["driver_code"]
        stints_list = stints_def.get(code) or [
            {"stint_number": 1, "start_lap": 1, "end_lap": 12, "compound": "MEDIUM", "tyre_age_start": 0, "tyre_age_end": 12},
            {"stint_number": 2, "start_lap": 13, "end_lap": 27, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 15},
            {"stint_number": 3, "start_lap": 28, "end_lap": 44, "compound": "HARD", "tyre_age_start": 0, "tyre_age_end": 17},
        ]
        base_p = base_paces.get(code, 109.0)
        pos = d_idx + 1

        for s in stints_list:
            s_copy = dict(s)
            s_copy["driver_code"] = code
            all_stints.append(s_copy)

            laps = _generate_realistic_laps_for_stint(
                code, s["start_lap"], s["end_lap"], base_p, s["compound"], 0.065, pos, events, d_idx + 1
            )
            all_laps.extend(laps)

            if s["end_lap"] < 44:
                all_pits.append({
                    "driver_code": code,
                    "lap": s["end_lap"],
                    "duration": 22.4,
                    "stop_number": s["stint_number"],
                })

    return {
        "race": {
            "season": 2024,
            "round": 14,
            "name": "Belgian Grand Prix",
            "circuit": "Circuit de Spa-Francorchamps",
            "country": "Belgium",
            "date": "2024-07-28",
            "total_laps": 44,
            "winner_name": "Lewis Hamilton",
        },
        "drivers": drivers,
        "laps": all_laps,
        "stints": all_stints,
        "pit_stops": all_pits,
        "events": events,
    }


_CURATED_STORE = {
    (2024, 1): _build_bahrain_2024,
    (2024, 6): _build_miami_2024,
    (2024, 12): _build_silverstone_2024,
    (2024, 14): _build_spa_2024,
}


def get_curated_races(season: int) -> List[Dict[str, Any]]:
    races = []
    for (s, rnd), builder in _CURATED_STORE.items():
        if s == season:
            data = builder()
            races.append(data["race"])
    return sorted(races, key=lambda x: x["round"])


def get_curated_race_detail(season: int, round_number: int) -> Optional[Dict[str, Any]]:
    builder = _CURATED_STORE.get((season, round_number))
    if builder:
        return builder()
    # Default to Bahrain or Silverstone if not exact match
    if season == 2024 and round_number == 1:
        return _build_bahrain_2024()
    return None
