# Resume Points

## One-Line Project Title

**GLOF Sentinel: AI-based Glacier Lake Outburst Flood Early Warning System**

## Resume Bullets

- Engineered a full-stack early warning system for Glacier Lake Outburst Floods using FastAPI, React, WebSockets, and an interpretable ML risk-scoring pipeline.
- Fused simulated lake-level, rainfall, temperature, snowmelt, moraine-stability, seismic, satellite NDWI, and downstream-flow signals to classify watch, preparation, and evacuation stages.
- Built a real-time disaster operations dashboard with JWT login, basin risk visualization, live warning feed, and demo telemetry simulation for stakeholder presentations.
- Designed the architecture for production extension with IoT sensor ingestion, Sentinel/Landsat satellite processing, PostGIS persistence, and multi-channel public alerting.

## Interview Pitch

I built GLOF Sentinel as an end-to-end disaster-risk AI project. The backend accepts telemetry streams, computes an explainable outburst risk score, and pushes warnings over WebSockets. The React dashboard lets an operator start a demo basin simulation, watch the lake-to-valley risk map update, and inspect why each alert was raised. I kept the first model interpretable because early warning systems need trust and auditability before replacing the risk score with a trained temporal model.

## Technologies To List

FastAPI, React, Vite, WebSockets, JWT, scikit-learn, Python, JavaScript, sensor fusion, risk scoring, disaster management systems
