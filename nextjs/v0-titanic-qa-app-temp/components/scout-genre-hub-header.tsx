"use client";

import { getScoutGenre } from "@/lib/scout-genres";

type ScoutGenreHubHeaderProps = {
  genreId: string;
};

export function ScoutGenreHubHeader({ genreId }: ScoutGenreHubHeaderProps) {
  const genre = getScoutGenre(genreId);
  if (!genre) return null;

  const Icon = genre.icon;

  return (
    <div className="relative h-44 sm:h-52 shrink-0 overflow-hidden bg-gray-950">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={genre.imageUrl}
        alt=""
        aria-hidden
        className="absolute inset-0 h-full w-full object-contain object-center blur-[2px] brightness-90"
      />
      <div
        className={`absolute inset-0 bg-gradient-to-b ${genre.overlayClass} opacity-85`}
        aria-hidden
      />
      <div className="relative z-10 h-full max-w-7xl mx-auto px-4 sm:px-6 flex flex-col justify-end pb-6">
        <div className="flex items-center gap-3">
          <div className="inline-flex items-center justify-center w-11 h-11 rounded-xl bg-black/30 backdrop-blur-sm">
            <Icon size={22} className="text-white" aria-hidden />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white drop-shadow">
              {genre.label}
            </h1>
            <p className="text-sm text-white/80">{genre.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
