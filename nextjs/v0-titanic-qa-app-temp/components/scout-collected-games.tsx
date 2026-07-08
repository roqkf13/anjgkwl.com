"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { ScoutGameCard } from "@/components/scout-game-card";
import { getScoutGenre, type ScoutGame } from "@/lib/scout-genres";
import { readMergedGenreIds } from "@/lib/scout-merged-genres";

type ScoutCollectedGamesProps = {
  genreId: string;
  baseGames: ScoutGame[];
  searchQuery?: string;
};

function gameMatchesSearch(game: ScoutGame, query: string): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  return (
    game.title.toLowerCase().includes(q) ||
    game.summary.toLowerCase().includes(q)
  );
}

export function ScoutCollectedGames({
  genreId,
  baseGames,
  searchQuery = "",
}: ScoutCollectedGamesProps) {
  const [mergedIds, setMergedIds] = useState<string[]>([]);
  const [hydrated, setHydrated] = useState(false);

  const refresh = useCallback(() => {
    setMergedIds(readMergedGenreIds());
  }, []);

  useEffect(() => {
    refresh();
    setHydrated(true);
    const onChange = () => refresh();
    window.addEventListener("scout-merged-genres-changed", onChange);
    window.addEventListener("storage", onChange);
    return () => {
      window.removeEventListener("scout-merged-genres-changed", onChange);
      window.removeEventListener("storage", onChange);
    };
  }, [refresh]);

  const mergedOtherIds = useMemo(
    () => mergedIds.filter((id) => id !== genreId),
    [mergedIds, genreId],
  );

  const filteredBaseGames = useMemo(
    () => baseGames.filter((g) => gameMatchesSearch(g, searchQuery)),
    [baseGames, searchQuery],
  );

  const trimmedQuery = searchQuery.trim();

  return (
    <section>
      <div className="mb-4">
        <h2 className="text-lg font-semibold">모여 있는 정보</h2>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
          오른쪽 검색창으로 카드를 걸러 낼 수 있습니다.「선호 장르」를 누르면 이
          섹션 <strong className="text-gray-700 dark:text-gray-300">아래</strong>에
          다른 장르 게임이 붙거나 빠집니다.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {filteredBaseGames.map((game) => (
          <ScoutGameCard
            key={`base-${game.steamAppId}`}
            game={game}
            genreId={genreId}
          />
        ))}
      </div>

      {trimmedQuery.length > 0 && filteredBaseGames.length === 0 && (
        <p className="text-sm text-gray-500 dark:text-gray-400 py-4">
          현재 장르에서 검색 결과가 없습니다.
        </p>
      )}

      {hydrated &&
        mergedOtherIds.map((id) => {
          const meta = getScoutGenre(id);
          if (!meta) return null;
          const filteredMerged = meta.games.filter((g) =>
            gameMatchesSearch(g, searchQuery),
          );
          if (trimmedQuery.length > 0 && filteredMerged.length === 0) {
            return null;
          }
          return (
            <div
              key={id}
              className="mt-10 pt-8 border-t border-gray-200 dark:border-gray-800"
            >
              <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100 mb-4">
                {meta.label}
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
                {filteredMerged.map((game) => (
                  <ScoutGameCard
                    key={`${id}-${game.steamAppId}`}
                    game={game}
                    genreId={id}
                  />
                ))}
              </div>
            </div>
          );
        })}

      {trimmedQuery.length > 0 &&
        filteredBaseGames.length === 0 &&
        hydrated &&
        mergedOtherIds.every((id) => {
          const meta = getScoutGenre(id);
          if (!meta) return true;
          return !meta.games.some((g) => gameMatchesSearch(g, searchQuery));
        }) && (
          <p className="text-sm text-gray-500 dark:text-gray-400 py-6 text-center border border-dashed border-gray-200 dark:border-gray-800 rounded-xl">
            「{trimmedQuery}」에 맞는 게임이 없습니다. 검색어를 바꿔 보세요.
          </p>
        )}
    </section>
  );
}
