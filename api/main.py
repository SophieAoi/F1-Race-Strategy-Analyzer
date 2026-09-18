import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import math

import fastf1
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.session_cache import get_cached_session
from src.analysis.pace import driver_pit_laps, driver_rolling_pace, find_crossovers
from src.analysis.pitstops import all_pit_stops, extract_pit_stops
from src.analysis.stints import extract_stints, finishing_order

app = FastAPI(title="F1 Strategy Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _load_or_404(year: int, event: str):
    try:
        return get_cached_session(year, event, "R")
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Could not load session: {exc}") from exc


@app.get("/sessions")
def list_sessions(year: int):
    """Race events available for a given season."""
    schedule = fastf1.get_event_schedule(year)
    races = schedule[schedule["RoundNumber"] > 0]
    return [
        {"round": int(row.RoundNumber), "event": row.EventName}
        for row in races.itertuples()
    ]


@app.get("/session/{year}/{event}/drivers")
def list_drivers(year: int, event: str):
    """Drivers who took part in a session, ordered by finishing position."""
    session = _load_or_404(year, event)
    order = finishing_order(session.results)
    return {"drivers": order}


@app.get("/session/{year}/{event}/stints")
def get_stints(year: int, event: str):
    """Per-driver stint data for the strategy chart, ordered by finishing position."""
    session = _load_or_404(year, event)
    stints = extract_stints(session.laps)
    order = finishing_order(session.results)

    return {
        "event": session.event["EventName"],
        "year": year,
        "driver_order": order,
        "stints": [
            {
                "driver": s.driver,
                "stint_number": s.stint_number,
                "compound": s.compound,
                "start_lap": s.start_lap,
                "end_lap": s.end_lap,
            }
            for s in stints
        ],
    }


@app.get("/session/{year}/{event}/pace")
def get_pace(year: int, event: str, drivers: str, window: int = 3):
    """Rolling-average pace comparison for a comma-separated list of drivers."""
    session = _load_or_404(year, event)
    driver_list = [d.strip().upper() for d in drivers.split(",") if d.strip()]

    if not driver_list:
        raise HTTPException(status_code=400, detail="No drivers specified")

    series = {}
    for driver in driver_list:
        pace = driver_rolling_pace(session.laps, driver, window)
        series[driver] = {
            "laps": pace["LapNumber"].tolist(),
            "rolling_pace_s": pace["RollingPace"].tolist(),
            "pit_laps": driver_pit_laps(session.laps, driver),
        }

    crossovers = []
    if len(driver_list) == 2:
        pace_a = driver_rolling_pace(session.laps, driver_list[0], window)
        pace_b = driver_rolling_pace(session.laps, driver_list[1], window)
        crossovers = find_crossovers(pace_a, pace_b)

    return {
        "event": session.event["EventName"],
        "year": year,
        "window": window,
        "series": series,
        "crossovers": crossovers,
    }


@app.get("/session/{year}/{event}/pitstops")
def get_pitstops(year: int, event: str, driver: str | None = None):
    """Pit stop summary table, optionally filtered to one driver."""
    session = _load_or_404(year, event)

    stops = extract_pit_stops(session.laps, driver.upper()) if driver else all_pit_stops(session.laps)

    return {
        "event": session.event["EventName"],
        "year": year,
        "stops": [
            {
                "driver": s.driver,
                "lap": s.lap,
                "stationary_s": None if math.isnan(s.stationary_s) else s.stationary_s,
                "position_before": s.position_before,
                "position_after": s.position_after,
                "position_change": s.position_change,
                "time_lost_s": s.time_lost_s,
            }
            for s in stops
        ],
    }
