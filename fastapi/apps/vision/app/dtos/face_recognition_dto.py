from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FaceRecognitionResult:
    name: str
    confidence: float
