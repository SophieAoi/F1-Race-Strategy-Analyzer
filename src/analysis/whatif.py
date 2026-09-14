from dataclasses import dataclass

import pandas as pd

from src.analysis.degradation import StintDegradation, fit_stint_degradation
from src.analysis.pitstops import extract_pit_stops


@dataclass
class StrategyPlan:
    """A hypothetical strategy: an ordered list of (compound, stint_length)."""

    stints: list[tuple[str, int]]

    @property
    def total_laps(self) -> int:
        return sum(length for _, length in self.stints)

    @property
    def num_stops(self) -> int:
        return len(self.stints) - 1


@dataclass
class SimulationResult:
    plan: StrategyPlan
    predicted_total_s: float
    actual_total_s: float

    @property
    def delta_s(self) -> float:
        """Negative means the hypothetical strategy would have been faster."""
        return self.predicted_total_s - self.actual_total_s


def _compound_models(driver_fits: list[StintDegradation], field_fits: list[StintDegradation]) -> dict:
    """Per-compound (slope, intercept) using this driver's own fitted stints
    where available, falling back to the field-wide average for compounds
    the driver never actually ran."""
    models = {}

    for compound in {f.compound for f in field_fits}:
        driver_matches = [f for f in driver_fits if f.compound == compound]
        if driver_matches:
            slope = sum(f.deg_s_per_lap for f in driver_matches) / len(driver_matches)
            intercept = sum(f.intercept_s for f in driver_matches) / len(driver_matches)
        else:
            field_matches = [f for f in field_fits if f.compound == compound]
            slope = sum(f.deg_s_per_lap for f in field_matches) / len(field_matches)
            intercept = sum(f.intercept_s for f in field_matches) / len(field_matches)
        models[compound] = (slope, intercept)

    return models


def _predict_stint_time(slope: float, intercept: float, num_laps: int) -> float:
    """Sum of predicted lap times for tyre ages 1..num_laps under a linear
    degradation model: lap_time(age) = intercept + slope * age."""
    return sum(intercept + slope * age for age in range(1, num_laps + 1))


def _average_pit_loss(laps: pd.DataFrame) -> float:
    """Field-wide average time lost per pit stop, used as the cost of each
    hypothetical stop (a driver-specific average would be noisier with only
    1-2 real stops to sample from)."""
    all_losses = []
    for driver in laps["Driver"].unique():
        for stop in extract_pit_stops(laps, driver):
            if stop.time_lost_s is not None:
                all_losses.append(stop.time_lost_s)
    return sum(all_losses) / len(all_losses) if all_losses else 25.0


def simulate_strategy(
    session, driver: str, plan: StrategyPlan
) -> SimulationResult:
    """Predict total race time for a hypothetical strategy and compare it to
    the driver's actual recorded race time.

    Limitations: this model has no awareness of traffic, safety car timing,
    or track position (an undercut/overcut's real value comes from position,
    which this ignores entirely) — it only compares raw predicted pace plus
    pit loss. Treat results as a rough "was this strategy family faster on
    pure pace" signal, not a race-winning prediction.
    """
    laps = session.laps
    driver_laps = laps[laps["Driver"] == driver]

    driver_fits = fit_stint_degradation(driver_laps)
    field_fits = fit_stint_degradation(laps)
    models = _compound_models(driver_fits, field_fits)

    pit_loss = _average_pit_loss(laps)

    predicted_total = 0.0
    for compound, num_laps in plan.stints:
        slope, intercept = models[compound]
        predicted_total += _predict_stint_time(slope, intercept, num_laps)
    predicted_total += plan.num_stops * pit_loss

    actual_total_s = driver_laps["LapTime"].dt.total_seconds().sum()

    return SimulationResult(plan=plan, predicted_total_s=predicted_total, actual_total_s=actual_total_s)
