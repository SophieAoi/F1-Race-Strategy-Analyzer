from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.data.cleaning import clean_laps


@dataclass
class StintDegradation:
    driver: str
    stint_number: int
    compound: str
    num_laps: int
    deg_s_per_lap: float
    intercept_s: float


def _lap_time_seconds(laps: pd.DataFrame) -> pd.Series:
    return laps["LapTime"].dt.total_seconds()


def fit_stint_degradation(laps: pd.DataFrame) -> list[StintDegradation]:
    """Fit a linear trend (lap time vs. tyre age) per driver/stint on clean laps only.

    Returns one StintDegradation per stint with at least 3 clean laps —
    shorter stints don't have enough points for a meaningful fit.
    """
    clean = clean_laps(laps)
    results = []

    for (driver, stint_number), group in clean.groupby(["Driver", "Stint"]):
        if len(group) < 3:
            continue

        x = group["TyreLife"].to_numpy(dtype=float)
        y = _lap_time_seconds(group).to_numpy()

        slope, intercept = np.polyfit(x, y, 1)

        results.append(
            StintDegradation(
                driver=driver,
                stint_number=int(stint_number),
                compound=group["Compound"].iloc[0],
                num_laps=len(group),
                deg_s_per_lap=float(slope),
                intercept_s=float(intercept),
            )
        )

    return results


def degradation_by_compound(stint_results: list[StintDegradation]) -> pd.DataFrame:
    """Aggregate per-stint degradation into an average seconds/lap per compound."""
    df = pd.DataFrame([vars(r) for r in stint_results])
    if df.empty:
        return df

    return (
        df.groupby("compound")
        .agg(
            avg_deg_s_per_lap=("deg_s_per_lap", "mean"),
            num_stints=("deg_s_per_lap", "count"),
            total_clean_laps=("num_laps", "sum"),
        )
        .sort_values("avg_deg_s_per_lap")
        .reset_index()
    )
