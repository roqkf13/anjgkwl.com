from scout.app.dtos.genre_hub_dto import GenreGameDto, GenreHubDto
from scout.app.ports.output.genre_hub_repository import GenreHubRepository


class RoguelikeStaticRepository(GenreHubRepository):
    """로그라이크 장르 허브용 정적 데이터 (DB 연동 전)."""

    async def get_hub(self) -> GenreHubDto:
        return GenreHubDto(
            id="roguelike",
            label="로그라이크",
            description="매 run 이 다른 랜덤 던전과 성장",
            representative_title="Slay the Spire 2",
            traits=["영구 사망", "랜덤 맵", "빌드 조합", "run 기반 성장"],
            games=[
                GenreGameDto(
                    title="Slay the Spire 2",
                    summary="카드 덱 빌딩과 roguelike run 의 후속작.",
                    steam_app_id=2868840,
                ),
                GenreGameDto(
                    title="Hades",
                    summary="스토리와 액션이 결합된 roguelike 인디 명작.",
                    steam_app_id=1145360,
                ),
                GenreGameDto(
                    title="Balatro",
                    summary="포커 핸드 조합 기반의 roguelike 덱빌더.",
                    steam_app_id=2379780,
                ),
            ],
        )
