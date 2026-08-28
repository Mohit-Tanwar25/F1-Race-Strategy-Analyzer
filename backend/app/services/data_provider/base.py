from abc import ABC, abstractmethod
from typing import List, Dict, Any


class F1DataProvider(ABC):
    """
    Abstract Base Class for F1 Data Providers.
    Allows swappable ingestion sources (Jolpica/Ergast, OpenF1, FastF1, local telemetry files).
    """

    @abstractmethod
    def get_seasons(self) -> List[int]:
        """Return available seasons."""
        pass

    @abstractmethod
    def get_races(self, season: int) -> List[Dict[str, Any]]:
        """Return list of races for a given season."""
        pass

    @abstractmethod
    def get_drivers(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        """Return list of drivers participating in the race."""
        pass

    @abstractmethod
    def get_lap_data(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        """Return lap times and sector timing records."""
        pass

    @abstractmethod
    def get_pit_stops(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        """Return pit stops data."""
        pass

    @abstractmethod
    def get_stints(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        """Return tyre compound and stint usage."""
        pass

    @abstractmethod
    def get_race_events(self, season: int, round_number: int) -> List[Dict[str, Any]]:
        """Return Safety Car, VSC, Red Flag, and race events."""
        pass
