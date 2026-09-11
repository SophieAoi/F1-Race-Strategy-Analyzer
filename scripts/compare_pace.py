"""Phase 4: race pace comparison for selected drivers, with a CLI-style param block."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt

from src.analysis.pace import driver_rolling_pace, find_crossovers
from src.data.loader import enable_cache, load_session
from src.viz.pace_chart import plot_pace_comparison

enable_cache("cache")

YEAR = 2023
EVENT = "Monza"
DRIVERS = ["VER", "PER"]
WINDOW = 3

session = load_session(YEAR, EVENT, "R")

if len(DRIVERS) == 2:
    pace_a = driver_rolling_pace(session.laps, DRIVERS[0], WINDOW)
    pace_b = driver_rolling_pace(session.laps, DRIVERS[1], WINDOW)
    crossovers = find_crossovers(pace_a, pace_b)
    print(f"Pace crossovers between {DRIVERS[0]} and {DRIVERS[1]}: laps {crossovers}")

plot_pace_comparison(session, DRIVERS, WINDOW)

output_path = (
    Path(__file__).resolve().parents[1]
    / "output"
    / f"pace_{'_'.join(DRIVERS)}_{YEAR}_{EVENT}.png"
)
output_path.parent.mkdir(exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"Saved chart to {output_path}")
