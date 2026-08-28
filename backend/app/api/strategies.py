from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.race import Race
from app.models.driver import Driver
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.schemas.f1_schemas import DriverStrategyResponse, StintResponse, PitStopResponse

router = APIRouter(prefix="/races", tags=["Strategies"])


@router.get("/{race_id}/strategies", response_model=List[DriverStrategyResponse])
def get_race_strategies(race_id: int, db: Session = Depends(get_db)):
    """
    Get tyre stints and pit stops for all drivers in a race to construct the Strategy Timeline.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    drivers = db.query(Driver).join(Stint, Stint.driver_id == Driver.id).filter(Stint.race_id == race_id).distinct().all()
    if not drivers:
        drivers = db.query(Driver).all()

    stints_all = db.query(Stint).filter(Stint.race_id == race_id).order_by(Stint.stint_number).all()
    pits_all = db.query(PitStop).filter(PitStop.race_id == race_id).order_by(PitStop.lap).all()

    stints_by_driver = {}
    for s in stints_all:
        stints_by_driver.setdefault(s.driver_id, []).append(s)

    pits_by_driver = {}
    for p in pits_all:
        pits_by_driver.setdefault(p.driver_id, []).append(p)

    res = []
    for d in drivers:
        d_stints = stints_by_driver.get(d.id, [])
        d_pits = pits_by_driver.get(d.id, [])

        if not d_stints:
            continue

        res.append(
            DriverStrategyResponse(
                driver_id=d.id,
                driver_code=d.driver_code,
                driver_name=d.full_name,
                team=d.team,
                team_color=d.team_color or "#E10600",
                stints=[
                    StintResponse(
                        id=s.id,
                        driver_id=s.driver_id,
                        driver_code=d.driver_code,
                        stint_number=s.stint_number,
                        start_lap=s.start_lap,
                        end_lap=s.end_lap,
                        compound=s.compound.upper(),
                        tyre_age_start=s.tyre_age_start,
                        tyre_age_end=s.tyre_age_end,
                        stint_length=s.end_lap - s.start_lap + 1,
                    )
                    for s in d_stints
                ],
                pit_stops=[
                    PitStopResponse(
                        id=p.id,
                        race_id=p.race_id,
                        driver_id=p.driver_id,
                        driver_code=d.driver_code,
                        lap=p.lap,
                        duration=p.duration,
                        stop_number=p.stop_number,
                    )
                    for p in d_pits
                ],
            )
        )

    # Sort drivers roughly by start order or code
    return sorted(res, key=lambda x: x.driver_id)
