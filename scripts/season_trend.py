"""Stretch Phase B: multi-race view for one driver across a season."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt

from src.analysis.season import season_summary_table, summarize_driver_season
from src.data.loader import enable_cache
from src.viz.season_chart import plot_season_trend

enable_cache("cache")

YEAR = 2023
DRIVER = "VER"
EVENTS = ["Monza", "Singapore"]

summaries = summarize_driver_season(YEAR, EVENTS, DRIVER)

print(f"\n=== {DRIVER} — {YEAR} season strategy summary ===")
print(season_summary_table(summaries).to_string(index=False))

plot_season_trend(summaries, DRIVER)

output_path = Path(__file__).resolve().parents[1] / "output" / f"season_trend_{DRIVER}_{YEAR}.png"
output_path.parent.mkdir(exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\nSaved chart to {output_path}")
