from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ontology.app.dtos.face_recognition_dto import FaceRecognitionResult


class FaceRecognitionUseCase(ABC):

    @abstractmethod
    def train(self, epochs: int = 50, imgsz: int = 224) -> Path:
        pass

    @abstractmethod
    def recognize(self, image_path: Path, weights_path: Path | None = None) -> FaceRecognitionResult:
        pass
