import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.loader import enable_cache, load_session
from src.data.cleaning import clean_laps, flag_pit_laps, flag_caution_laps, flag_invalid_laps

enable_cache("cache")


def _monza_2023():
    return load_session(2023, "Monza", "R")


def test_verstappen_pit_stop_count_matches_public_record():
    session = _monza_2023()
    laps = session.laps
    ver = laps[laps["Driver"] == "VER"]

    assert len(ver) == 51
    # one pit stop shows up as 2 flagged laps: the in-lap (PitInTime set)
    # and the following out-lap (PitOutTime set)
    assert flag_pit_laps(ver).sum() == 2
    assert ver["PitInTime"].notna().sum() == 1
    assert sorted(ver["Stint"].unique()) == [1.0, 2.0]


def test_clean_laps_drops_pit_and_invalid_laps():
    session = _monza_2023()
    laps = session.laps
    ver = laps[laps["Driver"] == "VER"]

    cleaned = clean_laps(ver)

    assert len(cleaned) < len(ver)
    assert not flag_pit_laps(cleaned).any()
    assert not flag_invalid_laps(cleaned).any()
    assert not flag_caution_laps(cleaned).any()


def test_caution_flag_detects_non_green_status():
    session = load_session(2023, "Singapore", "R")
    laps = session.laps

    caution = flag_caution_laps(laps)

    assert caution.any()
    assert not caution.all()
