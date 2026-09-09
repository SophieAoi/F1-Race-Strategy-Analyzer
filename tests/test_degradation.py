import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.degradation import degradation_by_compound, fit_stint_degradation
from src.data.loader import enable_cache, load_session

enable_cache("cache")


def test_verstappen_stint_degradation_monza_2023():
    session = load_session(2023, "Monza", "R")
    laps = session.laps[session.laps["Driver"] == "VER"]

    fits = fit_stint_degradation(laps)

    assert len(fits) == 2
    stint1, stint2 = sorted(fits, key=lambda f: f.stint_number)

    assert stint1.compound == "MEDIUM"
    assert stint2.compound == "HARD"
    # both stints show some positive degradation on this low-deg track
    assert stint1.deg_s_per_lap > 0
    assert stint2.deg_s_per_lap > 0
    # sanity bound: shouldn't see wild values from a bad fit
    assert stint1.deg_s_per_lap < 1.0
    assert stint2.deg_s_per_lap < 1.0


def test_short_stints_are_excluded():
    session = load_session(2023, "Monza", "R")
    laps = session.laps

    fits = fit_stint_degradation(laps)

    for f in fits:
        assert f.num_laps >= 3


def test_degradation_by_compound_aggregates_correctly():
    session = load_session(2023, "Monza", "R")
    fits = fit_stint_degradation(session.laps)

    summary = degradation_by_compound(fits)

    assert set(summary["compound"]) <= {"SOFT", "MEDIUM", "HARD", "INTERMEDIATE", "WET"}
    assert (summary["num_stints"] > 0).all()
    assert (summary["total_clean_laps"] > 0).all()
