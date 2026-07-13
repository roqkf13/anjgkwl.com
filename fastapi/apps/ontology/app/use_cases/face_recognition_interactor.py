from __future__ import annotations

from pathlib import Path

from ultralytics import YOLO

from ontology.app.dtos.face_recognition_dto import FaceRecognitionResult
from ontology.app.ports.input.face_recognition_use_case import FaceRecognitionUseCase
from ontology.app.ports.output.face_dataset_port import FaceDatasetPort

RUNS_DIR_NAME = "yolo_train_runs"
RUN_NAME = "face_classifier"


class FaceRecognitionInteractor(FaceRecognitionUseCase):
    def __init__(self, dataset_port: FaceDatasetPort) -> None:
        self.dataset_port = dataset_port

    def _default_weights_path(self) -> Path:
        dataset_root = self.dataset_port.get_dataset_root_path()
        return dataset_root.parent / RUNS_DIR_NAME / RUN_NAME / "weights" / "best.pt"

    def train(self, epochs: int = 50, imgsz: int = 224) -> Path:
        dataset_root = self.dataset_port.get_dataset_root_path()

        model = YOLO("yolov8n-cls.pt")
        results = model.train(
            data=str(dataset_root),
            epochs=epochs,
            imgsz=imgsz,
            project=str(dataset_root.parent / RUNS_DIR_NAME),
            name=RUN_NAME,
            exist_ok=True,
        )
        return Path(results.save_dir) / "weights" / "best.pt"

    def recognize(self, image_path: Path, weights_path: Path | None = None) -> FaceRecognitionResult:
        weights_path = weights_path or self._default_weights_path()
        if not weights_path.exists():
            raise FileNotFoundError(f"학습된 가중치를 찾을 수 없음: {weights_path}. 먼저 train()을 실행하세요.")

        model = YOLO(str(weights_path))
        results = model(str(image_path))
        probs = results[0].probs
        top1_index = probs.top1
        return FaceRecognitionResult(
            name=results[0].names[top1_index],
            confidence=float(probs.top1conf),
        )
