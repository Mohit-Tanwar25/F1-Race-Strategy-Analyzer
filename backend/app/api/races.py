from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.database.session import get_db
from app.models.race import Race
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.pit_stop import PitStop
from app.models.race_event import RaceEvent
from app.schemas.f1_schemas import RaceResponse, RaceSummaryResponse
from app.analysis.lap_times import format_lap_time

router = APIRouter(prefix="/races", tags=["Races"])


@router.get("/{race_id}", response_model=RaceSummaryResponse)
def get_race(race_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information and summary stats for a single race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    drivers_count = db.query(distinct(Lap.driver_id)).filter(Lap.race_id == race_id).count()
    pit_stops_count = db.query(PitStop).filter(PitStop.race_id == race_id).count()
    sc_count = db.query(RaceEvent).filter(RaceEvent.race_id == race_id, RaceEvent.event_type == "SAFETY_CAR").count()
    vsc_count = db.query(RaceEvent).filter(RaceEvent.race_id == race_id, RaceEvent.event_type == "VSC").count()

    # Find fastest lap
    fastest_lap_record = (
        db.query(Lap, Driver)
        .join(Driver, Lap.driver_id == Driver.id)
        .filter(Lap.race_id == race_id, Lap.lap_time.isnot(None), Lap.is_valid.is_(True), Lap.pit_stop.is_(False))
        .order_by(Lap.lap_time.asc())
        .first()
    )

    fastest_data = None
    if fastest_lap_record:
        lap_obj, driver_obj = fastest_lap_record
        fastest_data = {
            "driver_code": driver_obj.driver_code,
            "driver_name": driver_obj.full_name,
            "team": driver_obj.team,
            "lap_number": lap_obj.lap_number,
            "lap_time": lap_obj.lap_time,
            "formatted_time": format_lap_time(lap_obj.lap_time),
        }

    return RaceSummaryResponse(
        id=race.id,
        season=race.season,
        round=race.round,
        name=race.name,
        circuit=race.circuit,
        country=race.country,
        date=race.date,
        total_laps=race.total_laps,
        winner_name=race.winner_name,
        drivers_count=drivers_count,
        total_pit_stops=pit_stops_count,
        safety_car_periods=sc_count,
        vsc_periods=vsc_count,
        fastest_lap=fastest_data,
    )
