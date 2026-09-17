# F1 Strategy Analyzer — Build Phases

A phased checklist for building the F1 race strategy analyzer described in the project brief. Work top to bottom — each phase produces something demoable before moving on.

## Phase 0 — Project setup ✅

- [x] `python -m venv .venv && source .venv/bin/activate`
- [x] `pip install fastf1 pandas matplotlib numpy`
- [x] `pip freeze > requirements.txt`
- [x] Create `.gitignore` (FastF1 cache dir, `.venv/`, `__pycache__/`, `.env`)
- [x] Enable FastF1 local cache: `fastf1.Cache.enable_cache('cache/')`
- [x] Sanity check: load one session end-to-end and print lap data
  ```python
  import fastf1
  fastf1.Cache.enable_cache('cache/')
  session = fastf1.get_session(2023, "Monza", "R")
  session.load()
  print(session.laps.head())
  ```
- [x] Confirm `session.laps`, `session.weather_data`, and `session.results` are all populated

## Phase 1 — Data layer (`src/data/`) ✅

- [x] `loader.py`: wrapper around `fastf1.get_session(year, gp, session_type)` + `.load()`, with cache dir configurable
- [x] `cleaning.py`: helpers to
  - [x] flag in/out laps (`Lap.PitInTime` / `PitOutTime` not null)
  - [x] flag laps under Safety Car / VSC / Red Flag (via `TrackStatus`)
  - [x] drop/flag laps with no valid `LapTime` (deleted laps, `IsAccurate == False`)
- [x] `models.py`: typed dataclasses for `Stint`, `PitStop`
- [x] Unit test: load a known race, assert lap count and pit stop count match public record for one driver

## Phase 2 — Feature 1: Stint visualization ✅

- [x] Derive stints per driver: group laps by `Stint` number, get compound + lap range per stint
- [x] Build horizontal timeline chart (matplotlib `barh`), one row per driver
  - [x] Color by compound (soft=red, medium=yellow, hard=white/grey, inter=green, wet=blue)
  - [x] Mark pit stop boundaries between stints
  - [x] Sort drivers by finishing position
- [x] Save chart as PNG for README
- [x] **Checkpoint:** this chart alone is your first shareable artifact — grab a screenshot

## Phase 3 — Feature 2: Pace degradation analysis ✅

- [x] Filter laps: exclude in/out laps, SC/VSC laps, inaccurate laps (reuse Phase 1 cleaning)
- [x] Per stint, fit trend line (linear) of `LapTime` vs. `TyreLife` (tyre age within stint)
- [x] Report degradation as seconds/lap per compound, aggregated across drivers and per-driver
- [x] Visualize: scatter of clean laps + fitted trend line, faceted by driver/stint
- [x] Sanity-check against known narratives — Monza 2023: Medium +0.023 s/lap, Hard +0.026 s/lap field-wide, consistent with a low-degradation track
- [x] **Checkpoint:** findings written up in README ("Example findings" section)

## Phase 4 — Feature 3: Race pace comparison ✅

- [x] Compute rolling average lap time (window=3) per driver across the full race
- [x] Line chart: rolling pace for 2+ selected drivers overlaid, x-axis = lap number
- [x] Annotate pit stops on the chart (vertical markers)
- [x] Identify and label "crossover" points where relative pace order flips (with min-gap noise filtering)
- [x] Wire up a CLI-style param block (`DRIVERS`, `WINDOW`) so any two drivers can be compared

## Phase 5 — Feature 4: Pit stop summary ✅

- [x] Extract pit stop events: lap, in/out time, stationary duration (from `PitInTime`/`PitOutTime` deltas)
- [x] Compute position before/after each stop (from `session.laps` position column)
- [x] Model the "pit loss" delta — estimated as (in-lap time − median clean lap) + (out-lap time − median clean lap)
- [x] Build summary table: driver, lap, duration, position change, estimated time lost
- [x] Render as a formatted table and export to CSV

## Phase 6 — Polish & README ✅

- [x] Write `README.md` with:
  - [x] Project description + motivation
  - [x] Screenshot from Phase 2 (stint chart) front and center
  - [x] Setup instructions (venv, pip install, FastF1 cache note)
  - [x] Example usage / CLI commands
  - [x] Methodology notes: how degradation is modeled, how pit delta is estimated, what filtering is applied and why
- [x] Add `requirements.txt` (finalized)
- [x] Tests for cleaning logic (Phase 1), degradation fit (Phase 3), pace (Phase 4), and pit stops (Phase 5) — 13 tests passing

---

## Stretch Phase A — Strategy "what-if" simulator ✅

- [x] Given the degradation model (Phase 3) + pit loss model (Phase 5), simulate alternate strategies for a single driver
- [x] Output: predicted total race time for the alternate strategy vs. actual
- [x] Clearly document assumptions/limitations (no traffic modeling, no safety car timing, no track position) in README
- [x] Self-consistency check: replaying the actual strategy reproduces actual race time to within ~1s
- [x] Validated on 2023 Monza: two-stop alternate correctly predicted slower than VER's actual one-stop

## Stretch Phase B — Multi-race views ✅

- [x] Loop loader across multiple rounds of a season for one driver (`summarize_driver_season`, skips events that fail to resolve rather than aborting)
- [x] Aggregate: strategy choice (stops, compounds) and average degradation per race
- [x] Simple trend chart: degradation + pit stop count across races (`src/viz/season_chart.py`)
- [x] Documented FastF1's event-name fuzzy-matching behavior and the traffic-vs-wear ambiguity in average degradation as real caveats in README

## Stretch Phase C — Web frontend

- [ ] `api/`: FastAPI app exposing endpoints for:
  - [ ] `GET /sessions?year=&event=` — list available races
  - [ ] `GET /session/{id}/stints` — stint chart data
  - [ ] `GET /session/{id}/pace?drivers=` — pace comparison data
  - [ ] `GET /session/{id}/pitstops` — pit stop table
- [ ] Cache FastF1 loads server-side to avoid re-loading per request
- [ ] `frontend/`: React app with
  - [ ] Race/session picker
  - [ ] Driver multi-select for pace comparison
  - [ ] Chart components (recharts/visx) mirroring the matplotlib outputs
- [ ] Deploy notes (even if just "run locally" for now)

---

## Suggested repo structure (already scaffolded)

```
f1-strategy-analyzer/
├── src/
│   ├── data/        # FastF1 loading, caching, cleaning
│   ├── analysis/    # degradation models, pit delta, pace calcs
│   └── viz/         # chart builders
├── api/             # FastAPI endpoints (stretch)
├── frontend/         # React app (stretch)
├── notebooks/        # exploratory analysis
├── tests/
└── README.md         # screenshots + methodology notes
```
