"""패치 노트 한글·블록 판별 규칙 (도메인 순수 로직)."""

from __future__ import annotations

from scout.app.dtos.game_detail_dto import PatchNoteDto


def is_korean_translation(note: PatchNoteDto) -> bool:
    body = (note.body_ko or "").strip()
    if not body or body.startswith("【"):
        return False
    return any("\uac00" <= c <= "\ud7a3" for c in body[:500])


def has_korean_content_blocks(note: PatchNoteDto) -> bool:
    for block in note.content_blocks:
        if block.type != "text" or not (block.text or "").strip():
            continue
        if any("\uac00" <= c <= "\ud7a3" for c in block.text[:500]):
            return True
    return False


def _korean_text_block_count(note: PatchNoteDto) -> int:
    count = 0
    for block in note.content_blocks:
        if block.type != "text" or not (block.text or "").strip():
            continue
        if any("\uac00" <= c <= "\ud7a3" for c in block.text[:500]):
            count += 1
    return count


def needs_korean_block_translation(
    note: PatchNoteDto,
    *,
    steam_note: PatchNoteDto | None = None,
    steam_has_blocks: bool = False,
) -> bool:
    has_steam_blocks = steam_has_blocks or bool(
        steam_note and steam_note.content_blocks
    )
    if not has_steam_blocks or not is_korean_translation(note):
        return False
    if not has_korean_content_blocks(note):
        return True
    if not steam_note:
        return False
    steam_text = sum(1 for b in steam_note.content_blocks if b.type == "text")
    korean_text = _korean_text_block_count(note)
    steam_images = any(b.type == "image" for b in steam_note.content_blocks)
    if steam_images and korean_text < steam_text:
        return True
    return False
