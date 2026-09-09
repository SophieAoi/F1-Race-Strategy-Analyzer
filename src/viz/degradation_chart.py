import matplotlib.pyplot as plt
import numpy as np

from src.analysis.degradation import fit_stint_degradation
from src.data.cleaning import clean_laps
from src.viz.stint_chart import COMPOUND_COLORS


def plot_driver_degradation(session, driver: str, ax=None):
    """Scatter of clean lap times vs. tyre age for one driver, with a fitted
    degradation trend line per stint."""
    laps = session.laps[session.laps["Driver"] == driver]
    clean = clean_laps(laps)
    fits = {f.stint_number: f for f in fit_stint_degradation(laps)}

    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))

    for stint_number, group in clean.groupby("Stint"):
        compound = group["Compound"].iloc[0]
        color = COMPOUND_COLORS.get(compound, "#999999")
        x = group["TyreLife"].to_numpy(dtype=float)
        y = group["LapTime"].dt.total_seconds().to_numpy()

        ax.scatter(x, y, color=color, edgecolor="#1a1a1a", label=f"Stint {int(stint_number)} ({compound})")

        fit = fits.get(stint_number)
        if fit is not None:
            xs = np.linspace(x.min(), x.max(), 20)
            ys = fit.deg_s_per_lap * xs + fit.intercept_s
            ax.plot(xs, ys, color=color, linestyle="--", linewidth=2)

    ax.set_xlabel("Tyre age (laps)")
    ax.set_ylabel("Lap time (s)")
    ax.set_title(f"{driver} — Pace Degradation by Stint\n{session.event['EventName']} {session.event.year}")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    return ax
