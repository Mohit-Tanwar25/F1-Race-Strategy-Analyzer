from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.race import Race
from app.models.driver import Driver
from app.models.lap import Lap
from app.schemas.f1_schemas import DriverResponse

router = APIRouter(prefix="/races", tags=["Drivers"])


@router.get("/{race_id}/drivers", response_model=List[DriverResponse])
def get_race_drivers(race_id: int, db: Session = Depends(get_db)):
    """
    Get all drivers who participated in the specified race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    driver_ids = [d[0] for d in db.query(Lap.driver_id).filter(Lap.race_id == race_id).distinct().all()]
    if not driver_ids:
        # Fallback to all drivers
        drivers = db.query(Driver).all()
        return drivers

    drivers = db.query(Driver).filter(Driver.id.in_(driver_ids)).order_by(Driver.full_name).all()
    return drivers
