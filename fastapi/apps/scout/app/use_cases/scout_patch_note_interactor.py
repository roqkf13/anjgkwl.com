from __future__ import annotations

from scout.app.dtos.scout_patch_note_dto import ScoutPatchNoteDto
from scout.app.ports.input.scout_patch_note_use_case import ScoutPatchNoteUseCase
from scout.app.ports.output.scout_patch_note_db_repository import ScoutPatchNoteDbRepository
from scout.domain.entities.scout_patch_note_entity import ScoutPatchNoteEntity


def _to_dto(entity: ScoutPatchNoteEntity) -> ScoutPatchNoteDto:
    return ScoutPatchNoteDto(
        id=entity.id,
        game_id=entity.game_id,
        external_note_id=entity.external_note_id.value,
        source_title=entity.source_title,
        source_summary=entity.source_summary,
        source_body=entity.source_body,
        image_urls=entity.image_urls,
        published_at=entity.published_at,
        source_url=entity.source_url,
    )


class ScoutPatchNoteInteractor(ScoutPatchNoteUseCase):
    def __init__(self, repository: ScoutPatchNoteDbRepository) -> None:
        self._repository = repository

    async def get_patch_note(self, external_note_id: str) -> ScoutPatchNoteDto | None:
        entity = await self._repository.find_by_external_id(external_note_id)
        return _to_dto(entity) if entity else None
