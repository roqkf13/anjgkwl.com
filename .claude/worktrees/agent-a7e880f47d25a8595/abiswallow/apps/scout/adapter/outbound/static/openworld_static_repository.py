from scout.app.dtos.genre_hub_dto import GenreGameDto, GenreHubDto
from scout.app.ports.output.genre_hub_repository import GenreHubRepository


class OpenworldStaticRepository(GenreHubRepository):
    """오픈월드 장르 허브용 정적 데이터 (DB 연동 전)."""

    async def get_hub(self) -> GenreHubDto:
        return GenreHubDto(
            id="openworld",
            label="오픈월드",
            description="넓은 맵을 자유롭게 탐험하는 세계",
            representative_title="Red Dead Redemption 2",
            traits=["자유 탐험", "사이드 콘텐츠", "몰입형 세계관", "장거리 이동"],
            games=[
                GenreGameDto(
                    title="Red Dead Redemption 2",
                    summary="서부 시대 오픈월드 서사와 생태계가 돋보이는 작품.",
                    steam_app_id=1174180,
                ),
                GenreGameDto(
                    title="The Witcher 3: Wild Hunt",
                    summary="퀘스트 밀도가 높은 판타지 오픈월드 RPG.",
                    steam_app_id=292030,
                ),
                GenreGameDto(
                    title="Ghost of Tsushima DIRECTOR'S CUT",
                    summary="사무라이 액션과 아름다운 오픈 필드 탐험.",
                    steam_app_id=2215430,
                ),
            ],
        )
