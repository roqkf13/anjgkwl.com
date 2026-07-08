import { Compass, Map, Shield, Swords, type LucideIcon } from "lucide-react";

export const STEAM_CDN = "https://cdn.cloudflare.steamstatic.com/steam/apps";

export type ScoutGame = {
  title: string;
  summary: string;
  steamAppId: number;
};

export type ScoutGenre = {
  id: string;
  label: string;
  href: string;
  description: string;
  gameTitle: string;
  imageUrl: string;
  icon: LucideIcon;
  overlayClass: string;
  buttonClass: string;
  traits: string[];
  games: ScoutGame[];
};

export const SCOUT_GENRES: ScoutGenre[] = [
  {
    id: "soulslike",
    label: "소울라이크",
    href: "/scout/soulslike",
    description: "높은 난이도와 보스 전투 중심의 액션 RPG",
    gameTitle: "ELDEN RING",
    imageUrl: `${STEAM_CDN}/1245620/header.jpg`,
    icon: Shield,
    overlayClass: "from-red-950/80 via-red-900/55 to-red-950/75",
    buttonClass: "bg-red-600 group-hover:bg-red-700 text-white",
    traits: ["패턴 학습", "높은 난이도", "보스 중심 전투", "스태미나·회피"],
    games: [
      {
        title: "ELDEN RING",
        summary: "오픈 필드와 레거던 던전이 결합된 프롬소프트 대표작.",
        steamAppId: 1245620,
      },
      {
        title: "Dark Souls III",
        summary: "시리즈 정수를 담은 좁은 맵 기반 소울라이크.",
        steamAppId: 374320,
      },
      {
        title: "Sekiro: Shadows Die Twice",
        summary: "패링과 자세 시스템이 핵심인 액션 중심 소울라이크.",
        steamAppId: 814380,
      },
    ],
  },
  {
    id: "roguelike",
    label: "로그라이크",
    href: "/scout/roguelike",
    description: "매 run 이 다른 랜덤 던전과 성장",
    gameTitle: "Slay the Spire 2",
    imageUrl: `${STEAM_CDN}/2868840/header.jpg`,
    icon: Swords,
    overlayClass: "from-violet-950/80 via-violet-900/55 to-violet-950/75",
    buttonClass: "bg-violet-600 group-hover:bg-violet-700 text-white",
    traits: ["영구 사망", "랜덤 맵", "빌드 조합", "run 기반 성장"],
    games: [
      {
        title: "Slay the Spire 2",
        summary: "카드 덱 빌딩과 roguelike run 의 후속작.",
        steamAppId: 2868840,
      },
      {
        title: "Hades",
        summary: "스토리와 액션이 결합된 roguelike 인디 명작.",
        steamAppId: 1145360,
      },
      {
        title: "Balatro",
        summary: "포커 핸드 조합 기반의 roguelike 덱빌더.",
        steamAppId: 2379780,
      },
    ],
  },
  {
    id: "openworld",
    label: "오픈월드",
    href: "/scout/openworld",
    description: "넓은 맵을 자유롭게 탐험하는 세계",
    gameTitle: "Red Dead Redemption 2",
    imageUrl: `${STEAM_CDN}/1174180/header.jpg`,
    icon: Map,
    overlayClass: "from-emerald-950/80 via-emerald-900/55 to-emerald-950/75",
    buttonClass: "bg-emerald-600 group-hover:bg-emerald-700 text-white",
    traits: ["자유 탐험", "사이드 콘텐츠", "몰입형 세계관", "장거리 이동"],
    games: [
      {
        title: "Red Dead Redemption 2",
        summary: "서부 시대 오픈월드 서사와 생태계가 돋보이는 작품.",
        steamAppId: 1174180,
      },
      {
        title: "The Witcher 3: Wild Hunt",
        summary: "퀘스트 밀도가 높은 판타지 오픈월드 RPG.",
        steamAppId: 292030,
      },
      {
        title: "Ghost of Tsushima DIRECTOR'S CUT",
        summary: "사무라이 액션과 아름다운 오픈 필드 탐험.",
        steamAppId: 2215430,
      },
    ],
  },
  {
    id: "metroidvania",
    label: "메트로배니아",
    href: "/scout/metroidvania",
    description: "능력 해금으로 맵을 확장하는 탐험",
    gameTitle: "Hollow Knight",
    imageUrl: `${STEAM_CDN}/367520/header.jpg`,
    icon: Compass,
    overlayClass: "from-amber-950/80 via-amber-900/55 to-amber-950/75",
    buttonClass: "bg-amber-600 group-hover:bg-amber-700 text-white",
    traits: ["능력 게이트", "맵 백트래킹", "2D 탐험", "보스 전투"],
    games: [
      {
        title: "Hollow Knight",
        summary: "넓은 2D 맵과 가스파라트풍 분위기의 대표 메트로배니아.",
        steamAppId: 367520,
      },
      {
        title: "Ori and the Blind Forest",
        summary: "플랫폼과 스토리가 조화된 감성형 메트로배니아.",
        steamAppId: 261570,
      },
      {
        title: "Blasphemous",
        summary: "다크 판타지 풍의 2D 액션 메트로배니아.",
        steamAppId: 774361,
      },
    ],
  },
];

export function getScoutGenre(id: string): ScoutGenre | undefined {
  return SCOUT_GENRES.find((genre) => genre.id === id);
}
