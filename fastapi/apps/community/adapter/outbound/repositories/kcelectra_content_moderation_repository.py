from __future__ import annotations

from functools import lru_cache

from community.app.ports.output.content_moderation_model_port import ContentModerationModelPort

_MODEL_NAME = "smilegate-ai/kor_unsmile"


@lru_cache(maxsize=1)
def _load_pipeline():
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

    tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(_MODEL_NAME)
    return TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        device=-1,
        top_k=None,
        function_to_apply="sigmoid",
    )


class KcElectraContentModerationRepository(ContentModerationModelPort):
    """smilegate-ai/kor_unsmile(KcELECTRA 기반 파인튜닝 모델)로 욕설/혐오표현을 판별한다."""

    def classify(self, text: str) -> tuple[str, float]:
        pipe = _load_pipeline()
        scores = pipe(text[:512])[0]
        top = max(scores, key=lambda s: s["score"])
        return top["label"], top["score"]
