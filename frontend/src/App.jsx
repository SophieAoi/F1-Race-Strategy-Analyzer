import { useEffect, useState } from "react";
import { fetchDrivers, fetchPace, fetchPitStops, fetchSessions, fetchStints } from "./api";
import StintChart from "./StintChart";
import PaceChart from "./PaceChart";
import PitStopTable from "./PitStopTable";
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
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 24, fontFamily: "sans-serif" }}>
      <h1>F1 Strategy Analyzer</h1>

      <label>
        Race ({YEAR}):{" "}
        <select value={event} onChange={(e) => setEvent(e.target.value)}>
          {sessions.map((s) => (
            <option key={s.round} value={s.event}>
              {s.event}
            </option>
          ))}
        </select>
      </label>

      {error && <p style={{ color: "#c00" }}>Error: {error}</p>}

      <section>
        <h2>Tyre Strategy</h2>
        {stintData ? <StintChart data={stintData} /> : <p>Loading...</p>}
      </section>

      <section>
        <h2>Race Pace Comparison</h2>
        <div style={{ display: "flex", gap: 12, marginBottom: 8 }}>
          {[0, 1].map((slot) => (
            <label key={slot}>
              Driver {slot + 1}:{" "}
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
        {paceData ? <PaceChart data={paceData} /> : <p>Loading...</p>}
      </section>

      <section>
        <h2>Pit Stops</h2>
        {pitData ? <PitStopTable data={pitData} /> : <p>Loading...</p>}
      </section>
    </div>
  );
}
