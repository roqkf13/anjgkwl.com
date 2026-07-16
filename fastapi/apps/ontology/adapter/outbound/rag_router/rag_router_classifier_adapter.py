from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from ontology.app.ports.output.rag_router_classifier_port import RagRouterClassifierPort

_MODEL_DIR = Path(__file__).resolve().parents[3] / "resources" / "rag_router" / "model"


class KlueRobertaRagRouterClassifier(RagRouterClassifierPort):
    """apps/ontology/training/train_rag_router.py로 학습한 KLUE-RoBERTa 분류기."""

    def __init__(self) -> None:
        self._tokenizer = AutoTokenizer.from_pretrained(_MODEL_DIR)
        self._model = AutoModelForSequenceClassification.from_pretrained(_MODEL_DIR)
        self._model.eval()

    def classify(self, text: str) -> tuple[str, float]:
        inputs = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=64)
        with torch.no_grad():
            logits = self._model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
        pred_id = int(probs.argmax())
        label = self._model.config.id2label[pred_id]
        return label, float(probs[pred_id])


@lru_cache
def get_rag_router_classifier() -> RagRouterClassifierPort:
    """모델은 프로세스당 한 번만 로드한다."""
    return KlueRobertaRagRouterClassifier()
