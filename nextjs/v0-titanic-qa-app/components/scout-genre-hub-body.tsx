"use client";

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { useState } from "react";

import { FavoriteGenresPanel } from "@/components/scout-favorite-genres-panel";
import { ScoutCollectedGames } from "@/components/scout-collected-games";
import { ScoutGameSearch } from "@/components/scout-game-search";
import { getScoutGenre } from "@/lib/scout-genres";

type ScoutGenreHubBodyProps = {
  genreId: string;
};

export function ScoutGenreHubBody({ genreId }: ScoutGenreHubBodyProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const genre = getScoutGenre(genreId);

  if (!genre) return null;

  return (
    <div className="max-w-7xl mx-auto flex flex-col lg:flex-row min-h-0">
      <div className="flex-1 min-w-0 px-4 sm:px-6 py-8 space-y-8">
        <section>
          <h2 className="text-lg font-semibold mb-3">장르 특징</h2>
          <ul className="flex flex-wrap gap-2">
            {genre.traits.map((trait) => (
              <li
                key={trait}
                className="px-3 py-1.5 text-sm rounded-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800"
              >
                {trait}
              </li>
            ))}
          </ul>
        </section>

        <ScoutCollectedGames
          genreId={genre.id}
          baseGames={genre.games}
          searchQuery={searchQuery}
        />

        <Link
          href="/"
          className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <ArrowLeft size={16} aria-hidden />
          Scout 메인으로
        </Link>
      </div>

      <aside className="shrink-0 lg:w-48 xl:w-52 border-t lg:border-t-0 lg:border-l border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-3 sm:px-4 py-6 lg:sticky lg:top-14 lg:self-start lg:max-h-[calc(100vh-3.5rem)] lg:overflow-y-auto">
        <ScoutGameSearch value={searchQuery} onChange={setSearchQuery} />
        <FavoriteGenresPanel currentGenreId={genre.id} />
      </aside>
    </div>
  );
}
