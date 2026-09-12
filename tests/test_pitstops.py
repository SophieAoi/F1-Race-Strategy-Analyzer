import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.pitstops import all_pit_stops, extract_pit_stops, pit_stops_table
from src.data.loader import enable_cache, load_session

enable_cache("cache")


def test_verstappen_single_stop_matches_known_data():
    session = load_session(2023, "Monza", "R")

    stops = extract_pit_stops(session.laps, "VER")

    assert len(stops) == 1
    stop = stops[0]
    assert stop.lap == 20
    assert stop.position_before == 1
    assert 20 < stop.stationary_s < 30
    assert stop.time_lost_s > 0


def test_retirement_in_pits_has_no_out_lap_data():
    session = load_session(2023, "Monza", "R")

    stops = extract_pit_stops(session.laps, "OCO")

    last_stop = stops[-1]
    assert last_stop.position_after is None
    assert last_stop.time_lost_s is None


def test_all_pit_stops_sorted_by_lap():
    session = load_session(2023, "Monza", "R")

    stops = all_pit_stops(session.laps)

    laps = [s.lap for s in stops]
    assert laps == sorted(laps)
    assert len(stops) > 0


def test_pit_stops_table_has_expected_columns():
    session = load_session(2023, "Monza", "R")
    stops = all_pit_stops(session.laps)

    table = pit_stops_table(stops)

    assert list(table.columns) == [
        "Driver",
        "Lap",
        "Stationary (s)",
        "Pos Before",
        "Pos After",
        "Pos Change",
        "Time Lost (s)",
    ]
    assert len(table) == len(stops)
