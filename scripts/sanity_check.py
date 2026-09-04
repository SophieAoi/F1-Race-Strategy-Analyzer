"""Phase 0 sanity check: confirm FastF1 loads a session end-to-end with cache enabled."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.loader import enable_cache, load_session

enable_cache("cache")

session = load_session(2023, "Monza", "R")

print("Laps loaded:", len(session.laps))
print(session.laps.head())

print("\nWeather data rows:", len(session.weather_data))
print("Results rows:", len(session.results))
