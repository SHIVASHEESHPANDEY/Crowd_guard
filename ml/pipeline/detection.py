from __future__ import annotations

from typing import Any

from ultralytics import YOLO

from ml.pipeline.types import Detection


class YOLODetector:
    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        self.model = YOLO(model_name)

    def detect(self, frame) -> list[Detection]:
        results: list[Any] = self.model.predict(frame, verbose=False)
        detections: list[Detection] = []
        for result in results:
            names = result.names
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                class_name = names[class_id]
                if class_name not in {"person", "car", "bus", "truck", "motorbike", "bicycle", "backpack", "suitcase"}:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                detections.append(
                    Detection(
                        class_name=class_name,
                        confidence=float(box.conf[0].item()),
                        bbox=(x1, y1, x2, y2),
                    )
                )
        return detections
