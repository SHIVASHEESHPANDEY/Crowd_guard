export function HeatmapPanel({ points }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Basin Risk Map</h2>
        <span>Lake to valley exposure</span>
      </div>
      <div className="heatmap">
        <span className="terrain-label lake">Glacial lake</span>
        <span className="terrain-label moraine">Moraine dam</span>
        <span className="terrain-label village">Village corridor</span>
        {points.map((point, index) => (
          <span
            key={`${point.x}-${point.y}-${index}`}
            className="heat-dot"
            title={point.label ?? "Risk node"}
            style={{
              left: `${point.x * 100}%`,
              top: `${point.y * 100}%`,
              opacity: point.intensity,
              transform: `scale(${0.6 + point.intensity})`
            }}
          />
        ))}
      </div>
    </section>
  );
}
