export function SummaryCards({ alerts }) {
  const critical = alerts.filter((alert) => alert.severity === "critical").length;
  const warning = alerts.filter((alert) => alert.severity === "warning").length;

  return (
    <section className="summary-row">
      <article className="summary-card">
        <span>Critical Events</span>
        <strong>{critical}</strong>
      </article>
      <article className="summary-card">
        <span>Warnings</span>
        <strong>{warning}</strong>
      </article>
      <article className="summary-card">
        <span>Monitored Feeds</span>
        <strong>3</strong>
      </article>
    </section>
  );
}
