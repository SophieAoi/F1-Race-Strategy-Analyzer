import pandas as pd

from src.data.cleaning import flag_pit_laps


def driver_rolling_pace(laps: pd.DataFrame, driver: str, window: int = 3) -> pd.DataFrame:
    """Rolling-average lap time for one driver across the race.

    Pit in/out laps are dropped before rolling (they're not representative of
    pace) but safety-car laps are kept, since the comparison should reflect
    what actually happened on track, not just clean-air pace.
    """
    sub = laps[laps["Driver"] == driver].sort_values("LapNumber").copy()
    sub = sub[~flag_pit_laps(sub)]
    sub = sub[sub["LapTime"].notna()]

    sub["LapTimeSeconds"] = sub["LapTime"].dt.total_seconds()
    sub["RollingPace"] = sub["LapTimeSeconds"].rolling(window, min_periods=1).mean()

    return sub[["LapNumber", "LapTimeSeconds", "RollingPace"]].reset_index(drop=True)


def driver_pit_laps(laps: pd.DataFrame, driver: str) -> list[int]:
    """Lap numbers on which the driver pitted (the in-lap of each stop)."""
    sub = laps[laps["Driver"] == driver]
    pit_in = sub[sub["PitInTime"].notna()]
    return pit_in["LapNumber"].astype(int).tolist()


def find_crossovers(pace_a: pd.DataFrame, pace_b: pd.DataFrame, min_gap: int = 3) -> list[int]:
    """Laps where the rolling-pace order between two drivers flips.

    Crossovers within `min_gap` laps of the previous one are dropped — at a
    short rolling window, near-identical pace produces rapid order flips that
    are noise rather than a genuine change in who's faster.
    """
    merged = pace_a.merge(pace_b, on="LapNumber", suffixes=("_a", "_b"))
    merged["a_faster"] = merged["RollingPace_a"] < merged["RollingPace_b"]

    crossovers = []
    prev = None
    last_lap = None
    for _, row in merged.iterrows():
        if prev is not None and row["a_faster"] != prev:
            lap = int(row["LapNumber"])
            if last_lap is None or lap - last_lap >= min_gap:
                crossovers.append(lap)
                last_lap = lap
        prev = row["a_faster"]

    return crossovers
