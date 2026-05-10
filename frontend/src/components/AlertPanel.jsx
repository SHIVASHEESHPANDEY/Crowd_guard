export function AlertPanel({ alerts }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Live Alerts</h2>
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
            <small>{alert.source_name || alert.stream_id}</small>
          </article>
        ))}
        {alerts.length === 0 ? (
          <p className="helper-text">No alerts yet. Start the demo monitoring flow to simulate crowd anomalies.</p>
        ) : null}
      </div>
    </section>
  );
}
