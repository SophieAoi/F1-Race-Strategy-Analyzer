import { COMPOUND_COLORS } from "./compoundColors";

export default function StintChart({ data }) {
  if (!data) return null;

  const { driver_order: driverOrder, stints } = data;
  const maxLap = Math.max(...stints.map((s) => s.end_lap), 1);
  const rowHeight = 28;
  const chartWidth = 700;

  const stintsByDriver = {};
  for (const stint of stints) {
    if (!stintsByDriver[stint.driver]) stintsByDriver[stint.driver] = [];
    stintsByDriver[stint.driver].push(stint);
  }

  return (
    <div style={{ overflowX: "auto" }}>
      <svg
        width={chartWidth + 60}
        height={driverOrder.length * rowHeight + 40}
        role="img"
        aria-label="Tyre strategy chart"
      >
        {driverOrder.map((driver, i) => {
          const y = i * rowHeight;
          const driverStints = stintsByDriver[driver] || [];
          return (
            <g key={driver}>
              <text x={0} y={y + rowHeight / 2 + 4} fontSize={12} fontFamily="monospace">
                {driver}
              </text>
              {driverStints.map((stint) => {
                const x = 50 + ((stint.start_lap - 1) / maxLap) * chartWidth;
                const width = ((stint.end_lap - stint.start_lap + 1) / maxLap) * chartWidth;
                return (
                  <rect
                    key={`${driver}-${stint.stint_number}`}
                    x={x}
                    y={y + 3}
                    width={width}
                    height={rowHeight - 8}
                    fill={COMPOUND_COLORS[stint.compound] || "#999"}
                    stroke="#1a1a1a"
                    strokeWidth={0.5}
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
      <div style={{ display: "flex", gap: 16, marginTop: 8, fontSize: 12 }}>
        {Object.entries(COMPOUND_COLORS).map(([compound, color]) => (
          <div key={compound} style={{ display: "flex", alignItems: "center", gap: 4 }}>
            <span
              style={{
                display: "inline-block",
                width: 12,
                height: 12,
                background: color,
                border: "1px solid #1a1a1a",
              }}
            />
            {compound}
          </div>
        ))}
      </div>
    </div>
  );
}
