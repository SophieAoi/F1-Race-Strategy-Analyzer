# F1 Strategy Analyzer — Build Phases

A phased checklist for building the F1 race strategy analyzer described in the project brief. Work top to bottom — each phase produces something demoable before moving on.

## Phase 0 — Project setup

- [ ] `python -m venv .venv && source .venv/bin/activate`
- [ ] `pip install fastf1 pandas matplotlib numpy`
- [ ] `pip freeze > requirements.txt`
- [ ] Create `.gitignore` (FastF1 cache dir, `.venv/`, `__pycache__/`, `.env`)
- [ ] Enable FastF1 local cache: `fastf1.Cache.enable_cache('cache/')`
- [ ] Sanity check: load one session end-to-end and print lap data
  ```python
  import fastf1
  fastf1.Cache.enable_cache('cache/')
  session = fastf1.get_session(2023, "Monza", "R")
  session.load()
  print(session.laps.head())
  ```
- [ ] Confirm `session.laps`, `session.weather_data`, and `session.results` are all populated

## Phase 1 — Data layer (`src/data/`)

- [ ] `loader.py`: wrapper around `fastf1.get_session(year, gp, session_type)` + `.load()`, with cache dir configurable
- [ ] `cleaning.py`: helpers to
  - [ ] flag in/out laps (`Lap.PitInTime` / `PitOutTime` not null)
  - [ ] flag laps under Safety Car / VSC / Red Flag (via `TrackStatus`)
  - [ ] drop/flag laps with no valid `LapTime` (deleted laps, `IsAccurate == False`)
- [ ] `models.py` (optional): typed dataclasses/pydantic models for `Stint`, `PitStop`, `Lap` if you want cleaner interfaces than raw DataFrames
- [ ] Unit test: load a known race, assert lap count and pit stop count match public record for one driver

## Phase 2 — Feature 1: Stint visualization

- [ ] Derive stints per driver: group laps by `Stint` number, get compound + lap range per stint
- [ ] Build horizontal timeline chart (matplotlib `barh`), one row per driver
  - [ ] Color by compound (soft=red, medium=yellow, hard=white/grey, inter=green, wet=blue)
  - [ ] Mark pit stop boundaries between stints
  - [ ] Sort drivers by finishing position
- [ ] Save chart as PNG for README
- [ ] **Checkpoint:** this chart alone is your first shareable artifact — grab a screenshot

## Phase 3 — Feature 2: Pace degradation analysis

- [ ] Filter laps: exclude in/out laps, SC/VSC laps, inaccurate laps (reuse Phase 1 cleaning)
- [ ] Per stint, fit trend line (linear first, quadratic optional) of `LapTime` vs. `LapNumber within stint`
- [ ] Report degradation as seconds/lap per compound, aggregated across drivers and per-driver
- [ ] Visualize: scatter of clean laps + fitted trend line, faceted by compound or by driver
- [ ] Sanity-check against known narratives (e.g. "softs degrade faster than hards") to validate the filtering logic is actually working
- [ ] **Checkpoint:** write down 2-3 sentences of findings for a specific race — this is the "real learning" the brief calls out

## Phase 4 — Feature 3: Race pace comparison

- [ ] Compute rolling average lap time (e.g. window=3) per driver across the full race
- [ ] Line chart: rolling pace for 2+ selected drivers overlaid, x-axis = lap number
- [ ] Annotate pit stops on the chart (vertical markers or shaded bands)
- [ ] Identify and label "crossover" points where relative pace order flips
- [ ] Wire up a simple CLI or notebook param so any two drivers can be compared

## Phase 5 — Feature 4: Pit stop summary

- [ ] Extract pit stop events: lap, in/out time, stationary duration (from `PitInTime`/`PitOutTime` deltas)
- [ ] Compute position before/after each stop (delta from `session.laps` position column)
- [ ] Model the "pit loss" delta — track-specific baseline time lost vs. staying out (research typical pit lane time loss for the circuit, or estimate from the field's out-lap vs. in-lap pace)
- [ ] Build summary table: driver, lap, duration, position change, estimated time lost
- [ ] Render as a formatted table (pandas `to_markdown()` or a simple HTML table)

## Phase 6 — Polish & README

- [ ] Write `README.md` with:
  - [ ] Project description + motivation
  - [ ] Screenshot from Phase 2 (stint chart) front and center
  - [ ] Setup instructions (venv, pip install, FastF1 cache note)
  - [ ] Example usage / CLI commands
  - [ ] Methodology notes: how degradation is modeled, how pit delta is estimated, what filtering is applied and why
- [ ] Add `requirements.txt` (finalized)
- [ ] Basic tests for cleaning logic (Phase 1) and degradation fit (Phase 3)

---

## Stretch Phase A — Strategy "what-if" simulator

- [ ] Given the degradation model (Phase 3) + pit loss model (Phase 5), simulate alternate strategies (e.g. 1-stop vs actual 2-stop) for a single driver
- [ ] Output: predicted total race time for the alternate strategy vs. actual
- [ ] Clearly document assumptions/limitations (no traffic modeling, no safety car timing, etc.) — this is what makes it credible rather than hand-wavy

## Stretch Phase B — Multi-race views

- [ ] Loop loader across multiple rounds of a season for one driver
- [ ] Aggregate: strategy choice per race, average degradation per compound across the season
- [ ] Simple trend chart: how a driver's tire management evolved race-over-race

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
