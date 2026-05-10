# GLOF Sentinel Architecture

## Goal

GLOF Sentinel predicts Glacier Lake Outburst Flood risk early enough for disaster-management teams to verify field conditions, notify downstream villages, and trigger evacuation procedures.

## Data Inputs

| Signal | Example Source | Why It Matters |
| --- | --- | --- |
| Lake level | Radar or pressure gauge | Direct proxy for overtopping pressure |
| Level rise rate | Gauge derivative | Detects sudden inflow or blockage failure |
| Rainfall | Automatic weather station | Drives inflow and slope instability |
| Temperature and snowmelt | Weather station or reanalysis | Captures meltwater loading |
| Moraine stability | Ground sensors, inspections | Estimates dam-breach vulnerability |
| Seismic tremor | Local geophone | Flags ice/rockfall or moraine movement |
| Satellite NDWI delta | Sentinel/Landsat imagery | Detects lake surface expansion |
| Downstream discharge | River gauge | Validates propagation into exposed valleys |

## Runtime Flow

1. Telemetry enters the ML pipeline as `LakeSensorReading`.
2. The classifier normalizes features into comparable risk contributions.
3. Weighted risk scoring produces a 0-1 GLOF risk probability surrogate.
4. Threshold logic emits staged operational alerts with feature metadata.
5. FastAPI stores alerts in memory for the prototype and broadcasts new warnings over WebSocket.
6. React renders a basin risk map, alert feed, and command controls.

## Risk Model

The prototype intentionally uses an interpretable model so interviewers and reviewers can inspect why the system raised a warning. The risk score is a weighted sum:

- lake level: 16%
- level rise rate: 20%
- rainfall: 12%
- temperature: 8%
- snowmelt: 10%
- moraine instability: 16%
- seismic tremor: 8%
- satellite lake expansion: 5%
- downstream flow: 5%

This can be upgraded to a trained classifier once labeled GLOF and non-GLOF time series are available. The same pipeline interface can host Random Forest, XGBoost, LSTM, or temporal transformer models.

## Alert Stages

| Stage | Risk Band | Operational Meaning |
| --- | --- | --- |
| Watch | 0.55-0.67 | Increased monitoring and manual verification |
| Prepare | 0.68-0.81 | Notify field teams and ready downstream response |
| Evacuate | 0.82+ | Critical warning for evacuation and siren activation |

## Backend

The backend uses FastAPI with:

- JWT login for disaster-cell users
- `/api/stream` to register demo or real telemetry streams
- `/api/alerts` to query paginated alerts
- `/api/heatmap/live` to return basin risk-map points
- `/ws/alerts` for real-time warning delivery
- notification-service adapter methods for SMS, WhatsApp, push, email, or siren integrations

## Frontend

The React dashboard is optimized for operations:

- a compact basin command view
- live warning feed with severity and confidence
- risk map showing lake basin, moraine dam, river channel, and village exposure
- one-click demo scenario for project presentations

## Production Deployment Plan

- Ingestion: MQTT or Kafka for sensor data, scheduled satellite jobs for NDWI.
- Storage: PostgreSQL/PostGIS for lakes, settlements, sensor history, and alert audit trails.
- Model serving: versioned ML service with calibration reports and drift monitoring.
- Alert delivery: redundant SMS, siren, WhatsApp, CAP feeds, and district control-room dashboards.
- Reliability: health checks, retry queues, alert deduplication, role-based access, and incident logs.
