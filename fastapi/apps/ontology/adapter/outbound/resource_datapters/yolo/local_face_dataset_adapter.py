from __future__ import annotations

from pathlib import Path

from ontology.app.ports.output.face_dataset_port import FaceDatasetPort

DEFAULT_DATASET_ROOT = Path(__file__).resolve().parents[4] / "resources" / "yolo_train"


class LocalFaceDatasetAdapter(FaceDatasetPort):
    def __init__(self, dataset_root: Path = DEFAULT_DATASET_ROOT) -> None:
        self.dataset_root = dataset_root

    def get_dataset_root_path(self) -> Path:
        train_dir = self.dataset_root / "train"
        val_dir = self.dataset_root / "val"
        if not train_dir.is_dir() or not val_dir.is_dir():
            raise FileNotFoundError(
                f"YOLO 분류 데이터셋을 찾을 수 없음: {self.dataset_root} (train/, val/ 폴더 필요)"
            )
        return self.dataset_root
