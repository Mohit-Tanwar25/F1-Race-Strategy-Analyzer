from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.race import Race
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.models.race_event import RaceEvent
from app.schemas.f1_schemas import (
    DegradationAnalysisResponse,
    DriverDegradation,
    UndercutDetail,
    OvercutDetail,
    DriverScore,
)
from app.analysis.degradation import calculate_stint_degradation, get_sc_vsc_lap_set
from app.analysis.undercut_overcut import analyze_undercuts_and_overcuts
from app.analysis.strategy_score import calculate_strategy_effectiveness_score

router = APIRouter(prefix="/races", tags=["Analysis"])


@router.get("/{race_id}/analysis/degradation", response_model=DegradationAnalysisResponse)
def get_degradation_analysis(
    race_id: int,
    driver_id: Optional[int] = Query(None, description="Optional driver filter"),
    db: Session = Depends(get_db)
):
    """
    Calculate Estimated Tyre Degradation for all stints in the race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    events = db.query(RaceEvent).filter(RaceEvent.race_id == race_id).all()
    sc_vsc_laps = get_sc_vsc_lap_set(events)

    drivers_query = db.query(Driver).join(Lap, Lap.driver_id == Driver.id).filter(Lap.race_id == race_id).distinct()
    if driver_id:
        drivers_query = drivers_query.filter(Driver.id == driver_id)
    drivers = drivers_query.all()

    laps_all = db.query(Lap).filter(Lap.race_id == race_id).all()
    stints_all = db.query(Stint).filter(Stint.race_id == race_id).all()

    laps_by_driver = {}
    for l in laps_all:
        laps_by_driver.setdefault(l.driver_id, []).append(l)

    stints_by_driver = {}
    for s in stints_all:
        stints_by_driver.setdefault(s.driver_id, []).append(s)

    driver_degs = []
    for d in drivers:
        d_laps = laps_by_driver.get(d.id, [])
        d_stints = sorted(stints_by_driver.get(d.id, []), key=lambda x: x.stint_number)

        stint_results = []
        valid_paces = []

        for st in d_stints:
            deg_res = calculate_stint_degradation(st, d_laps, sc_vsc_laps)
            stint_results.append(deg_res)
            if deg_res["avg_lap_time"] > 0:
                valid_paces.append(deg_res["avg_lap_time"])

        overall_avg = sum(valid_paces) / len(valid_paces) if valid_paces else 0.0

        driver_degs.append(
            DriverDegradation(
                driver_id=d.id,
                driver_code=d.driver_code,
                driver_name=d.full_name,
                team=d.team,
                overall_avg_pace=round(overall_avg, 3),
                stints=stint_results,
            )
        )

    return DegradationAnalysisResponse(
        race_id=race.id,
        race_name=race.name,
        drivers=driver_degs,
    )


@router.get("/{race_id}/analysis/undercuts", response_model=List[UndercutDetail])
def get_undercut_analysis(race_id: int, db: Session = Depends(get_db)):
    """
    Detect and calculate all strategic Undercut attempts in the race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    drivers = db.query(Driver).join(Lap, Lap.driver_id == Driver.id).filter(Lap.race_id == race_id).distinct().all()
    laps_all = db.query(Lap).filter(Lap.race_id == race_id).all()
    pits_all = db.query(PitStop).filter(PitStop.race_id == race_id).all()
    events = db.query(RaceEvent).filter(RaceEvent.race_id == race_id).all()

    laps_by_driver = {}
    for l in laps_all:
        laps_by_driver.setdefault(l.driver_id, []).append(l)

    pits_by_driver = {}
    for p in pits_all:
        pits_by_driver.setdefault(p.driver_id, []).append(p)

    res = analyze_undercuts_and_overcuts(drivers, laps_by_driver, pits_by_driver, events)
    return res["undercuts"]


@router.get("/{race_id}/analysis/overcuts", response_model=List[OvercutDetail])
def get_overcut_analysis(race_id: int, db: Session = Depends(get_db)):
    """
    Detect and calculate all strategic Overcut attempts in the race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    drivers = db.query(Driver).join(Lap, Lap.driver_id == Driver.id).filter(Lap.race_id == race_id).distinct().all()
    laps_all = db.query(Lap).filter(Lap.race_id == race_id).all()
    pits_all = db.query(PitStop).filter(PitStop.race_id == race_id).all()
    events = db.query(RaceEvent).filter(RaceEvent.race_id == race_id).all()

    laps_by_driver = {}
    for l in laps_all:
        laps_by_driver.setdefault(l.driver_id, []).append(l)

    pits_by_driver = {}
    for p in pits_all:
        pits_by_driver.setdefault(p.driver_id, []).append(p)

    res = analyze_undercuts_and_overcuts(drivers, laps_by_driver, pits_by_driver, events)
    return res["overcuts"]


@router.get("/{race_id}/analysis/scores", response_model=List[DriverScore])
def get_strategy_scores(race_id: int, db: Session = Depends(get_db)):
    """
    Get Strategy Effectiveness Scores for all drivers.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    drivers = db.query(Driver).join(Lap, Lap.driver_id == Driver.id).filter(Lap.race_id == race_id).distinct().all()
    laps_all = db.query(Lap).filter(Lap.race_id == race_id).all()
    stints_all = db.query(Stint).filter(Stint.race_id == race_id).all()
    pits_all = db.query(PitStop).filter(PitStop.race_id == race_id).all()
    events = db.query(RaceEvent).filter(RaceEvent.race_id == race_id).all()

    laps_by_driver = {}
    for l in laps_all:
        laps_by_driver.setdefault(l.driver_id, []).append(l)

    stints_by_driver = {}
    for s in stints_all:
        stints_by_driver.setdefault(s.driver_id, []).append(s)

    pits_by_driver = {}
    for p in pits_all:
        pits_by_driver.setdefault(p.driver_id, []).append(p)

    scores = []
    for d in drivers:
        d_laps = sorted(laps_by_driver.get(d.id, []), key=lambda x: x.lap_number)
        d_stints = stints_by_driver.get(d.id, [])
        d_pits = pits_by_driver.get(d.id, [])

        start_p = d_laps[0].position if d_laps else None
        fin_p = d_laps[-1].position if d_laps else None
        gained = (start_p - fin_p) if (start_p and fin_p) else 0

        score_res = calculate_strategy_effectiveness_score(
            d, d_laps, d_stints, d_pits, events, race.total_laps or 50
        )

        scores.append(
            DriverScore(
                driver_id=d.id,
                driver_code=d.driver_code,
                driver_name=d.full_name,
                team=d.team,
                start_position=start_p,
                finish_position=fin_p,
                positions_gained=gained,
                score=score_res,
                summary=score_res["summary"],
            )
        )

    return sorted(scores, key=lambda x: x.score.total_score, reverse=True)
