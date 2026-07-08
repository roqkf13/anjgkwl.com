"use client";

import { useCallback, useEffect, useState } from "react";

import { SCOUT_GENRES } from "@/lib/scout-genres";
import {
  readMergedGenreIds,
  toggleMergedGenreId,
} from "@/lib/scout-merged-genres";

type FavoriteGenresPanelProps = {
  currentGenreId: string;
};

export function FavoriteGenresPanel({ currentGenreId }: FavoriteGenresPanelProps) {
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

  return (
    <div className="flex flex-col min-h-0">
      <h2 className="text-base font-semibold text-gray-900 dark:text-gray-100 mb-1">
        선호 장르
      </h2>
      <p className="text-[11px] text-gray-500 dark:text-gray-400 mb-3 leading-relaxed">
        장르 이미지를 누르면 왼쪽「모여 있는 정보」
        <strong className="text-gray-700 dark:text-gray-300"> 아래</strong>에 그 장르
        게임이 붙었다가, 다시 누르면 빠집니다. 테두리가 강한 이미지는 현재 페이지
        장르입니다.
      </p>

      {!hydrated ? (
        <p className="text-xs text-gray-400">…</p>
      ) : (
        <div className="grid grid-cols-2 gap-2">
          {SCOUT_GENRES.map((g) => {
            const isCurrent = g.id === currentGenreId;
            const isOn = mergedIds.includes(g.id);
            return (
              <button
                key={g.id}
                type="button"
                disabled={isCurrent}
                title={
                  isCurrent
                    ? "지금 보고 있는 장르입니다"
                    : isOn
                      ? `${g.label} — 다시 누르면 아래 목록에서 제거`
                      : `${g.label} — 누르면 아래에 게임 추가`
                }
                onClick={() => {
                  if (isCurrent) return;
                  toggleMergedGenreId(g.id);
                  refresh();
                }}
                className={[
                  "relative aspect-video w-full overflow-hidden rounded-xl border-2 transition-[box-shadow,opacity]",
                  isCurrent
                    ? "border-blue-500 ring-2 ring-blue-400/40 opacity-95 cursor-default"
                    : isOn
                      ? "border-emerald-500 ring-2 ring-emerald-400/30 hover:opacity-95"
                      : "border-transparent hover:border-gray-300 dark:hover:border-gray-600",
                ].join(" ")}
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={g.imageUrl}
                  alt=""
                  className="h-full w-full object-cover object-center scale-105"
                />
                <span className="absolute inset-x-0 bottom-0 bg-black/55 px-1 py-0.5 text-center text-[10px] font-medium text-white truncate">
                  {g.label}
                  {isCurrent && " · 현재"}
                  {!isCurrent && isOn && " · 표시 중"}
                </span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
