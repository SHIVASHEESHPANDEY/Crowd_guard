# Crowd Guard Architecture

## End-to-End System Diagram

```mermaid
flowchart LR
    subgraph Ingestion["Video Ingestion Layer"]
        CCTV["CCTV Cameras"]
        DRONE["Drone Feeds"]
        RTSP["RTSP / WebRTC Streams"]
    end

    subgraph Edge["Edge Deployment Layer"]
        EDGEBOX["Raspberry Pi / Jetson / Edge GPU"]
        PRE["Preprocessing Pipeline
        - Frame extraction
        - Noise reduction
        - Face blurring
        - Geo-fence mapping"]
        INFER["AI Inference Engine
        YOLOv8 + DeepSORT"]
        ANOM["Anomaly Classification
        Position / Movement / Appearance / Action / Affect / Unknown"]
    end

    subgraph Core["Backend and Intelligence Services"]
        API["FastAPI REST API"]
        WS["WebSocket Alert Stream"]
        HEAT["Live Heatmap Service"]
        TOURIST["Digital Tourist ID Service"]
        VERIFY["Alert Verification and Escalation"]
        STORE["Alert Store and Audit Log"]
        CLOUD["AWS S3 / Firebase Storage"]
    end

    subgraph Notify["Notification System"]
        TWILIO["Twilio SMS / WhatsApp"]
        PUSH["Push Notifications"]
        EMAIL["Email Digest"]
    end

    subgraph UI["Real-Time Dashboard"]
        DASH["React.js Operations Console"]
        MAP["Density Heatmap and Camera View"]
        FEED["Incident Timeline and Alert Queue"]
    end

    CCTV --> EDGEBOX
    DRONE --> EDGEBOX
    RTSP --> EDGEBOX
    EDGEBOX --> PRE --> INFER --> ANOM
    ANOM --> API
    ANOM --> VERIFY
    API --> WS
    API --> HEAT
    API --> TOURIST
    API --> STORE
    API --> CLOUD
    VERIFY --> TWILIO
    VERIFY --> PUSH
    VERIFY --> EMAIL
    WS --> DASH
    HEAT --> MAP
    API --> FEED
    TOURIST --> DASH
```

## Runtime Flow

1. CCTV, drone, or RTSP feeds are registered through the backend.
2. Frames are extracted and anonymized with face blurring before deeper processing.
3. YOLOv8 identifies people, vehicles, and suspicious objects.
4. DeepSORT maintains object identity across frames.
5. The anomaly engine scores:
   - anomalous position
   - anomalous movement
   - anomalous appearance
   - anomalous action
   - anomalous affect
   - unknown anomaly patterns
6. Alerts are confidence-ranked, stored, broadcast to the dashboard, and passed into escalation logic.
7. Heatmap points and live alert telemetry are exposed to the React dashboard.
8. Tourist IDs can be registered and verified through a blockchain-style hashing layer.

## Privacy and Security

- Face anonymization happens before downstream analytics.
- Authority APIs use JWT authentication.
- Tourist IDs are anchored using deterministic hashing for tamper-evident verification.
- Edge-first processing reduces unnecessary raw video transfer.
- Cloud integrations should use encrypted object storage and signed-access patterns.

## Deployment Strategy

- Edge inference for low-latency monitoring
- FastAPI backend as the coordination and alerting layer
- React dashboard for command and monitoring teams
- Optional PostgreSQL, Redis, S3, Firebase, Twilio, and FCM integrations for production
