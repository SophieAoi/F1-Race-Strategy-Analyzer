"""Phase 5: pit stop summary table for a session."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.pitstops import all_pit_stops, pit_stops_table
from src.data.loader import enable_cache, load_session

enable_cache("cache")

YEAR = 2023
EVENT = "Monza"

session = load_session(YEAR, EVENT, "R")

stops = all_pit_stops(session.laps)
table = pit_stops_table(stops)

print(f"\n=== Pit stops — {EVENT} {YEAR} ===")
print(table.to_string(index=False))

output_path = Path(__file__).resolve().parents[1] / "output" / f"pitstops_{YEAR}_{EVENT}.csv"
output_path.parent.mkdir(exist_ok=True)
table.to_csv(output_path, index=False)
print(f"\nSaved table to {output_path}")
