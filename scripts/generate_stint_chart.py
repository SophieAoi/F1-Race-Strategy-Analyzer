"""Phase 2: generate the stint/strategy chart for a given session."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt

from src.data.loader import enable_cache, load_session
from src.viz.stint_chart import plot_stint_chart

enable_cache("cache")

YEAR = 2023
EVENT = "Monza"

session = load_session(YEAR, EVENT, "R")
plot_stint_chart(session)

output_path = Path(__file__).resolve().parents[1] / "output" / f"stint_chart_{YEAR}_{EVENT}.png"
output_path.parent.mkdir(exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"Saved chart to {output_path}")
