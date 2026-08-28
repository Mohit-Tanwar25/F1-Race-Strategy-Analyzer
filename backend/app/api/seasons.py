from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.database.session import get_db
from app.models.race import Race
from app.services.data_provider.real_f1_provider import RealF1DataProvider

router = APIRouter(prefix="/seasons", tags=["Seasons"])


@router.get("", response_model=List[int])
def get_seasons(db: Session = Depends(get_db)):
    """
    Get all available seasons.
    """
    db_seasons = [s[0] for s in db.query(distinct(Race.season)).all() if s[0] is not None]
    if not db_seasons:
        provider = RealF1DataProvider()
        return sorted(provider.get_seasons(), reverse=True)
    return sorted(list(set(db_seasons)), reverse=True)


@router.get("/{year}/races")
def get_races_by_season(year: int, db: Session = Depends(get_db)):
    """
    Get all races for a specific season.
    """
    races = db.query(Race).filter(Race.season == year).order_by(Race.round).all()
    if not races:
        # Fallback to provider
        provider = RealF1DataProvider()
        return provider.get_races(year)

    return [
        {
            "id": r.id,
            "season": r.season,
            "round": r.round,
            "name": r.name,
            "circuit": r.circuit,
            "country": r.country,
            "date": r.date,
            "total_laps": r.total_laps,
            "winner_name": r.winner_name,
        }
        for r in races
    ]
