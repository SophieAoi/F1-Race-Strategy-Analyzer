import matplotlib.pyplot as plt

from src.analysis.season import RaceStrategySummary


def plot_season_trend(summaries: list[RaceStrategySummary], driver: str, ax=None):
    """Two-panel view: average degradation and pit stop count per race,
    across a season, for one driver."""
    if ax is None:
        _, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    else:
        axes = ax

    events = [s.event for s in summaries]
    degs = [s.avg_deg_s_per_lap for s in summaries]
    stops = [s.num_stops for s in summaries]

    axes[0].plot(events, degs, marker="o", color="#DA291C", linewidth=2)
    axes[0].set_ylabel("Avg degradation (s/lap)")
    axes[0].set_title(f"{driver} — Season Strategy Trend ({summaries[0].year})")
    axes[0].grid(alpha=0.3)

    axes[1].bar(events, stops, color="#0067AD")
    axes[1].set_ylabel("Pit stops")
    axes[1].set_xlabel("Event")
    axes[1].grid(axis="y", alpha=0.3)
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    return axes
