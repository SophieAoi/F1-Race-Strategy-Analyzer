from dataclasses import dataclass

import pandas as pd

from src.data.cleaning import clean_laps


@dataclass
class PitStopSummary:
    driver: str
    lap: int
    stationary_s: float
    position_before: int | None
    position_after: int | None
    time_lost_s: float | None

    @property
    def position_change(self) -> int | None:
        if self.position_before is None or self.position_after is None:
            return None
        return self.position_before - self.position_after


def _median_clean_lap_seconds(laps: pd.DataFrame) -> float:
    clean = clean_laps(laps)
    return clean["LapTime"].dt.total_seconds().median()


def extract_pit_stops(laps: pd.DataFrame, driver: str) -> list[PitStopSummary]:
    """One entry per pit stop for a driver: lap, stationary time, position
    change, and estimated time lost vs. staying out at normal pace.

    Time lost is modeled as (in-lap time - median clean lap) + (out-lap time
    - median clean lap): the combined cost, in race time, of the slow in-lap
    and slow out-lap relative to an idealized lap where the driver just kept
    circulating at their normal pace instead of pitting.
    """
    driver_laps = laps[laps["Driver"] == driver].sort_values("LapNumber")
    baseline = _median_clean_lap_seconds(driver_laps)

    stops = []
    in_laps = driver_laps[driver_laps["PitInTime"].notna()]

    for _, in_row in in_laps.iterrows():
        lap_number = int(in_row["LapNumber"])
        out_row_df = driver_laps[driver_laps["LapNumber"] == lap_number + 1]

        stationary_s = float("nan")
        time_lost_s = None
        position_after = None

        if not out_row_df.empty:
            out_row = out_row_df.iloc[0]
            if pd.notna(out_row["PitOutTime"]):
                stationary_s = (out_row["PitOutTime"] - in_row["PitInTime"]).total_seconds()

            in_lap_s = in_row["LapTime"].total_seconds() if pd.notna(in_row["LapTime"]) else None
            out_lap_s = out_row["LapTime"].total_seconds() if pd.notna(out_row["LapTime"]) else None
            if in_lap_s is not None and out_lap_s is not None:
                time_lost_s = (in_lap_s - baseline) + (out_lap_s - baseline)

            position_after = int(out_row["Position"]) if pd.notna(out_row["Position"]) else None

        position_before = int(in_row["Position"]) if pd.notna(in_row["Position"]) else None

        stops.append(
            PitStopSummary(
                driver=driver,
                lap=lap_number,
                stationary_s=stationary_s,
                position_before=position_before,
                position_after=position_after,
                time_lost_s=time_lost_s,
            )
        )

    return stops


def all_pit_stops(laps: pd.DataFrame) -> list[PitStopSummary]:
    """Pit stop summaries for every driver in the session."""
    stops = []
    for driver in laps["Driver"].unique():
        stops.extend(extract_pit_stops(laps, driver))
    return sorted(stops, key=lambda s: (s.lap, s.driver))


def pit_stops_table(stops: list[PitStopSummary]) -> pd.DataFrame:
    """Render pit stop summaries as a flat table for display."""
    return pd.DataFrame(
        [
            {
                "Driver": s.driver,
                "Lap": s.lap,
                "Stationary (s)": round(s.stationary_s, 2) if s.stationary_s == s.stationary_s else None,
                "Pos Before": s.position_before,
                "Pos After": s.position_after,
                "Pos Change": s.position_change,
                "Time Lost (s)": round(s.time_lost_s, 2) if s.time_lost_s is not None else None,
            }
            for s in stops
        ]
    )
