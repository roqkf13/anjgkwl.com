"""패치 노트 블록·본문 변환 (도메인 순수 로직)."""

from scout.app.dtos.game_detail_dto import PatchContentBlockDto


def blocks_to_plain_body(blocks: list[PatchContentBlockDto]) -> str:
    parts = [b.text.strip() for b in blocks if b.type == "text" and b.text]
    return "\n\n".join(parts)
