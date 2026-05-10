export function HeatmapPanel({ points }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Density Heatmap</h2>
        <span>Live crowd concentration</span>
      </div>
      <div className="heatmap">
        {points.map((point, index) => (
          <span
            key={`${point.x}-${point.y}-${index}`}
            className="heat-dot"
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
