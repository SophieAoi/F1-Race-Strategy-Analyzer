"""Stretch Phase A: strategy what-if simulator.

Compares the driver's actual strategy against hypothetical alternates using
the fitted degradation model (Phase 3) and average pit loss (Phase 5).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.whatif import StrategyPlan, simulate_strategy
from src.data.loader import enable_cache, load_session

enable_cache("cache")

YEAR = 2023
EVENT = "Monza"
DRIVER = "VER"

session = load_session(YEAR, EVENT, "R")

# VER's actual strategy: Medium x20, Hard x31 (one stop)
actual_plan = StrategyPlan(stints=[("MEDIUM", 20), ("HARD", 31)])

# Alternates to test against the actual one-stop
candidate_plans = {
    "Actual (M20 / H31)": actual_plan,
    "Two-stop (M17 / H17 / H17)": StrategyPlan(stints=[("MEDIUM", 17), ("HARD", 17), ("HARD", 17)]),
    "One-stop, earlier split (M15 / H36)": StrategyPlan(stints=[("MEDIUM", 15), ("HARD", 36)]),
    "One-stop, later split (M30 / H21)": StrategyPlan(stints=[("MEDIUM", 30), ("HARD", 21)]),
}

print(f"=== Strategy what-if: {DRIVER} — {EVENT} {YEAR} ===\n")

for name, plan in candidate_plans.items():
    result = simulate_strategy(session, DRIVER, plan)
    sign = "faster" if result.delta_s < 0 else "slower"
    print(
        f"{name:<38} predicted={result.predicted_total_s:8.1f}s  "
        f"actual={result.actual_total_s:8.1f}s  "
        f"delta={result.delta_s:+7.1f}s ({sign} than actual)"
    )

print(
    "\nNote: this model ignores traffic, safety car timing, and track position — "
    "it compares raw predicted pace + pit loss only. Read deltas as a pace signal, "
    "not a race-result prediction."
)
