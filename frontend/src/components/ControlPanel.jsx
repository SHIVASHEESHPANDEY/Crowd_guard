export function ControlPanel({ onStartDemo, starting, sourceStatus, error }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Monitoring Controls</h2>
        <span>{sourceStatus}</span>
      </div>
      <p className="helper-text">
        Start a basin simulation that fuses lake gauge, rainfall, snowmelt, seismic,
        satellite, and downstream flow telemetry.
      </p>
      {error ? <p className="error-text">{error}</p> : null}
      <button className="primary-btn" onClick={() => onStartDemo("monsoon_breach")} disabled={starting}>
        {starting ? "Starting simulation..." : "Start GLOF Simulation"}
      </button>
    </section>
  );
}
