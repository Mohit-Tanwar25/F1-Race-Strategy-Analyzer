from fastapi import APIRouter
from app.api.seasons import router as seasons_router
from app.api.races import router as races_router
from app.api.drivers import router as drivers_router
from app.api.laps import router as laps_router
from app.api.strategies import router as strategies_router
from app.api.events import router as events_router
from app.api.analysis import router as analysis_router
from app.api.compare import router as compare_router
from app.api.ingest_api import router as ingest_router

api_router = APIRouter(prefix="/api")

api_router.include_router(seasons_router)
api_router.include_router(races_router)
api_router.include_router(drivers_router)
api_router.include_router(laps_router)
api_router.include_router(strategies_router)
api_router.include_router(events_router)
api_router.include_router(analysis_router)
api_router.include_router(compare_router)
api_router.include_router(ingest_router)
