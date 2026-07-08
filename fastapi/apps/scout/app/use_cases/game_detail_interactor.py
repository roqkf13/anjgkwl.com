import asyncio
import logging

from scout.app.dtos.game_detail_dto import (
    GameDetailDto,
    PatchContentBlockDto,
    PatchNoteDto,
)
from scout.app.ports.input.game_detail_use_case import GameDetailUseCase
from scout.app.ports.output.game_detail_repository import GameDetailRepository
from scout.app.ports.output.mod_repository import ModRepository
from scout.app.ports.output.patch_note_translator import PatchNoteTranslator
from scout.app.ports.output.patch_translation_repository import (
    PatchTranslationRepository,
)
from scout.app.ports.output.steam_news_repository import SteamNewsRepository
from scout.domain.patch_note_format import blocks_to_plain_body
from scout.domain.patch_note_rules import (
    has_korean_content_blocks,
    is_korean_translation,
    needs_korean_block_translation,
)

logger = logging.getLogger(__name__)

# steam_app_id -> note_id -> 영문 본문 (클릭 시 번역용)
_steam_body_en: dict[int, dict[str, str]] = {}


def _merge_steam_media(
    persisted: PatchNoteDto, steam_note: PatchNoteDto | None
) -> PatchNoteDto:
    if not steam_note:
        return persisted
    images = steam_note.image_urls or persisted.image_urls
    if has_korean_content_blocks(persisted):
        blocks = persisted.content_blocks
    elif is_korean_translation(persisted) and persisted.body_ko:
        blocks = _blocks_from_body_and_images(persisted.body_ko, images)
    elif steam_note.content_blocks:
        blocks = steam_note.content_blocks
    else:
        blocks = persisted.content_blocks
    return persisted.model_copy(
        update={
            "image_urls": images,
            "content_blocks": blocks,
        }
    )


def _blocks_from_body_and_images(
    body: str, image_urls: list[str]
) -> list[PatchContentBlockDto]:
    blocks: list[PatchContentBlockDto] = []
    if body.strip():
        blocks.append(PatchContentBlockDto(type="text", text=body.strip()))
    for url in image_urls:
        blocks.append(PatchContentBlockDto(type="image", url=url))
    return blocks


class GameDetailInteractor(GameDetailUseCase):
    def __init__(
        self,
        repository: GameDetailRepository,
        steam_news: SteamNewsRepository,
        patch_translator: PatchNoteTranslator,
        translation_store: PatchTranslationRepository,
        mod_repository: ModRepository,
    ) -> None:
        self._repository = repository
        self._steam_news = steam_news
        self._patch_translator = patch_translator
        self._translation_store = translation_store
        self._mod_repository = mod_repository

    async def get_game_detail(self, steam_app_id: int) -> GameDetailDto | None:
        detail = await self._repository.get_detail(steam_app_id)
        if not detail:
            return None

        steam_notes_task = asyncio.create_task(
            self._steam_news.fetch_patch_notes(steam_app_id)
        )
        mods_task = asyncio.create_task(
            self._mod_repository.fetch_mods_for_game(steam_app_id)
        )
        steam_notes, (appearance_mods, functional_mods) = await asyncio.gather(
            steam_notes_task,
            mods_task,
        )

        if steam_notes:
            raw_map: dict[str, str] = {}
            list_notes: list[PatchNoteDto] = []
            from_cache = 0
            for note in steam_notes:
                body_en = note.body_ko
                raw_map[note.id] = body_en
                persisted = self._translation_store.load(note.id)
                if persisted and is_korean_translation(persisted):
                    merged = _merge_steam_media(persisted, note)
                    if not merged.content_blocks and merged.body_ko:
                        merged = merged.model_copy(
                            update={
                                "content_blocks": _blocks_from_body_and_images(
                                    merged.body_ko, merged.image_urls
                                )
                            }
                        )
                    list_notes.append(merged.model_copy(update={"body_ko": ""}))
                    from_cache += 1
                    continue

                excerpt = (body_en or note.summary or "")[:220].strip()
                list_notes.append(
                    note.model_copy(
                        update={
                            "body_ko": "",
                            "summary": excerpt or note.summary,
                            "content_blocks": note.content_blocks,
                        }
                    )
                )

            _steam_body_en[steam_app_id] = raw_map
            detail = detail.model_copy(update={"patch_notes": list_notes})
            logger.info(
                "[GameDetailInteractor] steam notes list steam_app_id=%s "
                "count=%s summary_from_cache=%s (body on /korean)",
                steam_app_id,
                len(list_notes),
                from_cache,
            )
        else:
            fallback = self._repository.get_fallback_patch_notes(steam_app_id)
            detail = detail.model_copy(update={"patch_notes": fallback})
            logger.info(
                "[GameDetailInteractor] static fallback steam_app_id=%s count=%s",
                steam_app_id,
                len(fallback),
            )

        detail = detail.model_copy(
            update={
                "appearance_mods": appearance_mods,
                "functional_mods": functional_mods,
            }
        )
        logger.info(
            "[GameDetailInteractor] mods steam_app_id=%s "
            "appearance=%s functional=%s",
            steam_app_id,
            len(appearance_mods),
            len(functional_mods),
        )

        return detail

    async def translate_patch_note(
        self, steam_app_id: int, note_id: str
    ) -> PatchNoteDto | None:
        steam_notes = await self._steam_news.fetch_patch_notes(steam_app_id)
        base = next((n for n in steam_notes if n.id == note_id), None)

        persisted = self._translation_store.load(note_id)
        needs_block_refresh = bool(
            persisted
            and base
            and needs_korean_block_translation(persisted, steam_note=base)
        )
        if persisted and not needs_block_refresh:
            merged = _merge_steam_media(persisted, base)
            if not merged.content_blocks and merged.body_ko:
                merged = merged.model_copy(
                    update={
                        "content_blocks": _blocks_from_body_and_images(
                            merged.body_ko, merged.image_urls
                        )
                    }
                )
            return merged

        body_en = (_steam_body_en.get(steam_app_id) or {}).get(note_id)

        if base and not body_en:
            body_en = base.body_ko
            _steam_body_en.setdefault(steam_app_id, {})[note_id] = body_en

        if base and body_en:
            translated = await self._patch_translator.translate(base, body_en=body_en)
            if base.image_urls and not translated.image_urls:
                translated = translated.model_copy(
                    update={"image_urls": base.image_urls}
                )
            if translated.content_blocks and not translated.body_ko:
                translated = translated.model_copy(
                    update={"body_ko": blocks_to_plain_body(translated.content_blocks)}
                )
            if not translated.body_ko.startswith("【번역 안내】"):
                return translated
            fallback = await self._static_fallback(steam_app_id, base)
            if fallback:
                return fallback
            return translated

        detail = await self._repository.get_detail(steam_app_id)
        if not detail:
            return None
        static_note = next((n for n in detail.patch_notes if n.id == note_id), None)
        if static_note and static_note.body_ko:
            return static_note
        return None

    async def _static_fallback(
        self, steam_app_id: int, steam_note: PatchNoteDto
    ) -> PatchNoteDto | None:
        detail = await self._repository.get_detail(steam_app_id)
        if not detail or not detail.patch_notes:
            return None
        static = detail.patch_notes[0]
        if not static.body_ko or static.body_ko.startswith("【"):
            return None
        return static.model_copy(
            update={
                "id": steam_note.id,
                "title": steam_note.title,
                "published_at": steam_note.published_at,
                "source_url": steam_note.source_url or static.source_url,
                "summary": static.summary,
            }
        )
