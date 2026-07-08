export type ScoutPatchContentBlock = {
  type: "text" | "image";
  text?: string | null;
  url?: string | null;
};

export type ScoutPatchNote = {
  id: string;
  title: string;
  publishedAt: string;
  summary: string;
  bodyKo: string;
  imageUrls?: string[];
  contentBlocks?: ScoutPatchContentBlock[];
  sourceUrl?: string;
};

export type ScoutModKind = "appearance" | "functional";
export type ScoutModSource = "nexus" | "workshop" | "curated" | "github";

export type ModCharacterSlug =
  | "regent"
  | "silent"
  | "ironclad"
  | "defect"
  | "necrobinder"
  | "collection"
  | "other";

export const MOD_CHARACTER_LABELS: Record<ModCharacterSlug, string> = {
  regent: "리젠트",
  silent: "사일런트",
  ironclad: "아이언클래드",
  defect: "디펙트",
  necrobinder: "네크로바인더",
  collection: "모음",
  other: "기타",
};

/** 플레이어블 로스터 — 2명 이상이면 모음 탭으로만 분류 */
export const ROSTER_CHARACTER_SLUGS: ModCharacterSlug[] = [
  "regent",
  "silent",
  "ironclad",
  "defect",
  "necrobinder",
];

export const MOD_CHARACTER_ORDER: ModCharacterSlug[] = [
  "regent",
  "silent",
  "ironclad",
  "defect",
  "necrobinder",
  "collection",
  "other",
];

export type ScoutMod = {
  id: string;
  modKind: ScoutModKind;
  name: string;
  author: string;
  summary: string;
  characters?: ModCharacterSlug[];
  source?: ScoutModSource;
  sourceUrl?: string;
};

export type ModCharacterGroup = {
  slug: ModCharacterSlug;
  label: string;
  mods: ScoutMod[];
};

export function modCharacterBucket(mod: ScoutMod): ModCharacterSlug {
  const raw = mod.characters ?? [];
  const roster = raw.filter((slug): slug is ModCharacterSlug =>
    ROSTER_CHARACTER_SLUGS.includes(slug as ModCharacterSlug),
  );
  if (roster.length >= 2) {
    return "collection";
  }
  if (roster.length === 1) {
    return roster[0];
  }
  return "other";
}

export function groupModsByCharacter(mods: ScoutMod[]): ModCharacterGroup[] {
  const buckets = new Map<ModCharacterSlug, ScoutMod[]>();

  for (const mod of mods) {
    const key = modCharacterBucket(mod);
    const list = buckets.get(key) ?? [];
    list.push(mod);
    buckets.set(key, list);
  }

  return MOD_CHARACTER_ORDER.filter((slug) => buckets.has(slug)).map((slug) => ({
    slug,
    label: MOD_CHARACTER_LABELS[slug],
    mods: buckets.get(slug) ?? [],
  }));
}

export function modSourceLinkLabel(source?: ScoutModSource): string {
  switch (source) {
    case "nexus":
      return "Nexus Mods에서 보기";
    case "workshop":
      return "Steam Workshop에서 보기";
    case "github":
      return "GitHub에서 보기";
    case "curated":
      return "제작자 페이지에서 보기";
    default:
      return "모드 페이지에서 보기";
  }
}

export type ScoutRelatedVideo = {
  id: string;
  title: string;
  channel: string;
  publishedAt: string;
  watchUrl: string;
};

export type ScoutGameDetail = {
  steamAppId: number;
  title: string;
  steamStoreUrl: string;
  officialSiteUrl: string;
  patchNotes: ScoutPatchNote[];
  appearanceMods: ScoutMod[];
  functionalMods: ScoutMod[];
  videos: ScoutRelatedVideo[];
};

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const PATCH_CACHE_VERSION = "v5";

export function patchNotesStorageKey(steamAppId: number): string {
  return `scout-patch-notes-${PATCH_CACHE_VERSION}-${steamAppId}`;
}

export function isKoreanPatchNote(note: ScoutPatchNote): boolean {
  const body = note.bodyKo.trim();
  return (
    body.length > 0 &&
    !body.startsWith("【") &&
    /[\uac00-\ud7a3]/.test(body)
  );
}

