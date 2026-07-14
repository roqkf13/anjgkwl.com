export type ScoutSearchVideo = {
  title: string;
  channel: string;
  watchUrl: string;
  publishedAt?: string | null;
};

export type ScoutSearchResult = {
  title: string;
  platform?: string | null;
  summary?: string | null;
  officialSiteUrl?: string | null;
  videos: ScoutSearchVideo[];
};

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

/** GET /scout/search?q= — 실패·미발견 시 null */
export async function fetchScoutGameSearch(
  query: string,
): Promise<ScoutSearchResult | null> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30_000);
  try {
    const res = await fetch(
      `${apiBaseUrl}/scout/search?q=${encodeURIComponent(query)}`,
      { cache: "no-store", signal: controller.signal },
    );
    if (!res.ok) return null;
    const data = (await res.json()) as ScoutSearchResult;
    return {
      ...data,
      videos: data.videos ?? [],
    };
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}
