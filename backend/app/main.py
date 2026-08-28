import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import Base, engine, SessionLocal
from app.api.router import api_router
from app.services.data_provider.real_f1_provider import RealF1DataProvider
from app.services.ingestion import ingest_race_data
from app.models.race import Race

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("f1_strategy_app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and auto-seed initial races if empty
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        race_count = db.query(Race).count()
        if race_count == 0:
            logger.info("Database is empty. Seeding initial flagship races (Bahrain, Silverstone, Miami, Spa)...")
            provider = RealF1DataProvider()
            for rnd in [1, 6, 12, 14]:
                try:
                    ingest_race_data(db, provider, season=2024, round_number=rnd)
                except Exception as e:
                    logger.error(f"Error seeding 2024 round {rnd}: {e}")
            logger.info("Initial seeding complete.")
    finally:
        db.close()

    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="F1 Race Strategy Analyzer API",
    description="Professional full-stack telemetry and race strategy analytics API for Formula 1.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API
app.include_router(api_router)


@app.get("/")
def root():
    return {
        "service": "F1 Race Strategy Analyzer API",
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "seasons": "/api/seasons",
            "races": "/api/seasons/2024/races",
            "strategies": "/api/races/1/strategies",
            "degradation": "/api/races/1/analysis/degradation",
            "undercuts": "/api/races/1/analysis/undercuts",
            "overcuts": "/api/races/1/analysis/overcuts",
            "scores": "/api/races/1/analysis/scores",
            "compare": "/api/races/1/compare?driver1=1&driver2=2",
        },
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
