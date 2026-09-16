from dataclasses import dataclass

import pandas as pd

from src.analysis.degradation import fit_stint_degradation
from src.analysis.stints import extract_stints
from src.data.loader import load_session


@dataclass
class RaceStrategySummary:
    year: int
    event: str
    driver: str
    num_stops: int
    compounds_used: list[str]
    avg_deg_s_per_lap: float | None
    finishing_position: int | None


def summarize_driver_race(year: int, event: str, driver: str) -> RaceStrategySummary:
    """Load one race and summarize a single driver's strategy and degradation."""
    session = load_session(year, event, "R")
    laps = session.laps[session.laps["Driver"] == driver]

    stints = extract_stints(laps)
    num_stops = max(len(stints) - 1, 0)
    compounds_used = [s.compound for s in sorted(stints, key=lambda s: s.stint_number)]

    fits = fit_stint_degradation(laps)
    avg_deg = sum(f.deg_s_per_lap for f in fits) / len(fits) if fits else None

    results = session.results
    pos_row = results[results["Abbreviation"] == driver]
    finishing_position = int(pos_row["Position"].iloc[0]) if not pos_row.empty else None

    return RaceStrategySummary(
        year=year,
        event=event,
        driver=driver,
        num_stops=num_stops,
        compounds_used=compounds_used,
        avg_deg_s_per_lap=avg_deg,
        finishing_position=finishing_position,
    )


def summarize_driver_season(year: int, events: list[str], driver: str) -> list[RaceStrategySummary]:
    """Summarize one driver's strategy across multiple rounds of a season.

    Events that fail to load (e.g. driver didn't race, data unavailable) are
    skipped rather than aborting the whole season summary.
    """
    summaries = []
    for event in events:
        try:
            summaries.append(summarize_driver_race(year, event, driver))
        except Exception as exc:
            print(f"Skipping {event} {year}: {exc}")
    return summaries


def season_summary_table(summaries: list[RaceStrategySummary]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Event": s.event,
                "Position": s.finishing_position,
                "Stops": s.num_stops,
                "Compounds": " -> ".join(s.compounds_used),
                "Avg Deg (s/lap)": round(s.avg_deg_s_per_lap, 3) if s.avg_deg_s_per_lap is not None else None,
            }
            for s in summaries
        ]
    )
