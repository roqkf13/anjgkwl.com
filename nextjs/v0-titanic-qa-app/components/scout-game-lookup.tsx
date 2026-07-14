"use client";

import { useState } from "react";
import { Loader2, Search } from "lucide-react";
import {
  fetchScoutGameSearch,
  type ScoutSearchResult,
} from "@/lib/scout-game-search-lookup";

const PLATFORM_LABELS: Record<string, string> = {
  steam: "Steam",
  mobile: "모바일",
  other: "기타",
};

export function ScoutGameLookup() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScoutSearchResult | null>(null);
  const [notFound, setNotFound] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const trimmed = query.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setNotFound(false);
    setResult(null);
    const found = await fetchScoutGameSearch(trimmed);
    setLoading(false);
    if (found) {
      setResult(found);
    } else {
      setNotFound(true);
    }
  }

  return (
    <section className="w-full max-w-2xl mx-auto px-4 pt-6 pb-2">
      <form
        onSubmit={handleSubmit}
        className="w-full rounded-full bg-white dark:bg-gray-900 shadow-[0_2px_12px_rgba(0,0,0,0.08)] dark:shadow-[0_2px_12px_rgba(0,0,0,0.35)] border border-gray-100 dark:border-gray-800 flex items-center gap-1 pl-3 pr-2 py-2"
        role="search"
      >
        <Search
          size={18}
          strokeWidth={1.75}
          className="shrink-0 text-gray-500 dark:text-gray-400"
          aria-hidden
        />
        <label htmlFor="scout-game-lookup" className="sr-only">
          어떤 게임이든 검색
        </label>
        <input
          id="scout-game-lookup"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="어떤 게임이든 검색해보세요 (모바일 게임 포함)"
          autoComplete="off"
          className="flex-1 min-w-0 bg-transparent px-1 py-1.5 text-[15px] text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none [&::-webkit-search-cancel-button]:hidden"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="shrink-0 rounded-full px-4 py-1.5 text-sm font-medium bg-violet-600 text-white disabled:opacity-40 hover:bg-violet-700 transition-colors"
        >
          검색
        </button>
      </form>

      {loading ? (
        <div className="flex items-center gap-2 text-sm text-gray-500 py-4">
          <Loader2 size={18} className="animate-spin" aria-hidden />
          AI가 게임 정보를 찾는 중…
        </div>
      ) : null}

      {!loading && notFound ? (
        <p className="text-sm text-gray-500 py-4">
          게임 정보를 찾지 못했습니다. 다른 이름으로 검색해보세요.
        </p>
      ) : null}

      {!loading && result ? (
        <div className="mt-4 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-4">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold">{result.title}</h2>
            {result.platform ? (
              <span className="text-xs px-2 py-0.5 rounded-full bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300">
                {PLATFORM_LABELS[result.platform] ?? result.platform}
              </span>
            ) : null}
          </div>
          {result.summary ? (
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
              {result.summary}
            </p>
          ) : null}
          {result.officialSiteUrl ? (
            <a
              href={result.officialSiteUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block text-sm text-violet-700 dark:text-violet-300 hover:underline mt-2"
            >
              공식 사이트 / 스토어 바로가기
            </a>
          ) : null}

          {result.videos.length > 0 ? (
            <ul className="space-y-3 mt-4">
              {result.videos.map((video, i) => (
                <li
                  key={`${video.watchUrl}-${i}`}
                  className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-4"
                >
                  <a
                    href={video.watchUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium hover:text-violet-700 dark:hover:text-violet-300 transition-colors"
                  >
                    {video.title}
                  </a>
                  <p className="text-xs text-gray-500 mt-1">
                    {video.channel}
                    {video.publishedAt ? ` · ${video.publishedAt}` : ""}
                  </p>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}
