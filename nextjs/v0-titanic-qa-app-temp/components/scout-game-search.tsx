"use client";

import { Search, X } from "lucide-react";

type ScoutGameSearchProps = {
  value: string;
  onChange: (value: string) => void;
};

export function ScoutGameSearch({ value, onChange }: ScoutGameSearchProps) {
  return (
    <div
      className="w-full rounded-full bg-white dark:bg-gray-900 shadow-[0_2px_12px_rgba(0,0,0,0.08)] dark:shadow-[0_2px_12px_rgba(0,0,0,0.35)] border border-gray-100 dark:border-gray-800 flex items-center gap-1 pl-3 pr-2 py-2 mb-5"
      role="search"
    >
      <Search
        size={18}
        strokeWidth={1.75}
        className="shrink-0 text-gray-500 dark:text-gray-400"
        aria-hidden
      />
      <label htmlFor="scout-game-search" className="sr-only">
        게임 검색
      </label>
      <input
        id="scout-game-search"
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="게임 검색"
        autoComplete="off"
        className="flex-1 min-w-0 bg-transparent px-1 py-1.5 text-[15px] text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none [&::-webkit-search-cancel-button]:hidden"
      />
      {value.length > 0 ? (
        <button
          type="button"
          onClick={() => onChange("")}
          aria-label="검색어 지우기"
          className="shrink-0 inline-flex items-center justify-center w-9 h-9 rounded-full text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <X size={18} strokeWidth={1.75} aria-hidden />
        </button>
      ) : (
        <span className="shrink-0 w-9" aria-hidden />
      )}
    </div>
  );
}
