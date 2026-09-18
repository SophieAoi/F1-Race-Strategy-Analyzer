import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const DRIVER_COLORS = ["#3ea6ff", "#ff3b30", "#4ade80", "#ffd12e"];
const AXIS_COLOR = "#9a9aab";
const GRID_COLOR = "#2a2a38";
const Y_AXIS_WIDTH = 80;
const MARGIN_LEFT = 16;
const MARGIN_RIGHT = 24;

export default function PaceChart({ data }) {
  if (!data) return null;

  const drivers = Object.keys(data.series);

  const lapNumbers = new Set();
  for (const driver of drivers) {
    for (const lap of data.series[driver].laps) lapNumbers.add(lap);
  }
  const sortedLaps = [...lapNumbers].sort((a, b) => a - b);

  const rows = sortedLaps.map((lap) => {
    const row = { lap };
    for (const driver of drivers) {
      const series = data.series[driver];
      const idx = series.laps.indexOf(lap);
      row[driver] = idx >= 0 ? series.rolling_pace_s[idx] : null;
    }
    return row;
  });

  return (
    <div>
      <ResponsiveContainer width="100%" height={420}>
        <LineChart
          data={rows}
          margin={{ top: 16, right: MARGIN_RIGHT, bottom: 24, left: MARGIN_LEFT }}
        >
          <CartesianGrid stroke={GRID_COLOR} strokeOpacity={0.6} vertical={false} />
          <XAxis
            dataKey="lap"
            tick={{ fill: AXIS_COLOR, fontSize: 12 }}
            stroke={GRID_COLOR}
            tickLine={false}
            label={{
              value: "Lap",
              position: "bottom",
              offset: 0,
              fill: AXIS_COLOR,
              fontSize: 12,
            }}
          />
          <YAxis
            tick={{ fill: AXIS_COLOR, fontSize: 12 }}
            stroke={GRID_COLOR}
            tickLine={false}
            width={Y_AXIS_WIDTH}
            domain={["auto", "auto"]}
            label={{
              value: `Rolling avg (s), window=${data.window}`,
              angle: -90,
              position: "left",
              offset: 8,
              style: { textAnchor: "middle" },
              fill: AXIS_COLOR,
              fontSize: 12,
            }}
          />
          <Tooltip
            contentStyle={{
              background: "#1c1c26",
              border: "1px solid #2a2a38",
              borderRadius: 8,
              color: "#f5f5f7",
              fontSize: 13,
            }}
            labelStyle={{ color: "#9a9aab" }}
          />
          {drivers.map((driver, i) => (
            <Line
              key={driver}
              type="monotone"
              dataKey={driver}
              stroke={DRIVER_COLORS[i % DRIVER_COLORS.length]}
              dot={false}
              strokeWidth={2.5}
              connectNulls
            />
          ))}
          {data.crossovers.map((lap) => (
            <ReferenceLine key={lap} x={lap} stroke="#5a5a6a" strokeDasharray="4 4" />
          ))}
        </LineChart>
      </ResponsiveContainer>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: 24,
          marginTop: 12,
          marginLeft: Y_AXIS_WIDTH + MARGIN_LEFT,
          marginRight: MARGIN_RIGHT,
          fontSize: 13,
        }}
      >
        {drivers.map((driver, i) => (
          <div key={driver} style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span
              style={{
                display: "inline-block",
                width: 14,
                height: 3,
                borderRadius: 2,
                background: DRIVER_COLORS[i % DRIVER_COLORS.length],
              }}
            />
            <span style={{ color: "var(--text)" }}>{driver}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
