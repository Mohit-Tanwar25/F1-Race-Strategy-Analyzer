import pytest
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.analysis.strategy_score import calculate_strategy_effectiveness_score


def test_strategy_effectiveness_score():
    driver = Driver(id=1, driver_code="VER", full_name="Max Verstappen", team="Red Bull")

    laps = [
        Lap(id=i, race_id=1, driver_id=1, lap_number=i, lap_time=90.0 + (i % 2)*0.2, position=1, is_valid=True, pit_stop=(i==20))
        for i in range(1, 51)
    ]
    stints = [
        Stint(id=1, race_id=1, driver_id=1, stint_number=1, start_lap=1, end_lap=20, compound="MEDIUM"),
        Stint(id=2, race_id=1, driver_id=1, stint_number=2, start_lap=21, end_lap=50, compound="HARD"),
    ]
    pits = [
        PitStop(id=1, race_id=1, driver_id=1, lap=20, duration=22.0, stop_number=1),
    ]

    score = calculate_strategy_effectiveness_score(driver, laps, stints, pits, events=[], race_total_laps=50)

    assert 0 <= score["pace_efficiency"] <= 35
    assert 0 <= score["position_gain"] <= 30
    assert 0 <= score["tyre_efficiency"] <= 20
    assert 0 <= score["pit_stop_efficiency"] <= 15
    assert 0 <= score["total_score"] <= 100
    assert score["rating"] in ["Exceptional", "Highly Effective", "Solid", "Suboptimal"]
