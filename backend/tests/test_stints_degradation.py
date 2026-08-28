import pytest
from app.models.stint import Stint
from app.models.lap import Lap
from app.analysis.degradation import calculate_stint_degradation
from app.analysis.stints import detect_stints_from_laps_and_pits
from app.models.pit_stop import PitStop


def test_detect_stints_from_laps_and_pits():
    laps = [
        Lap(lap_number=i, pit_stop=(i == 15), is_valid=True)
        for i in range(1, 30)
    ]
    pits = [PitStop(lap=15, stop_number=1)]

    stints = detect_stints_from_laps_and_pits(laps, pits)
    assert len(stints) == 2
    assert stints[0]["start_lap"] == 1
    assert stints[0]["end_lap"] == 15
    assert stints[1]["start_lap"] == 16
    assert stints[1]["end_lap"] == 29


def test_calculate_stint_degradation():
    stint = Stint(
        id=1,
        race_id=1,
        driver_id=1,
        stint_number=1,
        start_lap=1,
        end_lap=15,
        compound="SOFT",
        tyre_age_start=0,
        tyre_age_end=15,
    )

    # 15 laps with linear degradation of +0.08s per lap
    laps = [
        Lap(
            id=i,
            race_id=1,
            driver_id=1,
            lap_number=i,
            lap_time=90.0 + (i * 0.08),
            pit_stop=(i == 15),
            is_valid=True,
        )
        for i in range(1, 16)
    ]

    sc_laps = set()
    result = calculate_stint_degradation(stint, laps, sc_laps)

    assert result["compound"] == "SOFT"
    assert result["degradation_rate_per_lap"] > 0.05
    assert result["best_lap_time"] > 0
    assert result["confidence"] > 0.5
