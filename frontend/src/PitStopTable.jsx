export default function PitStopTable({ data }) {
  if (!data) return null;

  return (
    <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 13 }}>
      <thead>
        <tr style={{ borderBottom: "2px solid #ccc", textAlign: "left" }}>
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
          <tr key={`${stop.driver}-${stop.lap}-${i}`} style={{ borderBottom: "1px solid #eee" }}>
            <td style={cellStyle}>{stop.driver}</td>
            <td style={cellStyle}>{stop.lap}</td>
            <td style={cellStyle}>{stop.stationary_s?.toFixed(2) ?? "—"}</td>
            <td style={cellStyle}>{stop.position_before ?? "—"}</td>
            <td style={cellStyle}>{stop.position_after ?? "—"}</td>
            <td style={cellStyle}>{stop.position_change ?? "—"}</td>
            <td style={cellStyle}>{stop.time_lost_s?.toFixed(2) ?? "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const cellStyle = { padding: "6px 10px" };
