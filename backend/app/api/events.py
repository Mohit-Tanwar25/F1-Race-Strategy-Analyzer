from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.race import Race
from app.models.race_event import RaceEvent
from app.schemas.f1_schemas import RaceEventResponse

router = APIRouter(prefix="/races", tags=["Events"])


@router.get("/{race_id}/events", response_model=List[RaceEventResponse])
def get_race_events(race_id: int, db: Session = Depends(get_db)):
    """
    Get Safety Car, VSC, Red Flag, and incident events for a race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    events = db.query(RaceEvent).filter(RaceEvent.race_id == race_id).order_by(RaceEvent.lap).all()
    return events