/** 모달에 쓸 만한 전체 본문이 있는지 */
export function hasFullPatchBody(note: ScoutPatchNote): boolean {
  return isKoreanPatchNote(note) && note.bodyKo.trim().length > 250;
}

/** contentBlocks 텍스트가 한국어인지 */
export function hasKoreanPatchBlocks(note: ScoutPatchNote): boolean {
  return (note.contentBlocks ?? []).some(
    (b) => b.type === "text" && !!b.text && /[\uac00-\ud7a3]/.test(b.text),
  );
}

/** 모달에 바로 표시할 한글 본문·블록이 준비됐는지 */
export function isPatchNoteReady(note: ScoutPatchNote): boolean {
  const blocks = note.contentBlocks ?? [];
  if (!hasKoreanPatchBlocks(note)) {
    return hasFullPatchBody(note) && blocks.length === 0;
  }
  const hasImages = blocks.some((b) => b.type === "image");
  const koreanTextCount = blocks.filter(
    (b) => b.type === "text" && b.text && /[\uac00-\ud7a3]/.test(b.text),
  ).length;
  if (note.id.includes("-steam-") && hasImages && koreanTextCount < 2) {
    return false;
  }
  return true;
}

/** 브라우저에 저장된 한글 패치와 서버 응답 병합 */
export function mergePatchNotesWithCache(
  steamAppId: number,
  serverNotes: ScoutPatchNote[],
): ScoutPatchNote[] {
  if (typeof window === "undefined") return serverNotes;

  try {
    const raw = localStorage.getItem(patchNotesStorageKey(steamAppId));
    if (!raw) return serverNotes;

    const cached = JSON.parse(raw) as ScoutPatchNote[];
    const serverUsesSteam = serverNotes.some((n) => n.id.includes("-steam-"));
    if (serverUsesSteam && cached.some((n) => !n.id.includes("-steam-"))) {
      localStorage.removeItem(patchNotesStorageKey(steamAppId));
      return serverNotes;
    }

    const byId = new Map(cached.map((n) => [n.id, n]));
    return serverNotes.map((note) => {
      const hit = byId.get(note.id);
      if (hit?.id === note.id && (hasFullPatchBody(hit) || hasKoreanPatchBlocks(hit))) {
        return {
          ...note,
          ...hit,
          imageUrls: note.imageUrls?.length ? note.imageUrls : hit.imageUrls,
          contentBlocks: hasKoreanPatchBlocks(hit)
            ? hit.contentBlocks
            : hasKoreanPatchBlocks(note)
              ? note.contentBlocks
              : hit.contentBlocks ?? note.contentBlocks,
        };
      }
      if (hasFullPatchBody(note) || isKoreanPatchNote(note)) return note;
      return note;
    });
  } catch {
    return serverNotes;
  }
}

const _lastSavedByApp = new Map<number, string>();

export function savePatchNotesToCache(
  steamAppId: number,
  notes: ScoutPatchNote[],
): void {
  if (typeof window === "undefined") return;
  if (!notes.some(isKoreanPatchNote)) return;
  try {
    const payload = JSON.stringify(notes);
    if (_lastSavedByApp.get(steamAppId) === payload) return;
    _lastSavedByApp.set(steamAppId, payload);
    localStorage.setItem(patchNotesStorageKey(steamAppId), payload);
  } catch {
    /* storage full 등 */
  }
}

/** Steam 패치는 본문 번역 전 bodyKo 가 비어 있어야 함 */
export function needsPatchNoteTranslation(note: ScoutPatchNote): boolean {
  if (isPatchNoteReady(note)) return false;
  const body = note.bodyKo.trim();
  if (!body) return true;
  if (note.id.includes("-steam-") && !/[\uac00-\ud7a3]/.test(body)) {
    return true;
  }
  if ((note.contentBlocks?.length ?? 0) > 0 && !hasKoreanPatchBlocks(note)) {
    return true;
  }
  return false;
}

