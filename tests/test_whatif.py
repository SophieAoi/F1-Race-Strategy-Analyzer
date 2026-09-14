import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.whatif import StrategyPlan, simulate_strategy
from src.data.loader import enable_cache, load_session

enable_cache("cache")


def test_replaying_actual_strategy_reproduces_actual_time():
    session = load_session(2023, "Monza", "R")
    actual_plan = StrategyPlan(stints=[("MEDIUM", 20), ("HARD", 31)])

    result = simulate_strategy(session, "VER", actual_plan)

    # replaying VER's real stint lengths/compounds should predict a total
    # time very close to what actually happened (model self-consistency check)
    assert abs(result.delta_s) < 5.0


def test_two_stop_alternate_is_slower_on_a_low_deg_track():
    session = load_session(2023, "Monza", "R")
    two_stop = StrategyPlan(stints=[("MEDIUM", 17), ("HARD", 17), ("HARD", 17)])

    result = simulate_strategy(session, "VER", two_stop)

    assert result.plan.num_stops == 2
    # Monza 2023 was a famously low-degradation race where 1-stop dominated;
    # an extra stop's pit loss should outweigh the tyre-freshness benefit
    assert result.delta_s > 0


def test_strategy_plan_properties():
    plan = StrategyPlan(stints=[("MEDIUM", 20), ("HARD", 31)])

    assert plan.total_laps == 51
    assert plan.num_stops == 1
