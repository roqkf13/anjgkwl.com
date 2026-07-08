from scout.app.dtos.genre_hub_dto import GenreGameDto, GenreHubDto
from scout.app.ports.output.genre_hub_repository import GenreHubRepository


class SoulslikeStaticRepository(GenreHubRepository):
    """소울라이크 장르 허브용 정적 데이터 (DB 연동 전)."""

    async def get_hub(self) -> GenreHubDto:
        return GenreHubDto(
            id="soulslike",
            label="소울라이크",
            description="높은 난이도와 보스 전투 중심의 액션 RPG",
            representative_title="ELDEN RING",
            traits=["패턴 학습", "높은 난이도", "보스 중심 전투", "스태미나·회피"],
            games=[
                GenreGameDto(
                    title="ELDEN RING",
                    summary="오픈 필드와 레거던 던전이 결합된 프롬소프트 대표작.",
                    steam_app_id=1245620,
                ),
                GenreGameDto(
                    title="Dark Souls III",
                    summary="시리즈 정수를 담은 좁은 맵 기반 소울라이크.",
                    steam_app_id=374320,
                ),
                GenreGameDto(
                    title="Sekiro: Shadows Die Twice",
                    summary="패링과 자세 시스템이 핵심인 액션 중심 소울라이크.",
                    steam_app_id=814380,
                ),
            ],
        )
