import Link from "next/link";

import { SCOUT_GENRES } from "@/lib/scout-genres";

export function ScoutZones() {
  return (
    <section
      aria-label="게임 장르 구역"
      className="w-full h-[42vh] min-h-[240px] max-h-[420px] flex overflow-x-auto"
    >
      {SCOUT_GENRES.map((zone, index) => {
        const Icon = zone.icon;
        return (
          <Link
            key={zone.id}
            href={zone.href}
            aria-label={`${zone.label} 정보 구역으로 이동`}
            className="group relative flex-1 min-w-[200px] flex flex-col border-r last:border-r-0 border-gray-200/80 dark:border-gray-700/80 overflow-hidden bg-gray-950 cursor-pointer transition-[filter] hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-white/80"
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={zone.imageUrl}
              alt=""
              aria-hidden
              className="absolute inset-0 h-full w-full object-contain object-center blur-[3px] brightness-90 pointer-events-none"
            />
            <div
              className={`absolute inset-0 bg-gradient-to-b ${zone.overlayClass} opacity-90 group-hover:opacity-80 transition-opacity pointer-events-none`}
              aria-hidden
            />

            <div className="relative z-10 flex flex-col h-full p-5 sm:p-6 text-white pointer-events-none">
              <div className="flex items-center gap-3 mb-3 shrink-0">
                <div className="inline-flex items-center justify-center w-10 h-10 rounded-xl bg-black/30 backdrop-blur-sm shrink-0">
                  <Icon size={20} className="text-white" aria-hidden />
                </div>
                <div className="min-w-0">
                  <h2 className="text-base sm:text-lg font-semibold drop-shadow-sm">
                    {zone.label}
                  </h2>
                  <p className="text-[11px] sm:text-xs text-white/75 truncate">
                    {zone.gameTitle}
                  </p>
                </div>
              </div>

              <p className="text-sm text-white/85 leading-relaxed flex-1 drop-shadow-sm">
                {zone.description}
              </p>

              <span
                className={`mt-4 shrink-0 inline-flex w-full items-center justify-center rounded-xl px-4 py-2.5 text-sm font-medium transition-colors shadow-lg pointer-events-none ${zone.buttonClass}`}
              >
                {zone.label} 탐색
              </span>
            </div>

            {index < SCOUT_GENRES.length - 1 && (
              <span className="sr-only">
                다음 구역: {SCOUT_GENRES[index + 1].label}
              </span>
            )}
          </Link>
        );
      })}
    </section>
  );
}
