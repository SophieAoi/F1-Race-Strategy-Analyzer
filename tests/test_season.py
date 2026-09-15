import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.season import (
    season_summary_table,
    summarize_driver_race,
    summarize_driver_season,
)
from src.data.loader import enable_cache

enable_cache("cache")


def test_summarize_driver_race_monza_matches_known_data():
    summary = summarize_driver_race(2023, "Monza", "VER")

    assert summary.num_stops == 1
    assert summary.compounds_used == ["MEDIUM", "HARD"]
    assert summary.finishing_position == 1
    assert summary.avg_deg_s_per_lap is not None


def test_summarize_driver_season_skips_failing_events():
    # FastF1 fuzzy-matches event name strings against the season schedule, so
    # a typo'd name silently resolves to *some* real event rather than
    # failing — an out-of-range round number is what reliably raises.
    summaries = summarize_driver_season(2023, ["Monza", 25], "VER")

    # the bad event is skipped, not raised
    assert len(summaries) == 1
    assert summaries[0].event == "Monza"


def test_season_summary_table_has_expected_columns():
    summaries = summarize_driver_season(2023, ["Monza", "Singapore"], "VER")

    table = season_summary_table(summaries)

    assert list(table.columns) == ["Event", "Position", "Stops", "Compounds", "Avg Deg (s/lap)"]
    assert len(table) == 2
