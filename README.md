# Crowd Guard

Crowd Guard is an AI-powered crowd anomaly detection platform for tourist and street safety. It combines privacy-first video preprocessing, object detection and tracking, anomaly classification, authority alerting, and a live React command dashboard.

## What This Repo Contains

- `backend/` - FastAPI backend for streams, alerts, tourist IDs, heatmap data, auth, and WebSocket delivery
- `ml/` - inference pipeline, demo simulation, preprocessing, detection, tracking, and anomaly scoring
- `frontend/` - React dashboard for live crowd monitoring
- `docs/architecture.md` - full architecture and deployment design

## Core Capabilities

- Real-time crowd anomaly detection
- Face anonymization before downstream analytics
- YOLOv8 + DeepSORT pipeline structure for real streams
- Demo simulation mode for local presentations
- Digital tourist ID registration and verification with blockchain-style hashing
- Live alert feed, heatmap visualization, and escalation workflow
- Notification adapter hooks for SMS, WhatsApp, push, and email

## Quick Start

### Backend

```bash
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Prototype Login

- Username: `admin`
- Password: `crowdguard123`

## Demo Workflow

1. Start the backend from `backend/`.
2. Start the frontend from `frontend/`.
3. Sign in using the prototype authority credentials.
4. Click `Start Demo Monitoring`.
5. Watch the heatmap, live alerts, and dashboard summaries update automatically.

## Current Runtime Modes

- `demo` mode: runs a built-in simulated crowd safety scenario for quick demos
- `cctv` / `drone` / `rtsp` mode: uses the same API contracts and ML pipeline structure for real streams

## Notes

- The backend stores data in memory for the prototype.
- Notification services are structured as adapters and can be connected to Twilio, Firebase, SES, or other providers.
- Tourist identity verification uses deterministic hashing as a blockchain integration placeholder.
