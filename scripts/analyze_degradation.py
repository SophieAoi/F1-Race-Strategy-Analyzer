"""Phase 3: pace degradation analysis for a session."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt

from src.analysis.degradation import degradation_by_compound, fit_stint_degradation
from src.data.loader import enable_cache, load_session
from src.viz.degradation_chart import plot_driver_degradation

enable_cache("cache")

YEAR = 2023
EVENT = "Monza"
DRIVER = "VER"

session = load_session(YEAR, EVENT, "R")

all_fits = fit_stint_degradation(session.laps)
by_compound = degradation_by_compound(all_fits)

print(f"\n=== Field-wide degradation by compound — {EVENT} {YEAR} ===")
print(by_compound.to_string(index=False))

driver_fits = [f for f in all_fits if f.driver == DRIVER]
print(f"\n=== {DRIVER} per-stint degradation ===")
for f in driver_fits:
    print(
        f"Stint {f.stint_number} ({f.compound}, {f.num_laps} clean laps): "
        f"{f.deg_s_per_lap:+.3f} s/lap"
    )

plot_driver_degradation(session, DRIVER)
output_path = Path(__file__).resolve().parents[1] / "output" / f"degradation_{DRIVER}_{YEAR}_{EVENT}.png"
output_path.parent.mkdir(exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\nSaved chart to {output_path}")
