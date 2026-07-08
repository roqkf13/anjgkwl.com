from scout.app.dtos.genre_hub_dto import GenreGameDto, GenreHubDto
from scout.app.ports.output.genre_hub_repository import GenreHubRepository


class MetroidvaniaStaticRepository(GenreHubRepository):
    """메트로배니아 장르 허브용 정적 데이터 (DB 연동 전)."""

    async def get_hub(self) -> GenreHubDto:
        return GenreHubDto(
            id="metroidvania",
            label="메트로배니아",
            description="능력 해금으로 맵을 확장하는 탐험",
            representative_title="Hollow Knight",
            traits=["능력 게이트", "맵 백트래킹", "2D 탐험", "보스 전투"],
            games=[
                GenreGameDto(
                    title="Hollow Knight",
                    summary="넓은 2D 맵과 가스파라트풍 분위기의 대표 메트로배니아.",
                    steam_app_id=367520,
                ),
                GenreGameDto(
                    title="Ori and the Blind Forest",
                    summary="플랫폼과 스토리가 조화된 감성형 메트로배니아.",
                    steam_app_id=261570,
                ),
                GenreGameDto(
                    title="Blasphemous",
                    summary="다크 판타지 풍의 2D 액션 메트로배니아.",
                    steam_app_id=774361,
                ),
            ],
        )
