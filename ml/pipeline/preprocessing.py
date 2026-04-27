from __future__ import annotations

import cv2
import numpy as np


class VideoPreprocessor:
    def __init__(self, face_detector_path: str | None = None) -> None:
        self.face_cascade = cv2.CascadeClassifier(
            face_detector_path or cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def extract_frames(self, source: str | None, sample_rate: int = 5):
        capture = cv2.VideoCapture(0 if source is None else source)
        index = 0
        while capture.isOpened():
            ok, frame = capture.read()
            if not ok:
                break
            if index % sample_rate == 0:
                yield index, self.prepare_frame(frame)
            index += 1
        capture.release()

    def prepare_frame(self, frame: np.ndarray) -> np.ndarray:
        denoised = cv2.GaussianBlur(frame, (5, 5), sigmaX=0)
        anonymized = self.blur_faces(denoised)
        return anonymized

    def blur_faces(self, frame: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        result = frame.copy()
        for (x, y, w, h) in faces:
            face_region = result[y:y + h, x:x + w]
            if face_region.size == 0:
                continue
            blurred = cv2.GaussianBlur(face_region, (35, 35), sigmaX=30)
            result[y:y + h, x:x + w] = blurred
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 0), 2)
        return result
