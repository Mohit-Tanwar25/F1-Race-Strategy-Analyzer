import logging
from typing import List, Dict, Any, Optional
import httpx
from app.services.data_provider.base import F1DataProvider
from app.services.data_provider.curated_data import get_curated_races, get_curated_race_detail

logger = logging.getLogger(__name__)


class RealF1DataProvider(F1DataProvider):
    """
    F1 Data Provider supporting online REST retrieval (Jolpica / Ergast / OpenF1)
    with pre-packaged authentic historical race datasets for high reliability and offline execution.
    """

    def __init__(self, use_online_fallback: bool = True):
        self.use_online_fallback = use_online_fallback
        self.base_jolpica_url = "https://api.jolpi.ca/ergast/f1"

    def get_seasons(self) -> List[int]:
        """Return supported seasons."""
        return [2024, 2023]

    def get_races(self, season: int) -> List[Dict[str, Any]]:
        """Return races for season."""
        curated = get_curated_races(season)
        if curated:
            return curated

        if self.use_online_fallback:
            try:
                url = f"{self.base_jolpica_url}/{season}.json"
                with httpx.Client(timeout=8.0) as client:
                    resp = client.get(url)
                    if resp.status_code == 200:
                        data = resp.json()
                        race_table = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
                        return [
                            {
                                "season": int(r["season"]),
                                "round": int(r["round"]),
                                "name": r["raceName"],
                                "circuit": r.get("Circuit", {}).get("circuitName", "Grand Prix Circuit"),
                                "country": r.get("Circuit", {}).get("Location", {}).get("country", "Global"),
                                "date": r.get("date", "2024-01-01"),
                                "total_laps": 57,
                                "winner_name": None,
                            }
                            for r in race_table
                        ]
            except Exception as e:
                logger.warning(f"Failed to fetch online races for {season}: {e}")

        return []

    def _get_detail(self, season: int, round_number: int) -> Optional[Dict[str, Any]]:
        return get_curated_race_detail(season, round_number)

    def get_drivers(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        detail = self._get_detail(season, round_number)
        if detail:
            return detail.get("drivers", [])
        return []

    def get_lap_data(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        detail = self._get_detail(season, round_number)
        if detail:
            return detail.get("laps", [])
        return []

    def get_pit_stops(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        detail = self._get_detail(season, round_number)
        if detail:
            return detail.get("pit_stops", [])
        return []

    def get_stints(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        detail = self._get_detail(season, round_number)
        if detail:
            return detail.get("stints", [])
        return []

    def get_race_events(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        detail = self._get_detail(season, round_number)
        if detail:
            return detail.get("events", [])
        return []
