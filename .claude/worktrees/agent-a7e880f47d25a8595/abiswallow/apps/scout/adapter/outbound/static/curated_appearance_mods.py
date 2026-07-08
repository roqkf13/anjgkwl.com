"""게임별 큐레이션 외형 모드 (Nexus/Workshop 미등록·수동 수집).

steam_app_id 로만 조회 — 다른 게임 모드가 섞이지 않도록 한다.
"""

from __future__ import annotations

from scout.app.dtos.game_detail_dto import ModDto

_ALL_STS2_CHARACTERS = [
    "ironclad",
    "silent",
    "regent",
    "defect",
    "necrobinder",
]

# STS2(2868840) — 5인 로스터 외형 모드
_STS2_APPEARANCE: list[ModDto] = [
    # --- 리젠트 ---
    ModDto(
        id="2868840-curated-nexus-344",
        mod_kind="appearance",
        name="Regent Cards Anime Rework",
        author="DoublePigeon",
        summary="리젠트 카드 일러스트를 애니메 스타일로 교체하는 외형 모드.",
        characters=["regent"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/344",
    ),
    ModDto(
        id="2868840-curated-nexus-760",
        mod_kind="appearance",
        name="Card Portraits - Regent",
        author="Hatk",
        summary="리젠트 카드 초상화를 애니메 스타일 아트로 교체합니다.",
        characters=["regent"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/760",
    ),
    ModDto(
        id="2868840-curated-regent-skin-anaertailin",
        mod_kind="appearance",
        name="Regent Skin Mod",
        author="anaertailin",
        summary=(
            "리젠트 캐릭터 스킨 변경 모드. Nexus/Workshop 미등록 — "
            "Patreon에서 다운로드. Sts2SkinManager와 함께 쓰는 경우가 많습니다."
        ),
        characters=["regent"],
        source="curated",
        source_url="https://www.patreon.com/posts/sts2-regentskin-152923743",
    ),
    ModDto(
        id="2868840-curated-nexus-princess-icons",
        mod_kind="appearance",
        name="Princess Regent and Silent Icons and Text",
        author="커뮤니티",
        characters=["regent", "silent"],
        summary=(
            "캐릭터 선택·전투 UI 아이콘·대사를 여성형 톤으로 맞춘 외형 보조 모드. "
            "anaertailin 리젠트 스킨과 함께 쓰는 경우가 많습니다."
        ),
        source="nexus",
        source_url=(
            "https://www.nexusmods.com/slaythespire2/mods/"
            "?keyword=Princess+Regent+and+Silent+Icons+and+Text"
        ),
    ),
    # --- 사일런트 ---
    ModDto(
        id="2868840-curated-silent-skin-anaertailin",
        mod_kind="appearance",
        name="Silent Appearance Mod",
        author="anaertailin",
        summary="사일런트 캐릭터 외형 변경 모드. Patreon 게시글에서 다운로드.",
        characters=["silent"],
        source="curated",
        source_url="https://www.patreon.com/posts/sts2-silent-skin-154478527",
    ),
    ModDto(
        id="2868840-curated-nexus-1052",
        mod_kind="appearance",
        name="Chaos Zero Nightmare - Tressa (Silent Skin)",
        author="PelleasWorks",
        summary="사일런트를 CZN 트레사 비주얼·보이스·전투 연출 스킨으로 교체합니다.",
        characters=["silent"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/1052",
    ),
    # --- 아이언클래드 ---
    ModDto(
        id="2868840-curated-nexus-854",
        mod_kind="appearance",
        name="Ironclad Skin - Crimson Blade Valkyrie",
        author="OLC and ATA",
        summary="아이언클래드 스킨·카드 아트를 애니메 스타일 발키리 디자인으로 교체합니다.",
        characters=["ironclad"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/854",
    ),
    ModDto(
        id="2868840-curated-nexus-848",
        mod_kind="appearance",
        name="Red Mist",
        author="hasoro",
        summary="아이언클래드 Red Mist(라이브러리 오브 루이나) 스킨 모드.",
        characters=["ironclad"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/848",
    ),
    ModDto(
        id="2868840-curated-nexus-914",
        mod_kind="appearance",
        name="Chaos Zero Nightmare - Chizuru (Ironclad Skin)",
        author="PelleasWorks",
        summary="아이언클래드를 CZN 치즈루 비주얼·보이스·전투 연출 스킨으로 교체합니다.",
        characters=["ironclad"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/914",
    ),
    ModDto(
        id="2868840-curated-nexus-875",
        mod_kind="appearance",
        name="STS2 FSF Richard as Ironclad",
        author="커뮤니티",
        summary="아이언클래드를 Fate/Strange Fake 리처드 외형으로 교체하는 스킨 모드.",
        characters=["ironclad"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/875",
    ),
    # --- 디펙트 ---
    ModDto(
        id="2868840-curated-nexus-769",
        mod_kind="appearance",
        name="Anime Defect Skin Mod",
        author="Painttist",
        summary="디펙트 전투 모델·애니메이션·캐릭터 선택 화면을 애니메 스타일로 리디자인합니다.",
        characters=["defect"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/769",
    ),
    ModDto(
        id="2868840-curated-nexus-719",
        mod_kind="appearance",
        name="SaYi_998 Librarian - Defect Replacement",
        author="dzycdz",
        summary="디펙트 카드 아트·애니메이션을 SaYi_998 사서 로봇 테마로 교체합니다.",
        characters=["defect"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/719",
    ),
    # --- 네크로바인더 ---
    ModDto(
        id="2868840-curated-nexus-858",
        mod_kind="appearance",
        name="Booba Necrobinder Mod",
        author="Team JCI",
        summary=(
            "네크로바인더 전투·상점·휴식처·캐릭터 선택 아트 등 비주얼을 "
            "커스텀 외형으로 교체하는 스킨 모드."
        ),
        characters=["necrobinder"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/858",
    ),
    ModDto(
        id="2868840-curated-nexus-hatk-necrobinder",
        mod_kind="appearance",
        name="Card Portraits - Necrobinder",
        author="Hatk",
        summary="네크로바인더 카드 초상화를 애니메 스타일 아트로 교체합니다.",
        characters=["necrobinder"],
        source="nexus",
        source_url=(
            "https://www.nexusmods.com/slaythespire2/mods/"
            "?keyword=Card+Portraits+Necrobinder+Hatk"
        ),
    ),
    ModDto(
        id="2868840-curated-nexus-vaalmonica-necrobinder",
        mod_kind="appearance",
        name="Necrobinder Visuals - Vaalmonica",
        author="커뮤니티",
        summary="네크로바인더 외형을 유희왕 바알모니카 캐릭터 테마로 교체하는 비주얼 모드.",
        characters=["necrobinder"],
        source="nexus",
        source_url=(
            "https://www.nexusmods.com/slaythespire2/mods/"
            "?keyword=Vaalmonica+Necrobinder"
        ),
    ),
    ModDto(
        id="2868840-curated-nexus-623",
        mod_kind="appearance",
        name="Castorice (Necrobinder) Card Portraits",
        author="airvince",
        summary=(
            "네크로바인더 카드 초상화 90장을 붕괴: 스타레일 카스토리스 테마로 교체. "
            "xumoge3723 캐릭터 스킨과 함께 쓰는 경우가 많습니다."
        ),
        characters=["necrobinder"],
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/623",
    ),
    # --- 비공식 인기 (디시·Patreon·GitHub) ---
    ModDto(
        id="2868840-curated-regent-mesugaki",
        mod_kind="appearance",
        name="Mesugaki Regent Skin",
        author="커뮤니티",
        summary=(
            "리젠트 외형을 메스가키 톤으로 바꾸는 비공식 스킨. "
            "anaertailin 리젠트 스킨과 둘 중 하나만 설치 (동시 설치 시 충돌)."
        ),
        characters=["regent"],
        source="nexus",
        source_url=(
            "https://www.nexusmods.com/slaythespire2/mods/"
            "?keyword=Mesugaki+Regent+skin+mode"
        ),
    ),
    ModDto(
        id="2868840-curated-ironclad-anaertailin",
        mod_kind="appearance",
        name="Ironclad Skin Mod",
        author="anaertailin",
        summary=(
            "아이언클래드 캐릭터 스킨 변경 모드. Nexus/Workshop 미등록 — "
            "Patreon에서 다운로드."
        ),
        characters=["ironclad"],
        source="curated",
        source_url="https://www.patreon.com/posts/sts2-ironclad-152617854",
    ),
    ModDto(
        id="2868840-curated-necrobinder-anaertailin",
        mod_kind="appearance",
        name="Necrobinder Skin Mod",
        author="anaertailin",
        summary=(
            "네크로바인더 캐릭터 스킨 변경 모드. Patreon 게시글에서 다운로드. "
            "Princess Icons 모드와 함께 쓰는 경우가 많습니다."
        ),
        characters=["necrobinder"],
        source="curated",
        source_url="https://www.patreon.com/posts/sts2-0-8-156971990",
    ),
    ModDto(
        id="2868840-curated-defect-community",
        mod_kind="appearance",
        name="Defect Skin (커뮤니티 포팅)",
        author="커뮤니티",
        summary=(
            "디펙트 외형을 커뮤니티 제작 스킨으로 교체하는 비공식 모드. "
            "디시 모음글의 Google Drive 링크에서 배포."
        ),
        characters=["defect"],
        source="curated",
        source_url="https://m.dcinside.com/board/slay/333106",
    ),
    ModDto(
        id="2868840-curated-github-merchant2cute",
        mod_kind="appearance",
        name="Merchant2Cute",
        author="LinXce",
        summary=(
            "상인·가짜 상인 NPC 외형을 귀여운 여성형 비주얼로 교체. "
            "GitHub 릴리스 또는 Nexus #814. 압축 변형 중 하나만 설치."
        ),
        characters=["other"],
        source="github",
        source_url="https://github.com/LinXce/merchant-2-cute/releases",
    ),
    ModDto(
        id="2868840-curated-ancient-waifus",
        mod_kind="appearance",
        name="Ancient Waifus (고대의 존재 스킨)",
        author="커뮤니티",
        summary=(
            "선행 이벤트(고대의 존재) 스파인·카드 아트를 묶은 mixed 스킨 팩. "
            "Sts2SkinManager와 함께 쓰는 경우가 많습니다."
        ),
        characters=list(_ALL_STS2_CHARACTERS),
        source="curated",
        source_url="https://m.dcinside.com/board/slay/333106",
    ),
    ModDto(
        id="2868840-curated-star-rail-replace",
        mod_kind="appearance",
        name="Honkai Star Rail Replace (5캐릭터)",
        author="xumoge3723",
        summary=(
            "5인 로스터 전투·선택 화면 스프라이트를 붕괴: 스타레일 캐릭터 "
            "Q版 아트로 교체하는 비주얼 팩."
        ),
        characters=list(_ALL_STS2_CHARACTERS),
        source="nexus",
        source_url=(
            "https://www.nexusmods.com/slaythespire2/mods/"
            "?keyword=star+rail+Replace+xumoge3723"
        ),
    ),
    # --- 전 캐릭터 팩 ---
    ModDto(
        id="2868840-curated-nexus-61",
        mod_kind="appearance",
        name="Guise",
        author="Tbonex28b",
        summary=(
            "5캐릭터용 16종 몬스터 스킨 팩. 캐릭터 선택 화면에서 스킨을 고릅니다 "
            "(프로그 나이트·스펙트럴 나이트 등)."
        ),
        characters=list(_ALL_STS2_CHARACTERS),
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/61",
    ),
    ModDto(
        id="2868840-curated-nexus-163",
        mod_kind="appearance",
        name="STS2-Arknights-Pack",
        author="fxhere1024",
        summary=(
            "아크나이츠 캐릭터로 5인 플레이어블 외형 교체 "
            "(첸·프로스트·링·켈시트·레이지 등)."
        ),
        characters=list(_ALL_STS2_CHARACTERS),
        source="nexus",
        source_url="https://www.nexusmods.com/slaythespire2/mods/163",
    ),
]

_CURATED_BY_STEAM_APP_ID: dict[int, list[ModDto]] = {
    2868840: _STS2_APPEARANCE,
}


def curated_appearance_mods_for(steam_app_id: int) -> list[ModDto]:
    return list(_CURATED_BY_STEAM_APP_ID.get(steam_app_id, []))
