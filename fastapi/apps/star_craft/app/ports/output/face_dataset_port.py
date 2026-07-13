from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class FaceDatasetPort(ABC):

    @abstractmethod
    def get_dataset_root_path(self) -> Path:
        pass
