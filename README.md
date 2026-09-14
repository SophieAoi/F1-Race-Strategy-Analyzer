# F1 Strategy Analyzer

A tool that takes any completed Formula 1 Grand Prix and breaks down what actually happened strategically — who pitted when, which tyre strategies worked, and how each driver's pace evolved over the race. It answers questions like *"why did Verstappen pull away from Pérez despite similar early pace?"*

![Tyre strategy chart — 2023 Italian Grand Prix](output/stint_chart_2023_Monza.png)

*Every driver's tyre strategy for the 2023 Italian Grand Prix — stint length and compound at a glance.*

## What it does

Given a year, event, and session, the analyzer pulls full lap-by-lap data via [FastF1](https://github.com/theOehrly/Fast-F1) and produces:

1. **Stint visualization** — a strategy chart (above) showing every driver's tyre compounds, stint lengths, and pit stops.
2. **Pace degradation analysis** — fits a linear trend to clean laps within each stint to estimate tyre degradation in seconds/lap, per compound and per driver.
3. **Race pace comparison** — rolling-average lap time between two or more drivers, with pit stops and pace "crossovers" (where the faster driver flips) annotated.
4. **Pit stop summary** — a table of every stop: stationary time, position gained/lost, and estimated race-time cost relative to staying out.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

FastF1 caches session data locally after the first download, so re-running an analysis on the same race is fast and works offline. The cache directory (`cache/`) is gitignored — it's rebuilt automatically on first use and can grow to 100MB+ per race.

## Usage

Each core feature has a standalone script under `scripts/`. Edit the `YEAR` / `EVENT` / `DRIVERS` constants at the top of a script to point it at a different race:

```bash
python3 scripts/generate_stint_chart.py      # strategy chart -> output/stint_chart_<year>_<event>.png
python3 scripts/analyze_degradation.py       # degradation chart + printed summary
python3 scripts/compare_pace.py              # pace comparison chart + crossover laps
python3 scripts/pit_stop_summary.py          # pit stop table -> output/pitstops_<year>_<event>.csv
```

Run the test suite (uses the same cached session data):

```bash
python3 -m pytest tests/ -v
```

## Methodology notes

**Lap cleaning.** Degradation and pace analysis both need to exclude laps that don't reflect genuine pace: pit in/out laps, laps run under Safety Car / VSC / yellow flags (detected via FastF1's `TrackStatus` codes, which concatenate every status active during the lap), and laps FastF1 itself flags as inaccurate or deleted. This filtering (`src/data/cleaning.py`) is applied before any trend fitting — skipping it produces wildly wrong degradation numbers, since an in-lap or SC lap can be 10-20+ seconds off normal pace and dominates a small least-squares fit.

**Degradation model.** For each stint, lap time (seconds) is fit linearly against `TyreLife` (laps on that set of tyres) using clean laps only. Stints with fewer than 3 clean laps are skipped — not enough points for a meaningful trend. The slope is the estimated degradation in seconds/lap. This is a simple model: it doesn't account for fuel load (which decreases lap time as the race goes on, partially offsetting tyre wear) or track evolution, so absolute degradation numbers should be read as relative comparisons between compounds/drivers rather than precise physical wear rates.

**Race pace comparison.** Unlike the degradation model, this intentionally keeps Safety Car laps in the rolling average — the goal is to show what actually happened on track (who was managing tyres, who was pushing), not idealized clean-air pace. Only pit in/out laps are dropped, since their length is dominated by pit lane transit rather than pace. "Crossover" points (where the faster driver switches) are filtered with a minimum lap gap between crossovers — without it, a short rolling window produces rapid, meaningless flips when two drivers are running near-identical pace.

**Pit stop time loss.** Stationary time comes directly from `PitOutTime - PitInTime`. The more interesting number — time lost relative to staying out — is modeled as `(in-lap time - median clean lap time) + (out-lap time - median clean lap time)`: the combined cost, in race time, of the slow in-lap and slow out-lap versus an idealized lap where the driver just kept circulating at normal pace. This captures more than the raw pit lane delta (which undercounts the entry/exit pace loss) without requiring a full physics model of pit lane speed limits.

**Edge cases.** A driver who retires mid-pit-stop (see OCO, 2023 Monza, lap 39) has an in-lap but no out-lap — `position_after` and `time_lost_s` correctly come back as `None` rather than a fabricated value. A driver marked "Did Not Start" (see TSU, same race) has zero laps and renders as an empty row on the stint chart rather than being dropped silently.

## Example findings — 2023 Italian Grand Prix

- **Degradation was low across the board**: Medium averaged +0.023 s/lap, Hard +0.026 s/lap field-wide — consistent with Monza's low-abrasion surface and why most of the field ran a single stop.
- **Pit stops cost ~24-26s** of race time for most drivers (Monza has one of the shortest pit lanes on the calendar); Piastri's lap-41 stop was a clear outlier at ~34s lost.
- **VER vs. PER pace comparison** shows six genuine lead changes in relative pace across the race, with Verstappen fading on old hards in the final laps while Pérez — who pitted a lap later — held stronger late pace.

## Project structure

```
f1-strategy-analyzer/
├── src/
│   ├── data/        # FastF1 loading, caching, lap cleaning
│   ├── analysis/    # degradation model, pace calcs, pit stop modeling
│   └── viz/         # chart builders (stint, degradation, pace)
├── scripts/         # runnable entry points for each analysis
├── tests/           # pytest suite, validated against real race data
├── output/          # generated charts and tables
└── requirements.txt
```

## Roadmap

- [ ] **Strategy "what-if"** — use the degradation + pit loss models to estimate whether an alternate strategy (e.g. one-stop vs. the actual two-stop) would have been faster.
- [ ] **Multi-race views** — track how a driver's strategy and tyre management evolve across a season.
- [ ] **Web frontend** — FastAPI + React app with race/driver pickers, wrapping the existing analysis modules.
