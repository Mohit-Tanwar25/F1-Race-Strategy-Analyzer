import pytest
from app.analysis.lap_times import (
    parse_lap_time,
    format_lap_time,
    calculate_lap_statistics,
    compute_rolling_average,
)


def test_parse_lap_time_formats():
    assert parse_lap_time("1:18.423") == 78.423
    assert parse_lap_time("01:24.050") == 84.050
    assert parse_lap_time("1:30") == 90.0
    assert parse_lap_time(78.423) == 78.423
    assert parse_lap_time("78.423") == 78.423
    assert parse_lap_time(None) is None
    assert parse_lap_time("INVALID") is None
    assert parse_lap_time("") is None
    assert parse_lap_time(-5.0) is None


def test_format_lap_time():
    assert format_lap_time(78.423) == "1:18.423"
    assert format_lap_time(90.050) == "1:30.050"
    assert format_lap_time(None) == "N/A"
    assert format_lap_time(-1) == "N/A"


def test_calculate_lap_statistics():
    laps = [90.0, 90.5, 91.0, 89.5, 90.0]
    stats = calculate_lap_statistics(laps)
    assert stats["count"] == 5
    assert stats["mean"] == 90.2
    assert stats["min"] == 89.5
    assert stats["max"] == 91.0
    assert stats["formatted_best"] == "1:29.500"


def test_compute_rolling_average():
    laps = [90.0, 92.0, 94.0]
    rolling = compute_rolling_average(laps, window=2)
    assert rolling[0] == 90.0
    assert rolling[1] == 91.0
    assert rolling[2] == 93.0
