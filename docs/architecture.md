# Crowd Guard Architecture

## End-to-End Architecture

```mermaid
flowchart LR
    subgraph Ingestion["Video Ingestion Layer"]
        CCTV["CCTV Cameras"]
        DRONE["Drone Feeds"]
        RTSP["RTSP / WebRTC Streams"]
    end

    subgraph Edge["Edge Deployment Layer"]
        GATEWAY["Raspberry Pi / Jetson / GPU Gateway"]
        PRE["Preprocessing Pipeline
        - Frame extraction
        - Noise reduction
        - Face blurring
        - Geo-fence calibration"]
        INFER["AI Inference Engine
        YOLOv8 + DeepSORT"]
        ANOM["Anomaly Classification
        Position / Movement / Appearance / Action / Affect / Unknown"]
    end

    subgraph Alerting["Alert Generation & Verification"]
        RULES["Confidence & Escalation Rules"]
        VERIFY["Human-in-the-loop Verification"]
        NOTIFY["SMS / WhatsApp / Push / Email"]
    end

    subgraph Platform["Backend & Data Services"]
        API["FastAPI REST + WebSocket API"]
        WS["/ws/alerts"]
        HEAT["Live Heatmap Service"]
        TOURIST["Blockchain Tourist ID Service"]
        STORE["Alert Store / Audit Log"]
        CLOUD["AWS S3 / Firebase Storage"]
    end

    subgraph UI["Real-Time Dashboard"]
        REACT["React.js Control Center"]
        MAP["Heatmap + Camera Views"]
        CASES["Alert Queue & Incident Timeline"]
    end

    CCTV --> GATEWAY
    DRONE --> GATEWAY
    RTSP --> GATEWAY
    GATEWAY --> PRE --> INFER --> ANOM
    ANOM --> RULES --> API
    RULES --> VERIFY
    VERIFY --> NOTIFY
    API --> WS
    API --> HEAT
    API --> TOURIST
    API --> STORE
    API --> CLOUD
    WS --> REACT
    HEAT --> MAP
    API --> CASES
    TOURIST --> REACT
```

## Processing Flow

1. Streams enter through edge gateways near camera sources.
2. Frames are sampled, denoised, and privacy protected with face anonymization.
3. YOLOv8 detects people, vehicles, and objects while DeepSORT maintains tracking IDs.
4. Anomaly engines score position, movement, appearance, action, affect, and unknown patterns.
5. Alerts are confidence-ranked, optionally operator-verified, and distributed through Twilio, push, and email.
6. Metadata, anonymized frames, and audit records are stored in backend services and cloud storage.
7. The dashboard consumes live alerts and crowd heatmaps over REST and WebSocket APIs.

## Privacy and Security

- Face blurring is applied before storage and downstream analytics.
- JWT protects authority endpoints.
- Tourist identities are hash-anchored for tamper-evident verification.
- Edge inference reduces raw video egress and improves latency.
