import sys
import os
import argparse
import logging

# Ensure backend directory is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.database.session import Base, engine, SessionLocal
from app.services.data_provider.real_f1_provider import RealF1DataProvider
from app.services.ingestion import ingest_race_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ingest_cli")


def main():
    parser = argparse.ArgumentParser(description="Ingest F1 race strategy data into the database.")
    parser.add_argument("--season", type=int, default=2024, help="Season year (e.g. 2024)")
    parser.add_argument("--round", type=int, default=None, help="Race round number (e.g. 1)")
    parser.add_argument("--all", action="store_true", help="Ingest all curated flagship races")

    args = parser.parse_args()

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    provider = RealF1DataProvider()
    db = SessionLocal()

    try:
        if args.all:
            logger.info("Ingesting all available flagship races...")
            races = provider.get_races(args.season)
            for r in races:
                res = ingest_race_data(db, provider, season=args.season, round_number=r["round"])
                logger.info(f"Ingested {res['race_name']}: {res['laps_ingested']} laps, {res['stints_ingested']} stints.")
        else:
            round_num = args.round if args.round is not None else 1
            res = ingest_race_data(db, provider, season=args.season, round_number=round_num)
            logger.info(f"Successfully ingested {res['race_name']}: {res['laps_ingested']} laps, {res['stints_ingested']} stints.")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
