import pytest
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.pit_stop import PitStop
from app.analysis.undercut_overcut import analyze_undercuts_and_overcuts


def test_analyze_undercuts_and_overcuts():
    d1 = Driver(id=1, driver_code="VER", full_name="Max Verstappen", team="Red Bull")
    d2 = Driver(id=2, driver_code="NOR", full_name="Lando Norris", team="McLaren")

    # VER pits lap 20 (attacker), NOR pits lap 22 (target)
    # Pre-pit (lap 19): NOR P1, VER P2
    # Post-pit (lap 23): VER P1, NOR P2 (undercut success!)
    laps_d1 = []
    laps_d2 = []

    for l in range(1, 30):
        if l < 20:
            pos1, pos2 = 2, 1
            t1, t2 = 91.0, 90.9
        elif l == 20:
            pos1, pos2 = 10, 1
            t1, t2 = 112.0, 91.0  # VER in-lap
        elif l == 21:
            pos1, pos2 = 5, 1
            t1, t2 = 90.0, 91.5   # VER flying out-lap on fresh rubber
        elif l == 22:
            pos1, pos2 = 2, 10    # NOR in-lap
            t1, t2 = 89.8, 113.0
        else:
            pos1, pos2 = 1, 2     # VER is now ahead!
            t1, t2 = 90.0, 90.1

        laps_d1.append(Lap(id=l, race_id=1, driver_id=1, lap_number=l, lap_time=t1, position=pos1, is_valid=True, pit_stop=(l==20)))
        laps_d2.append(Lap(id=100+l, race_id=1, driver_id=2, lap_number=l, lap_time=t2, position=pos2, is_valid=True, pit_stop=(l==22)))

    pits_by_driver = {
        1: [PitStop(id=1, race_id=1, driver_id=1, lap=20, duration=22.0, stop_number=1)],
        2: [PitStop(id=2, race_id=1, driver_id=2, lap=22, duration=22.5, stop_number=1)],
    }

    res = analyze_undercuts_and_overcuts(
        drivers=[d1, d2],
        laps_by_driver={1: laps_d1, 2: laps_d2},
        pit_stops_by_driver=pits_by_driver,
        events=[],
    )

    undercuts = res["undercuts"]
    assert len(undercuts) >= 1
    assert undercuts[0]["attacker_code"] == "VER"
    assert undercuts[0]["target_code"] == "NOR"
    assert undercuts[0]["success"] is True
    assert undercuts[0]["estimated_gain_seconds"] > 0
