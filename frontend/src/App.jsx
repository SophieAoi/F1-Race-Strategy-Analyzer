import { useEffect, useState } from "react";
import { fetchDrivers, fetchPace, fetchPitStops, fetchSessions, fetchStints } from "./api";
import StintChart from "./StintChart";
import PaceChart from "./PaceChart";
import PitStopTable from "./PitStopTable";
import RaceCar from "./RaceCar";
import "./App.css";

const YEAR = 2023;

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [event, setEvent] = useState("");
  const [drivers, setDrivers] = useState([]);
  const [paceDrivers, setPaceDrivers] = useState([]);

  const [stintData, setStintData] = useState(null);
  const [paceData, setPaceData] = useState(null);
  const [pitData, setPitData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSessions(YEAR)
      .then((data) => {
        setSessions(data);
        if (data.length > 0) setEvent(data[0].event);
      })
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    if (!event) return;
    setError(null);
    setStintData(null);
    setPaceData(null);
    setPitData(null);

    fetchDrivers(YEAR, event)
      .then((data) => {
        setDrivers(data.drivers);
        setPaceDrivers(data.drivers.slice(0, 2));
      })
      .catch((err) => setError(err.message));

    fetchStints(YEAR, event).then(setStintData).catch((err) => setError(err.message));
    fetchPitStops(YEAR, event).then(setPitData).catch((err) => setError(err.message));
  }, [event]);

  useEffect(() => {
    if (!event || paceDrivers.length !== 2) return;
    fetchPace(YEAR, event, paceDrivers).then(setPaceData).catch((err) => setError(err.message));
  }, [event, paceDrivers]);

  return (
    <div className="app-shell">
      <header className="hero">
        <div className="hero-text">
          <p className="eyebrow">Race Engineering / Post-Race Breakdown</p>
          <h1>F1 Strategy Analyzer</h1>
          <p>Tyre strategy, pace degradation, and pit stop cost — broken down lap by lap.</p>
        </div>
        <div className="hero-car">
          <RaceCar width={300} />
        </div>
      </header>

      <div className="race-picker">
        Race ({YEAR})
        <select value={event} onChange={(e) => setEvent(e.target.value)}>
          {sessions.map((s) => (
            <option key={s.round} value={s.event}>
              {s.event}
            </option>
          ))}
        </select>
      </div>

      {error && <div className="error-banner">Error: {error}</div>}

      <section className="panel">
        <h2>Strategy</h2>
        <p className="panel-title">Tyre Strategy</p>
        {stintData ? <StintChart data={stintData} /> : <p className="loading-msg">Loading...</p>}
      </section>

      <section className="panel">
        <h2>Pace</h2>
        <p className="panel-title">Race Pace Comparison</p>
        <div className="driver-pickers">
          {[0, 1].map((slot) => (
            <label key={slot}>
              Driver {slot + 1}
              <select
                value={paceDrivers[slot] || ""}
                onChange={(e) => {
                  const next = [...paceDrivers];
                  next[slot] = e.target.value;
                  setPaceDrivers(next);
                }}
              >
                {drivers.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </label>
          ))}
        </div>
        {paceData ? <PaceChart data={paceData} /> : <p className="loading-msg">Loading...</p>}
      </section>

      <section className="panel">
        <h2>Stops</h2>
        <p className="panel-title">Pit Stops</p>
        {pitData ? <PitStopTable data={pitData} /> : <p className="loading-msg">Loading...</p>}
      </section>
    </div>
  );
}
