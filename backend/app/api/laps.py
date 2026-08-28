from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.race import Race
from app.models.driver import Driver
from app.models.lap import Lap
from app.schemas.f1_schemas import LapResponse

router = APIRouter(prefix="/races", tags=["Laps"])


@router.get("/{race_id}/laps/{driver_id}", response_model=List[LapResponse])
def get_driver_laps(
    race_id: int,
    driver_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all laps for a specific driver in a race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    laps = (
        db.query(Lap)
        .filter(Lap.race_id == race_id, Lap.driver_id == driver_id)
        .order_by(Lap.lap_number)
        .all()
    )

    return [
        LapResponse(
            id=l.id,
            race_id=l.race_id,
            driver_id=l.driver_id,
            driver_code=driver.driver_code,
            lap_number=l.lap_number,
            lap_time=l.lap_time,
            sector_1=l.sector_1,
            sector_2=l.sector_2,
            sector_3=l.sector_3,
            position=l.position,
            pit_stop=l.pit_stop,
            is_valid=l.is_valid,
        )
        for l in laps
    ]


@router.get("/{race_id}/all-laps", response_model=List[LapResponse])
def get_all_race_laps(
    race_id: int,
    drivers: Optional[str] = Query(None, description="Comma-separated driver IDs"),
    db: Session = Depends(get_db)
):
    """
    Get laps for all or selected drivers in a race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    query = db.query(Lap, Driver).join(Driver, Lap.driver_id == Driver.id).filter(Lap.race_id == race_id)

    if drivers:
        d_ids = [int(x.strip()) for x in drivers.split(",") if x.strip().isdigit()]
        if d_ids:
            query = query.filter(Lap.driver_id.in_(d_ids))

    results = query.order_by(Lap.driver_id, Lap.lap_number).all()

    return [
        LapResponse(
            id=l.id,
            race_id=l.race_id,
            driver_id=l.driver_id,
            driver_code=d.driver_code,
            lap_number=l.lap_number,
            lap_time=l.lap_time,
            sector_1=l.sector_1,
            sector_2=l.sector_2,
            sector_3=l.sector_3,
            position=l.position,
            pit_stop=l.pit_stop,
            is_valid=l.is_valid,
        )
        for l, d in results
    ]
