import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.race import Race
from app.models.driver import Driver
from app.models.lap import Lap
from app.models.stint import Stint
from app.models.pit_stop import PitStop
from app.models.race_event import RaceEvent
from app.analysis.lap_times import parse_lap_time
from app.services.data_provider.base import F1DataProvider

logger = logging.getLogger(__name__)


def ingest_race_data(
    db: Session,
    provider: F1DataProvider,
    season: int,
    round_number: int
) -> Dict[str, Any]:
    """
    Idempotent data ingestion pipeline:
    External Data -> Validation -> Normalization -> Processing -> Database.
    Running multiple times updates or safely replaces race records without duplicates.
    """
    logger.info(f"Starting ingestion for Season {season} Round {round_number}...")

    # 1. Fetch race overview
    races = provider.get_races(season)
    race_info = next((r for r in races if r["round"] == round_number), None)
    if not race_info:
        raise ValueError(f"Race not found for Season {season} Round {round_number}")

    # Check or create Race
    race = db.query(Race).filter(Race.season == season, Race.round == round_number).first()
    if not race:
        race = Race(
            season=season,
            round=round_number,
            name=race_info["name"],
            circuit=race_info["circuit"],
            country=race_info["country"],
            date=race_info["date"],
            total_laps=race_info.get("total_laps", 50),
            winner_name=race_info.get("winner_name"),
        )
        db.add(race)
        db.flush()
    else:
        race.name = race_info["name"]
        race.circuit = race_info["circuit"]
        race.country = race_info["country"]
        race.date = race_info["date"]
        race.total_laps = race_info.get("total_laps", race.total_laps)
        race.winner_name = race_info.get("winner_name", race.winner_name)
        db.flush()

    # 2. Ingest Drivers
    driver_data_list = provider.get_drivers(season, round_number)
    driver_map: Dict[str, Driver] = {}

    for d_data in driver_data_list:
        code = d_data["driver_code"]
        driver = db.query(Driver).filter(Driver.driver_code == code).first()
        if not driver:
            driver = Driver(
                driver_code=code,
                full_name=d_data["full_name"],
                permanent_number=d_data.get("permanent_number"),
                team=d_data["team"],
                team_color=d_data.get("team_color", "#E10600"),
            )
            db.add(driver)
            db.flush()
        else:
            driver.full_name = d_data["full_name"]
            driver.team = d_data["team"]
            driver.team_color = d_data.get("team_color", driver.team_color)
            db.flush()
        driver_map[code] = driver

    # Clean existing race child records for idempotency
    db.query(Lap).filter(Lap.race_id == race.id).delete()
    db.query(Stint).filter(Stint.race_id == race.id).delete()
    db.query(PitStop).filter(PitStop.race_id == race.id).delete()
    db.query(RaceEvent).filter(RaceEvent.race_id == race.id).delete()
    db.flush()

    # 3. Ingest Laps
    raw_laps = provider.get_lap_data(season, round_number)
    lap_objects = []
    for l in raw_laps:
        d_code = l.get("driver_code")
        driver = driver_map.get(d_code)
        if not driver:
            continue

        lap_sec = parse_lap_time(l.get("lap_time"))
        s1 = parse_lap_time(l.get("sector_1"))
        s2 = parse_lap_time(l.get("sector_2"))
        s3 = parse_lap_time(l.get("sector_3"))

        lap_obj = Lap(
            race_id=race.id,
            driver_id=driver.id,
            lap_number=l["lap_number"],
            lap_time=lap_sec,
            sector_1=s1,
            sector_2=s2,
            sector_3=s3,
            position=l.get("position"),
            pit_stop=bool(l.get("pit_stop", False)),
            is_valid=bool(l.get("is_valid", True)),
        )
        lap_objects.append(lap_obj)

    if lap_objects:
        db.bulk_save_objects(lap_objects)

    # 4. Ingest Stints
    raw_stints = provider.get_stints(season, round_number)
    stint_objects = []
    for s in raw_stints:
        d_code = s.get("driver_code")
        driver = driver_map.get(d_code)
        if not driver:
            continue

        stint_obj = Stint(
            race_id=race.id,
            driver_id=driver.id,
            stint_number=s["stint_number"],
            start_lap=s["start_lap"],
            end_lap=s["end_lap"],
            compound=s.get("compound", "MEDIUM").upper(),
            tyre_age_start=s.get("tyre_age_start", 0),
            tyre_age_end=s.get("tyre_age_end", s["end_lap"] - s["start_lap"] + 1),
        )
        stint_objects.append(stint_obj)

    if stint_objects:
        db.bulk_save_objects(stint_objects)

    # 5. Ingest Pit Stops
    raw_pits = provider.get_pit_stops(season, round_number)
    pit_objects = []
    for p in raw_pits:
        d_code = p.get("driver_code")
        driver = driver_map.get(d_code)
        if not driver:
            continue

        pit_obj = PitStop(
            race_id=race.id,
            driver_id=driver.id,
            lap=p["lap"],
            duration=p.get("duration"),
            stop_number=p.get("stop_number", 1),
        )
        pit_objects.append(pit_obj)

    if pit_objects:
        db.bulk_save_objects(pit_objects)

    # 6. Ingest Events
    raw_events = provider.get_race_events(season, round_number)
    event_objects = []
    for ev in raw_events:
        event_obj = RaceEvent(
            race_id=race.id,
            lap=ev["lap"],
            start_lap=ev.get("start_lap", ev["lap"]),
            end_lap=ev.get("end_lap", ev["lap"]),
            event_type=ev.get("event_type", "OTHER").upper(),
            description=ev.get("description"),
        )
        event_objects.append(event_obj)

    if event_objects:
        db.bulk_save_objects(event_objects)

    db.commit()
    logger.info(f"Ingestion completed for Race ID {race.id} ({race.name}).")

    return {
        "status": "success",
        "race_id": race.id,
        "race_name": race.name,
        "season": race.season,
        "round": race.round,
        "drivers_count": len(driver_map),
        "laps_ingested": len(lap_objects),
        "stints_ingested": len(stint_objects),
        "pit_stops_ingested": len(pit_objects),
        "events_ingested": len(event_objects),
    }
