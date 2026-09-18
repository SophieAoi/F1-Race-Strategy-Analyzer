export default function PitStopTable({ data }) {
  if (!data) return null;

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 13 }}>
        <thead>
          <tr style={headerRowStyle}>
            <th style={cellStyle}>Driver</th>
            <th style={cellStyle}>Lap</th>
            <th style={cellStyle}>Stationary (s)</th>
            <th style={cellStyle}>Pos Before</th>
            <th style={cellStyle}>Pos After</th>
            <th style={cellStyle}>Pos Change</th>
            <th style={cellStyle}>Time Lost (s)</th>
          </tr>
        </thead>
        <tbody>
          {data.stops.map((stop, i) => (
            <tr key={`${stop.driver}-${stop.lap}-${i}`} style={rowStyle}>
              <td style={{ ...cellStyle, fontWeight: 600 }}>{stop.driver}</td>
              <td style={cellStyle}>{stop.lap}</td>
              <td style={cellStyle}>{stop.stationary_s?.toFixed(2) ?? "—"}</td>
              <td style={cellStyle}>{stop.position_before ?? "—"}</td>
              <td style={cellStyle}>{stop.position_after ?? "—"}</td>
              <td style={{ ...cellStyle, color: positionChangeColor(stop.position_change) }}>
                {formatPositionChange(stop.position_change)}
              </td>
              <td style={cellStyle}>{stop.time_lost_s?.toFixed(2) ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatPositionChange(change) {
  if (change === null || change === undefined) return "—";
  if (change > 0) return `+${change}`;
  return `${change}`;
}

function positionChangeColor(change) {
  if (change === null || change === undefined) return "var(--text)";
  if (change < 0) return "#ff6b6b";
  if (change > 0) return "#4ade80";
  return "var(--text-dim)";
}

const headerRowStyle = {
  borderBottom: "2px solid var(--accent)",
  textAlign: "left",
  color: "var(--text-dim)",
  textTransform: "uppercase",
  fontSize: 11,
  letterSpacing: "0.06em",
};

const rowStyle = {
  borderBottom: "1px solid var(--border)",
  color: "var(--text)",
};

const cellStyle = { padding: "8px 12px" };
