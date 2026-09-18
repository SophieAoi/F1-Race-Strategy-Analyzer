import { COMPOUND_COLORS } from "./compoundColors";

const TEXT_COLOR = "#f5f5f7";
const AXIS_COLOR = "#9a9aab";
const GRID_COLOR = "#2a2a38";

export default function StintChart({ data }) {
  if (!data) return null;

  const { driver_order: driverOrder, stints } = data;
  const maxLap = Math.max(...stints.map((s) => s.end_lap), 1);
  const rowHeight = 28;
  const chartWidth = 660;
  const labelWidth = 56;
  const topPadding = 24;

  const stintsByDriver = {};
  for (const stint of stints) {
    if (!stintsByDriver[stint.driver]) stintsByDriver[stint.driver] = [];
    stintsByDriver[stint.driver].push(stint);
  }

  const tickStep = maxLap > 40 ? 10 : 5;
  const ticks = [];
  for (let lap = 0; lap <= maxLap; lap += tickStep) ticks.push(lap);

  return (
    <div style={{ overflowX: "auto" }}>
      <svg
        width={labelWidth + chartWidth + 16}
        height={driverOrder.length * rowHeight + topPadding + 24}
        role="img"
        aria-label="Tyre strategy chart"
        fontFamily="'Titillium Web', sans-serif"
      >
        {/* lap axis gridlines + ticks */}
        {ticks.map((lap) => {
          const x = labelWidth + (lap / maxLap) * chartWidth;
          return (
            <g key={lap}>
              <line
                x1={x}
                y1={topPadding}
                x2={x}
                y2={topPadding + driverOrder.length * rowHeight}
                stroke={GRID_COLOR}
                strokeWidth={1}
              />
              <text
                x={x}
                y={topPadding + driverOrder.length * rowHeight + 16}
                fontSize={11}
                fill={AXIS_COLOR}
                textAnchor="middle"
              >
                {lap}
              </text>
            </g>
          );
        })}

        {driverOrder.map((driver, i) => {
          const y = topPadding + i * rowHeight;
          const driverStints = stintsByDriver[driver] || [];
          return (
            <g key={driver}>
              <text
                x={0}
                y={y + rowHeight / 2 + 4}
                fontSize={12}
                fontWeight={600}
                fill={TEXT_COLOR}
              >
                {driver}
              </text>
              {driverStints.map((stint) => {
                const x = labelWidth + ((stint.start_lap - 1) / maxLap) * chartWidth;
                const width = ((stint.end_lap - stint.start_lap + 1) / maxLap) * chartWidth;
                return (
                  <rect
                    key={`${driver}-${stint.stint_number}`}
                    x={x}
                    y={y + 3}
                    width={width}
                    height={rowHeight - 8}
                    rx={2}
                    fill={COMPOUND_COLORS[stint.compound] || "#999"}
                    stroke="#0a0a0f"
                    strokeWidth={1}
                  >
                    <title>
                      {driver} — {stint.compound} (laps {stint.start_lap}-{stint.end_lap})
                    </title>
                  </rect>
                );
              })}
            </g>
          );
        })}
      </svg>
      <div style={{ display: "flex", gap: 16, marginTop: 12, fontSize: 12, flexWrap: "wrap" }}>
        {Object.entries(COMPOUND_COLORS).map(([compound, color]) => (
          <div key={compound} style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span
              style={{
                display: "inline-block",
                width: 12,
                height: 12,
                borderRadius: 3,
                background: color,
                border: "1px solid #0a0a0f",
              }}
            />
            <span style={{ color: TEXT_COLOR }}>{compound}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
