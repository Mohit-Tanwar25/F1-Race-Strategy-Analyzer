from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.race import Race
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.models.race_event import RaceEvent
from app.schemas.f1_schemas import DriverComparisonResponse
from app.analysis.comparison import compare_two_drivers

router = APIRouter(prefix="/races", tags=["Comparison"])


@router.get("/{race_id}/compare", response_model=DriverComparisonResponse)
def get_driver_comparison(
    race_id: int,
    driver1: int = Query(..., description="Driver 1 ID"),
    driver2: int = Query(..., description="Driver 2 ID"),
    db: Session = Depends(get_db),
):
    """
    Compare two drivers head-to-head on strategy, pace, stints, and lap delta progression.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    d1 = db.query(Driver).filter(Driver.id == driver1).first()
    d2 = db.query(Driver).filter(Driver.id == driver2).first()
    if not d1 or not d2:
        raise HTTPException(status_code=404, detail="One or both drivers not found")

    laps1 = db.query(Lap).filter(Lap.race_id == race_id, Lap.driver_id == driver1).order_by(Lap.lap_number).all()
    laps2 = db.query(Lap).filter(Lap.race_id == race_id, Lap.driver_id == driver2).order_by(Lap.lap_number).all()

    stints1 = db.query(Stint).filter(Stint.race_id == race_id, Stint.driver_id == driver1).order_by(Stint.stint_number).all()
    stints2 = db.query(Stint).filter(Stint.race_id == race_id, Stint.driver_id == driver2).order_by(Stint.stint_number).all()

    pits1 = db.query(PitStop).filter(PitStop.race_id == race_id, PitStop.driver_id == driver1).order_by(PitStop.lap).all()
    pits2 = db.query(PitStop).filter(PitStop.race_id == race_id, PitStop.driver_id == driver2).order_by(PitStop.lap).all()

    events = db.query(RaceEvent).filter(RaceEvent.race_id == race_id).all()

    res = compare_two_drivers(
        driver1=d1,
        driver2=d2,
        laps1=laps1,
        laps2=laps2,
        stints1=stints1,
        stints2=stints2,
        pits1=pits1,
        pits2=pits2,
        events=events,
        total_laps=race.total_laps or 50,
    )

    return DriverComparisonResponse(
        race_id=race.id,
        race_name=race.name,
        driver1=res["driver1"],
        driver2=res["driver2"],
        driver1_stints=res["driver1_stints"],
        driver2_stints=res["driver2_stints"],
        driver1_pit_stops=res["driver1_pit_stops"],
        driver2_pit_stops=res["driver2_pit_stops"],
        lap_deltas=res["lap_deltas"],
        faster_driver_code=res["faster_driver_code"],
        key_strategic_differences=res["key_strategic_differences"],
    )
