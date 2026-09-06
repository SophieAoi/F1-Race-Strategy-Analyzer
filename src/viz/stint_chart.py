import matplotlib.pyplot as plt

from src.analysis.stints import extract_stints, finishing_order

COMPOUND_COLORS = {
    "SOFT": "#DA291C",
    "MEDIUM": "#FFD12E",
    "HARD": "#F0F0F0",
    "INTERMEDIATE": "#43B02A",
    "WET": "#0067AD",
}
COMPOUND_EDGE = "#1a1a1a"


def plot_stint_chart(session, ax=None):
    """Horizontal strategy chart: one row per driver, bars colored by tyre compound.

    Drivers are ordered top-to-bottom by finishing position.
    """
    stints = extract_stints(session.laps)
    order = finishing_order(session.results)

    if ax is None:
        _, ax = plt.subplots(figsize=(12, 0.4 * len(order) + 1))

    driver_y = {driver: i for i, driver in enumerate(reversed(order))}

    for stint in stints:
        if stint.driver not in driver_y:
            continue
        y = driver_y[stint.driver]
        color = COMPOUND_COLORS.get(stint.compound, "#999999")
        ax.barh(
            y,
            width=stint.length,
            left=stint.start_lap - 1,
            color=color,
            edgecolor=COMPOUND_EDGE,
            height=0.7,
        )

    ax.set_yticks(list(driver_y.values()))
    ax.set_yticklabels(list(driver_y.keys()))
    ax.set_xlabel("Lap")
    ax.set_title(
        f"{session.event['EventName']} {session.event.year} — Tyre Strategy",
        fontsize=13,
        fontweight="bold",
    )

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=color, ec=COMPOUND_EDGE)
        for color in COMPOUND_COLORS.values()
    ]
    ax.legend(
        handles,
        COMPOUND_COLORS.keys(),
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=len(COMPOUND_COLORS),
        frameon=False,
    )

    ax.set_xlim(0, session.laps["LapNumber"].max() + 1)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    return ax
