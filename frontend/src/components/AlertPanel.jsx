export function AlertPanel({ alerts }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Warning Feed</h2>
        <span>{alerts.length} active</span>
      </div>
      <div className="alert-list">
        {alerts.map((alert) => (
          <article key={alert.id} className={`alert-card severity-${alert.severity}`}>
            <div className="alert-topline">
              <strong>{alert.anomaly_type.replaceAll("_", " ")}</strong>
              <span>{Math.round(alert.confidence * 100)}%</span>
            </div>
            <p>{alert.description}</p>
            <small>
              {alert.source_name || alert.stream_id}
              {alert.metadata?.risk_score ? ` | risk ${Math.round(alert.metadata.risk_score * 100)}%` : ""}
            </small>
          </article>
        ))}
        {alerts.length === 0 ? <p className="helper-text">No warnings yet. Start the simulation to stream basin telemetry.</p> : null}
      </div>
    </section>
  );
}
