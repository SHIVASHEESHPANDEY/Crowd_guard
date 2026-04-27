export function ControlPanel({ onStartDemo, starting, sourceStatus, error }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Monitoring Controls</h2>
        <span>{sourceStatus}</span>
      </div>
      <p className="helper-text">
        Start the built-in demo stream to simulate crowd anomalies without a live CCTV feed.
      </p>
      {error ? <p className="error-text">{error}</p> : null}
      <button className="primary-btn" onClick={() => onStartDemo("panic")} disabled={starting}>
        {starting ? "Starting demo..." : "Start Demo Monitoring"}
      </button>
    </section>
  );
}
