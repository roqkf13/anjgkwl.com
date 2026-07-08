from scout.app.dtos.game_detail_dto import (
    GameDetailDto,
    PatchNoteDto,
    RelatedVideoDto,
)
from scout.app.ports.output.game_detail_repository import GameDetailRepository

_KNOWN_GAMES: dict[int, str] = {
    1245620: "ELDEN RING",
    374320: "Dark Souls III",
    814380: "Sekiro: Shadows Die Twice",
    2868840: "Slay the Spire 2",
    1145360: "Hades",
    2379780: "Balatro",
    1174180: "Red Dead Redemption 2",
    292030: "The Witcher 3: Wild Hunt",
    2215430: "Ghost of Tsushima DIRECTOR'S CUT",
    367520: "Hollow Knight",
    261570: "Ori and the Blind Forest",
    774361: "Blasphemous",
}

_OFFICIAL_SITE_URL: dict[int, str] = {
    1245620: "https://en.bandainamcoent.eu/elden-ring/elden-ring",
    1145360: "https://www.supergiantgames.com/games/hades/",
    2868840: "https://www.megacrit.com/",
    2379780: "https://www.playbalatro.com/",
    367520: "https://www.hollowknight.com/",
    292030: "https://www.thewitcher.com/en/witcher3",
}


def _patch_note(
    *,
    note_id: str,
    title: str,
    published_at: str,
    summary: str,
    body_ko: str,
    source_url: str,
) -> PatchNoteDto:
    return PatchNoteDto(
        id=note_id,
        title=title,
        published_at=published_at,
        summary=summary,
        body_ko=body_ko,
        source_url=source_url,
    )


_PATCH_NOTES_KO: dict[int, list[PatchNoteDto]] = {
    2868840: [
        _patch_note(
            note_id="2868840-patch-1",
            title="5월 얼리 액세스 업데이트",
            published_at="2026-05-01",
            summary=(
                "신규 카드 12종과 유물 3종이 추가되었습니다. "
                "골드리스·하베스터 보스전 난이도를 조정했고, "
                "일부 카드 설명·키워드 툴팁을 한글화하여 수정했습니다."
            ),
            body_ko=(
                "안녕하세요, 슬레이 더 스파이어 2 플레이어 여러분.\n\n"
                "5월 얼리 액세스 업데이트가 적용되었습니다. 주요 변경 사항은 다음과 같습니다.\n\n"
                "【신규 콘텐츠】\n"
                "· 공격·스킬·파워 카드 12종 추가\n"
                "· 전투·탐험에 영향을 주는 유물 3종 추가\n\n"
                "【밸런스】\n"
                "· 골드리스·하베스터 보스전 2단계 패턴 타이밍 조정\n"
                "· 일부 카드 업그레이드 비용 소폭 하향\n\n"
                "【한글화】\n"
                "· 카드 설명·키워드(인위, 소모, 보존 등) 툴팁 문구 수정\n"
                "· 이벤트 선택지 일부 뉘앙스 보완\n\n"
                "버그 제보는 Steam 커뮤니티 또는 공식 디스코드를 이용해 주세요. "
                "즐거운 덱 빌딩 되세요!"
            ),
            source_url="https://store.steampowered.com/app/2868840/news/",
        ),
        _patch_note(
            note_id="2868840-patch-2",
            title="4월 품질 개선 패치",
            published_at="2026-04-18",
            summary=(
                "특정 유물 조합 시 데미지가 비정상적으로 적용되던 문제를 수정했습니다. "
                "맵 생성 시 이벤트 방 확률을 소폭 상향했습니다."
            ),
            body_ko=(
                "4월 품질 개선 패치가 배포되었습니다.\n\n"
                "【버그 수정】\n"
                "· 특정 유물 2개 이상 장착 시 최종 데미지가 중첩 계산되던 문제 해결\n"
                "· 보스전 종료 후 체력 회복 UI가 갱신되지 않던 현상 수정\n\n"
                "【게임플레이】\n"
                "· 맵 생성 시 ?(이벤트) 방 등장 확률 약 8% 상향\n"
                "· 상점 카드 가격 변동 폭 축소\n\n"
                "앞으로도 피드백을 보내 주시면 한글 패치 노트에 반영하겠습니다."
            ),
            source_url="https://store.steampowered.com/app/2868840/news/",
        ),
    ],
    1145360: [
        _patch_note(
            note_id="1145360-patch-1",
            title="최신 안정화 패치",
            published_at="2026-04-22",
            summary=(
                "보스전 중 대사가 겹치던 현상을 수정했습니다. "
                "한글 자막·UI 문구 오타를 정리했으며, "
                "일부 무기 대사 속도를 조정했습니다."
            ),
            body_ko=(
                "하데스 최신 안정화 패치입니다.\n\n"
                "【버그 수정】\n"
                "· 보스전 중 NPC 대사가 동시에 재생되던 문제 수정\n"
                "· 특정 방 입장 시 BGM이 끊기던 현상 해결\n\n"
                "【한글화】\n"
                "· 자막 오타 및 띄어쓰기 40여 곳 수정\n"
                "· 무기·신앙 관련 UI 용어 통일 (예: '피해' → '데미지' 표기 정리)\n\n"
                "【조정】\n"
                "· 아테나·아레스 무기 대사 재생 속도 미세 조정\n\n"
                "타르타로스에서 즐거운 러닝 되세요!"
            ),
            source_url="https://store.steampowered.com/app/1145360/news/",
        ),
    ],
    1245620: [
        _patch_note(
            note_id="1245620-patch-1",
            title="밸런스 및 버그 수정",
            published_at="2026-03-30",
            summary=(
                "특정 무기 스킬의 스태미나 소모가 의도와 다르게 적용되던 문제를 수정했습니다. "
                "협동 플레이 시 소환 표식이 보이지 않던 현상을 해결했습니다."
            ),
            body_ko=(
                "엘든 링 업데이트 1.12.3 요약입니다.\n\n"
                "【버그 수정】\n"
                "· 특정 무기 스킬 연계 시 스태미나 소모량이 잘못 적용되던 문제 수정\n"
                "· 협동 세션에서 협력자 소환 표식이 표시되지 않던 현상 해결\n"
                "· 일부 유물 효과가 PvP에서 중복 적용되던 문제 수정\n\n"
                "【밸런스】\n"
                "· 인기 PvP 무기 3종의 위력 소폭 조정 (단검·창·마법 카테고리)\n\n"
                "자세한 수치 변경은 공식 패치 노트(영문)를 참고해 주세요."
            ),
            source_url="https://store.steampowered.com/app/1245620/news/",
        ),
    ],
}


