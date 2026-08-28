import re
from typing import Optional, List, Dict, Any, Union
import numpy as np
import pandas as pd


def parse_lap_time(val: Union[str, float, int, None]) -> Optional[float]:
    """
    Parse various lap time formats into numeric seconds (float).
    Examples:
        "1:18.423" -> 78.423
        "01:24.050" -> 84.050
        "78.423" -> 78.423
        78.423 -> 78.423
    Returns None if missing or invalid.
    """
    if val is None or val == "" or pd.isna(val):
        return None

    if isinstance(val, (int, float)):
        if np.isnan(val) or val <= 0:
            return None
        return float(val)

    if isinstance(val, str):
        val = val.strip()
        if not val or val.lower() in ("nan", "none", "null", "nat"):
            return None

        # Check for M:SS.mmm or MM:SS.mmm format
        match = re.match(r"^(\d+):(\d{2})(?:\.(\d+))?$", val)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            milliseconds_str = match.group(3) or "0"
            milliseconds = float(f"0.{milliseconds_str}")
            total_seconds = minutes * 60 + seconds + milliseconds
            return round(total_seconds, 3)

        # Check for simple float string "78.423"
        try:
            sec = float(val)
            if sec > 0:
                return round(sec, 3)
        except ValueError:
            pass

    return None


def format_lap_time(seconds: Optional[float]) -> str:
    """
    Format numeric seconds into standard F1 lap time string M:SS.mmm.
    Example: 78.423 -> "1:18.423"
    """
    if seconds is None or np.isnan(seconds) or seconds <= 0:
        return "N/A"

    minutes = int(seconds // 60)
    rem_seconds = seconds % 60
    return f"{minutes}:{rem_seconds:06.3f}"


def calculate_lap_statistics(lap_times: List[float]) -> Dict[str, Any]:
    """
    Calculate statistical metrics for a list of lap times in seconds.
    Filters out None/NaN and extreme values.
    """
    clean_times = [t for t in lap_times if t is not None and not np.isnan(t) and t > 40.0]
    if not clean_times:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "std_dev": None,
            "formatted_mean": "N/A",
            "formatted_best": "N/A",
        }

    arr = np.array(clean_times)
    mean_val = float(np.mean(arr))
    median_val = float(np.median(arr))
    min_val = float(np.min(arr))
    max_val = float(np.max(arr))
    std_val = float(np.std(arr)) if len(arr) > 1 else 0.0

    return {
        "count": len(clean_times),
        "mean": round(mean_val, 3),
        "median": round(median_val, 3),
        "min": round(min_val, 3),
        "max": round(max_val, 3),
        "std_dev": round(std_val, 3),
        "formatted_mean": format_lap_time(mean_val),
        "formatted_best": format_lap_time(min_val),
    }


def compute_rolling_average(lap_times: List[Optional[float]], window: int = 3) -> List[Optional[float]]:
    """
    Compute rolling average lap pace over a given window size.
    """
    s = pd.Series(lap_times)
    rolling = s.rolling(window=window, min_periods=1).mean()
    return [round(float(v), 3) if not pd.isna(v) else None for v in rolling]
