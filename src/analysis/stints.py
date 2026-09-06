import pandas as pd

from src.data.models import Stint


def extract_stints(laps: pd.DataFrame) -> list[Stint]:
    """Derive per-driver stints (compound + lap range) from raw lap data."""
    stints = []
    for (driver, stint_number), group in laps.groupby(["Driver", "Stint"]):
        stints.append(
            Stint(
                driver=driver,
                stint_number=int(stint_number),
                compound=group["Compound"].iloc[0],
                start_lap=int(group["LapNumber"].min()),
                end_lap=int(group["LapNumber"].max()),
            )
        )
    return stints


def finishing_order(results: pd.DataFrame) -> list[str]:
    """Driver abbreviations ordered by finishing position."""
    ordered = results.sort_values("Position")
    return ordered["Abbreviation"].tolist()
