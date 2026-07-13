from __future__ import annotations

from community.app.dtos.content_moderation_dto import ContentModerationQuery, ContentModerationResult
from community.app.ports.input.content_moderation_use_case import ContentModerationUseCase
from community.app.ports.output.content_moderation_model_port import ContentModerationModelPort

_CLEAN_LABEL = "clean"


class ContentModerationInteractor(ContentModerationUseCase):

    def __init__(self, model: ContentModerationModelPort) -> None:
        self._model = model

    async def moderate(self, query: ContentModerationQuery) -> ContentModerationResult:
        text = " ".join(filter(None, [query.subject, query.body])).strip()
        if not text:
            return ContentModerationResult(is_clean=True, label=_CLEAN_LABEL, score=1.0)

        label, score = self._model.classify(text)
        return ContentModerationResult(is_clean=label == _CLEAN_LABEL, label=label, score=score)
