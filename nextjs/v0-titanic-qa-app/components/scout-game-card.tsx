import Link from "next/link";

import { STEAM_CDN, type ScoutGame } from "@/lib/scout-genres";
import { scoutGameDetailPath } from "@/lib/scout-game-lookup";

type ScoutGameCardProps = {
  game: ScoutGame;
  genreId: string;
};

export function ScoutGameCard({ game, genreId }: ScoutGameCardProps) {
  const href = scoutGameDetailPath(genreId, game.steamAppId);

  return (
    <Link
      href={href}
      className="group block rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 overflow-hidden shadow-sm hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-md transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-2"
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={`${STEAM_CDN}/${game.steamAppId}/header.jpg`}
        alt=""
        className="w-full h-24 object-cover group-hover:brightness-105 transition-[filter]"
      />
      <div className="p-4">
        <h3 className="font-semibold mb-1 group-hover:text-violet-700 dark:group-hover:text-violet-300 transition-colors">
          {game.title}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
          {game.summary}
        </p>
        <p className="mt-2 text-xs text-violet-600 dark:text-violet-400 font-medium">
          패치노트 · 모드 · 영상 보기
        </p>
      </div>
    </Link>
  );
}
