from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.data_provider.real_f1_provider import RealF1DataProvider
from app.services.ingestion import ingest_race_data

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("")
def trigger_ingestion(
    season: int = Query(2024, description="Season year"),
    round: int = Query(1, description="Round number"),
    db: Session = Depends(get_db)
):
    """
    Ingest or refresh authentic race data into the database.
    """
    try:
        provider = RealF1DataProvider()
        result = ingest_race_data(db, provider, season, round)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
