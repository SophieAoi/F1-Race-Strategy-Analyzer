import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const DRIVER_COLORS = ["#0067AD", "#DA291C", "#43B02A", "#FFD12E"];

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
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={rows} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
        <CartesianGrid strokeOpacity={0.3} />
        <XAxis dataKey="lap" label={{ value: "Lap", position: "insideBottom", offset: -5 }} />
        <YAxis
          label={{ value: `Rolling avg (s), window=${data.window}`, angle: -90, position: "insideLeft" }}
          domain={["auto", "auto"]}
        />
        <Tooltip />
        <Legend />
        {drivers.map((driver, i) => (
          <Line
            key={driver}
            type="monotone"
            dataKey={driver}
            stroke={DRIVER_COLORS[i % DRIVER_COLORS.length]}
            dot={false}
            strokeWidth={2}
            connectNulls
          />
        ))}
        {data.crossovers.map((lap) => (
          <ReferenceLine key={lap} x={lap} stroke="#888" strokeDasharray="4 4" />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