/** GET /scout/games/{steamAppId}/patch-notes/{noteId}/korean — Steam 본문 조회·한글 번역 */
export async function fetchPatchNoteKorean(
  steamAppId: number,
  noteId: string,
): Promise<ScoutPatchNote | null> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 90_000);
  try {
    const res = await fetch(
      `${apiBaseUrl}/scout/games/${steamAppId}/patch-notes/${encodeURIComponent(noteId)}/korean`,
      { cache: "no-store", signal: controller.signal },
    );
    if (!res.ok) return null;
    const data = (await res.json()) as ScoutPatchNote;
    return {
      ...data,
      bodyKo: data.bodyKo?.trim() ?? "",
      imageUrls: data.imageUrls ?? [],
      contentBlocks: data.contentBlocks ?? [],
    };
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

/** GET /scout/games/{steamAppId}/detail — 실패 시 플레이스홀더 */
export async function fetchScoutGameDetail(
  steamAppId: number,
  title: string,
): Promise<ScoutGameDetail> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12_000);
  try {
    const res = await fetch(
      `${apiBaseUrl}/scout/games/${steamAppId}/detail`,
      { cache: "no-store", signal: controller.signal },
    );
    if (!res.ok) {
      return getScoutGameDetailPlaceholder(steamAppId, title);
    }
    const data = (await res.json()) as ScoutGameDetail;
    return {
      ...data,
      patchNotes: data.patchNotes.map((note) => ({
        ...note,
        bodyKo: note.bodyKo?.trim() ?? "",
        imageUrls: note.imageUrls ?? [],
        contentBlocks: note.contentBlocks ?? [],
      })),
    };
  } catch {
    return getScoutGameDetailPlaceholder(steamAppId, title);
  } finally {
    clearTimeout(timeout);
  }
}

/** API 연동 전 프론트 플레이스홀더 */
function defaultStoreUrl(steamAppId: number): string {
  return `https://store.steampowered.com/app/${steamAppId}`;
}

export function getScoutGameDetailPlaceholder(
  steamAppId: number,
  title: string,
): ScoutGameDetail {
  const steamStoreUrl = defaultStoreUrl(steamAppId);
  return {
    steamAppId,
    title,
    steamStoreUrl,
    officialSiteUrl: steamStoreUrl,
    patchNotes: [
      {
        id: `${steamAppId}-patch-1`,
        title: "최신 업데이트",
        publishedAt: "2026-05-01",
        summary:
          "밸런스 조정 및 버그 수정이 포함된 최신 빌드입니다. 클릭하면 한글 본문을 볼 수 있습니다.",
        bodyKo: [
          `${title} 최신 업데이트 안내입니다.`,
          "",
          "【개요】",
          "· 밸런스 조정 및 버그 수정이 포함된 빌드가 배포되었습니다.",
          "",
          "【안내】",
          "· Scout 에서 한글로 요약한 패치 노트입니다.",
          "· 원문은 Steam 뉴스 링크에서 확인할 수 있습니다.",
        ].join("\n"),
        sourceUrl: `${steamStoreUrl}/news/`,
      },
    ],
    appearanceMods: [
      {
        id: `${steamAppId}-mod-appearance-1`,
        modKind: "appearance",
        name: "외형 모드 예시",
        author: "Community",
        summary: "캐릭터 스킨·카드 아트 등 외형 변경 모드가 이 영역에 표시됩니다.",
        characters: ["regent"],
        source: "curated",
        sourceUrl: steamStoreUrl,
      },
    ],
    functionalMods: [
      {
        id: `${steamAppId}-mod-functional-1`,
        modKind: "functional",
        name: "기능 모드 예시",
        author: "Community",
        summary: "새 캐릭터·밸런스·QoL 등 플레이 변경 모드가 이 영역에 표시됩니다.",
        source: "curated",
        sourceUrl: steamStoreUrl,
      },
    ],
    videos: [
      {
        id: `${steamAppId}-video-1`,
        title: `${title} 공략·하이라이트`,
        channel: "Scout Curated",
        publishedAt: "2026-04-15",
        watchUrl: `https://www.youtube.com/results?search_query=${encodeURIComponent(title)}`,
      },
    ],
  };
}