def _steam_store_url(steam_app_id: int) -> str:
    return f"https://store.steampowered.com/app/{steam_app_id}"


def _official_site_url(steam_app_id: int) -> str:
    return _OFFICIAL_SITE_URL.get(steam_app_id, _steam_store_url(steam_app_id))


def _default_patch_notes_ko(steam_app_id: int) -> list[PatchNoteDto]:
    store = _steam_store_url(steam_app_id)
    title = _KNOWN_GAMES.get(steam_app_id, "해당 게임")
    summary = (
        "밸런스 조정 및 버그 수정이 포함된 최신 빌드가 배포되었습니다. "
        "아래 본문에서 한글 요약을 확인할 수 있습니다."
    )
    body = (
        f"{title} 최신 업데이트 안내입니다.\n\n"
        "【개요】\n"
        "· 밸런스 조정 및 버그 수정이 포함된 빌드가 Steam에 배포되었습니다.\n\n"
        "【안내】\n"
        "· 상세 변경 목록은 Steam 클라이언트의 뉴스 탭에서 한글·영문 공지를 확인할 수 있습니다.\n"
        "· Scout 에는 공식 공지를 한글로 요약해 제공합니다. 원문이 필요하면 하단 링크를 이용해 주세요."
    )
    return [
        _patch_note(
            note_id=f"{steam_app_id}-patch-1",
            title="최신 업데이트",
            published_at="2026-05-01",
            summary=summary,
            body_ko=body,
            source_url=f"{store}/news/",
        ),
    ]


class GameDetailStaticRepository(GameDetailRepository):
    """게임별 패치노트·모드·영상 (외부 API 연동 전 정적 한글 데이터)."""

    def resolve_title(self, steam_app_id: int) -> str | None:
        return _KNOWN_GAMES.get(steam_app_id)

    def get_fallback_patch_notes(self, steam_app_id: int) -> list[PatchNoteDto]:
        return _PATCH_NOTES_KO.get(steam_app_id) or _default_patch_notes_ko(
            steam_app_id
        )

    async def get_detail(self, steam_app_id: int) -> GameDetailDto | None:
        title = self.resolve_title(steam_app_id)
        if not title:
            return None

        # 패치 목록은 GameDetailService 가 Steam API 로 채움 (정적 데이터는 fallback 전용)
        patch_notes: list[PatchNoteDto] = []

        return GameDetailDto(
            steam_app_id=steam_app_id,
            title=title,
            steam_store_url=_steam_store_url(steam_app_id),
            official_site_url=_official_site_url(steam_app_id),
            patch_notes=patch_notes,
            appearance_mods=[],
            functional_mods=[],
            videos=[
                RelatedVideoDto(
                    id=f"{steam_app_id}-video-1",
                    title=f"{title} 공략·하이라이트",
                    channel="Scout 큐레이션",
                    published_at="2026-04-15",
                    watch_url=(
                        "https://www.youtube.com/results?search_query="
                        + title.replace(" ", "+")
                    ),
                ),
            ],
        )
