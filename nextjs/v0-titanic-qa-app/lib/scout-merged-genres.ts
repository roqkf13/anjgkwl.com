/** 브라우저에만 저장. 메인 장르 이미지(상단) 클릭 시 "모여 있는 정보"에 합칠 장르 id 목록. */

export const MERGED_GENRES_STORAGE_KEY = "scout-merged-genre-ids";

export function readMergedGenreIds(): string[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(MERGED_GENRES_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed) || !parsed.every((x) => typeof x === "string")) {
      return [];
    }
    return parsed;
  } catch {
    return [];
  }
}

export function writeMergedGenreIds(ids: string[]): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(MERGED_GENRES_STORAGE_KEY, JSON.stringify(ids));
    window.dispatchEvent(new Event("scout-merged-genres-changed"));
  } catch {
    /* quota */
  }
}

/** 토글 후 최종 id 배열 반환 */
export function toggleMergedGenreId(id: string): string[] {
  const cur = readMergedGenreIds();
  const next = cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id];
  writeMergedGenreIds(next);
  return next;
}

export function removeMergedGenreId(id: string): void {
  writeMergedGenreIds(readMergedGenreIds().filter((x) => x !== id));
}
