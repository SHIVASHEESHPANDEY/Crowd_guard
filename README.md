# Crowd Guard

Crowd Guard is an end-to-end AI-powered crowd anomaly detection platform for tourist and street safety.

## Project Structure

- `docs/architecture.md` - system architecture and deployment strategy
- `backend/` - FastAPI backend
- `ml/` - AI pipeline modules
- `frontend/` - React dashboard scaffold

## Quick Start

### Backend

```bash
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

If `python` is not available on PATH in your environment, use the Windows launcher form such as `py -m pip install -r requirements.txt`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Default authority credentials for the prototype login flow:

- Username: `admin`
- Password: `crowdguard123`

## Demo Workflow

1. Start the backend from `backend/`.
2. Start the frontend from `frontend/`.
3. Open the dashboard and sign in with the prototype authority credentials.
4. Click `Start Demo Monitoring`.
5. The dashboard will populate with a live heatmap immediately and begin receiving simulated anomaly alerts.

## Current Working Modes

- `demo` mode: fully runnable without a live CCTV feed, designed for project demonstrations and review panels
- `cctv` / `rtsp` mode: uses the same APIs and pipeline structure, with YOLOv8 and DeepSORT activated when a real stream source is provided

## Notes

- The ML pipeline is organized for YOLOv8, DeepSORT, and anomaly scoring.
- Data persistence is in-memory by default for easy prototyping.
- Tourist identity anchoring uses a blockchain adapter pattern with deterministic hashing.
