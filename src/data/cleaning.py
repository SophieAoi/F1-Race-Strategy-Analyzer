import pandas as pd

# FastF1 TrackStatus digit codes: 1=green, 2=yellow, 4=SC, 5=red flag, 6=VSC deployed, 7=VSC ending
CLEAN_TRACK_STATUS = "1"


def flag_pit_laps(laps: pd.DataFrame) -> pd.Series:
    """True for laps where the driver pitted in or out."""
    return laps["PitInTime"].notna() | laps["PitOutTime"].notna()


def flag_caution_laps(laps: pd.DataFrame) -> pd.Series:
    """True for laps run under any non-green track status (SC/VSC/yellow/red)."""
    status = laps["TrackStatus"].astype(str)
    return status.apply(lambda s: any(c != CLEAN_TRACK_STATUS for c in s))


def flag_invalid_laps(laps: pd.DataFrame) -> pd.Series:
    """True for laps with no valid recorded time (deleted, or FastF1 marks inaccurate)."""
    return laps["LapTime"].isna() | laps["Deleted"] | ~laps["IsAccurate"]


def clean_laps(laps: pd.DataFrame) -> pd.DataFrame:
    """Return only laps suitable for pace/degradation analysis.

    Excludes pit in/out laps, caution-period laps, and laps with no valid time.
    """
    exclude = flag_pit_laps(laps) | flag_caution_laps(laps) | flag_invalid_laps(laps)
    return laps.loc[~exclude].copy()
