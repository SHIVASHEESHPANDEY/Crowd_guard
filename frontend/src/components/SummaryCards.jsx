export function SummaryCards({ alerts }) {
  const critical = alerts.filter((alert) => alert.severity === "critical").length;
  const warning = alerts.filter((alert) => alert.severity === "warning").length;

  return (
    <section className="summary-row">
      <article className="summary-card">
        <span>Evacuation Alerts</span>
        <strong>{critical}</strong>
      </article>
      <article className="summary-card">
        <span>Watch Warnings</span>
        <strong>{warning}</strong>
      </article>
      <article className="summary-card">
        <span>Sensor Groups</span>
        <strong>5</strong>
      </article>
    </section>
  );
}
