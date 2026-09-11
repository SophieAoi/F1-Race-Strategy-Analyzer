import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.pace import driver_pit_laps, driver_rolling_pace, find_crossovers
from src.data.loader import enable_cache, load_session

enable_cache("cache")


def test_rolling_pace_excludes_pit_laps():
    session = load_session(2023, "Monza", "R")
    laps = session.laps

    pace = driver_rolling_pace(laps, "VER")

    # VER pitted once (in-lap 20) out of 51 laps; that in-lap should be gone
    assert 20 not in pace["LapNumber"].tolist()
    assert len(pace) < 51


def test_driver_pit_laps_matches_known_stop():
    session = load_session(2023, "Monza", "R")

    pit_laps = driver_pit_laps(session.laps, "VER")

    assert pit_laps == [20]


def test_find_crossovers_collapses_noisy_flips():
    session = load_session(2023, "Monza", "R")
    laps = session.laps

    pace_a = driver_rolling_pace(laps, "VER")
    pace_b = driver_rolling_pace(laps, "PER")

    crossovers = find_crossovers(pace_a, pace_b, min_gap=3)

    # consecutive crossovers must be spaced at least min_gap laps apart
    for a, b in zip(crossovers, crossovers[1:]):
        assert b - a >= 3
