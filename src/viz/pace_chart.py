import matplotlib.pyplot as plt

from src.analysis.pace import driver_pit_laps, driver_rolling_pace, find_crossovers

DRIVER_COLORS = ["#0067AD", "#DA291C", "#43B02A", "#FFD12E", "#8B00FF"]


def plot_pace_comparison(session, drivers: list[str], window: int = 3, ax=None):
    """Rolling-average race pace for the given drivers, with pit stops and
    pace crossovers annotated."""
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 6))

    laps = session.laps
    paces = {d: driver_rolling_pace(laps, d, window) for d in drivers}

    for i, driver in enumerate(drivers):
        color = DRIVER_COLORS[i % len(DRIVER_COLORS)]
        pace = paces[driver]
        ax.plot(pace["LapNumber"], pace["RollingPace"], label=driver, color=color, linewidth=2)

        for pit_lap in driver_pit_laps(laps, driver):
            ax.axvline(pit_lap, color=color, linestyle=":", alpha=0.5, linewidth=1)

    if len(drivers) == 2:
        crossovers = find_crossovers(paces[drivers[0]], paces[drivers[1]])
        for lap in crossovers:
            ax.axvline(lap, color="black", linestyle="--", alpha=0.6, linewidth=1.2)
            ax.text(lap, ax.get_ylim()[1], " crossover", rotation=90, va="top", fontsize=8)

    ax.set_xlabel("Lap")
    ax.set_ylabel(f"Rolling avg lap time (s), window={window}")
    ax.set_title(
        f"{session.event['EventName']} {session.event.year} — Race Pace Comparison\n"
        f"(dotted = pit stop, dashed = pace crossover)"
    )
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    plt.tight_layout()

    return ax
