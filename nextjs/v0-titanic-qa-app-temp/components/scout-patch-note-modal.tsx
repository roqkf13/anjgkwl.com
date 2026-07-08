"use client";

import { useEffect, useMemo } from "react";
import { ExternalLink, X } from "lucide-react";

import {
  hasKoreanPatchBlocks,
  type ScoutPatchContentBlock,
  type ScoutPatchNote,
} from "@/lib/scout-game-detail";

type ScoutPatchNoteModalProps = {
  note: ScoutPatchNote;
  gameTitle: string;
  isLoading?: boolean;
  loadError?: boolean;
  onClose: () => void;
};

function renderTextLines(text: string, keyPrefix: string) {
  const lines = text.split("\n").filter((line) => line.length > 0);
  return lines.map((line, i) =>
    line.startsWith("【") ? (
      <p
        key={`${keyPrefix}-${i}`}
        className="font-semibold text-gray-900 dark:text-gray-100 pt-1"
      >
        {line}
      </p>
    ) : line.startsWith("·") || line.startsWith("- ") ? (
      <p key={`${keyPrefix}-${i}`} className="pl-2">
        {line}
      </p>
    ) : (
      <p key={`${keyPrefix}-${i}`}>{line}</p>
    ),
  );
}

function renderContentBlock(block: ScoutPatchContentBlock, index: number) {
  if (block.type === "image" && block.url) {
    return (
      <img
        key={`img-${index}-${block.url}`}
        src={block.url}
        alt={`패치 이미지 ${index + 1}`}
        loading="lazy"
        referrerPolicy="no-referrer"
        className="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800"
      />
    );
  }
  if (block.type === "text" && block.text?.trim()) {
    return (
      <div key={`text-${index}`} className="space-y-3">
        {renderTextLines(block.text, `block-${index}`)}
      </div>
    );
  }
  return null;
}

export function ScoutPatchNoteModal({
  note,
  gameTitle,
  isLoading = false,
  loadError = false,
  onClose,
}: ScoutPatchNoteModalProps) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [onClose]);

  const contentBlocks = useMemo(
    () => note.contentBlocks?.filter(Boolean) ?? [],
    [note.contentBlocks],
  );

  const paragraphs = useMemo(
    () => note.bodyKo.split("\n").filter((line) => line.length > 0),
    [note.bodyKo],
  );

  const blocksAreKorean = hasKoreanPatchBlocks(note);
  const showBlocks = contentBlocks.length > 0 && blocksAreKorean && !isLoading;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      role="presentation"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="patch-note-modal-title"
        className="relative w-full max-w-2xl max-h-[85vh] overflow-y-auto rounded-2xl bg-white dark:bg-gray-900 shadow-xl border border-gray-200 dark:border-gray-800"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          type="button"
          onClick={onClose}
          className="absolute top-3 right-3 p-2 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800"
          aria-label="닫기"
        >
          <X size={20} aria-hidden />
        </button>

        <div className="p-6 pr-12">
          <p className="text-xs text-violet-600 dark:text-violet-400 mb-1">
            {gameTitle}
          </p>
          <h2
            id="patch-note-modal-title"
            className="text-xl font-semibold text-gray-900 dark:text-gray-100"
          >
            {note.title}
          </h2>
          <time
            dateTime={note.publishedAt}
            className="block text-xs text-gray-500 mt-1 mb-4"
          >
            {note.publishedAt}
          </time>

          {isLoading && (
            <p className="text-sm text-gray-500 dark:text-gray-400 py-4 text-center">
              Steam 패치 상세를 가져와 한글로 번역하는 중입니다…
            </p>
          )}

          {showBlocks ? (
            <div className="space-y-4 text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
              {contentBlocks.map((block, i) => renderContentBlock(block, i))}
            </div>
          ) : (
            !isLoading && (
              <div className="space-y-3 text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                {paragraphs.length === 0 && loadError && (
                  <p className="text-gray-500">
                    패치 상세를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.
                  </p>
                )}
                {paragraphs.length === 0 && !loadError && (
                  <p className="text-gray-500">본문을 불러오지 못했습니다.</p>
                )}
                {paragraphs.map((line, i) =>
                  line.startsWith("【") ? (
                    <p
                      key={i}
                      className="font-semibold text-gray-900 dark:text-gray-100 pt-1"
                    >
                      {line}
                    </p>
                  ) : line.startsWith("·") || line.startsWith("- ") ? (
                    <p key={i} className="pl-2">
                      {line}
                    </p>
                  ) : (
                    <p key={i}>{line}</p>
                  ),
                )}
                {note.imageUrls && note.imageUrls.length > 0 && (
                  <div className="mt-6 space-y-4">
                    {note.imageUrls.map((url, i) => (
                      <img
                        key={`${url}-${i}`}
                        src={url}
                        alt={`${note.title} 이미지 ${i + 1}`}
                        loading="lazy"
                        referrerPolicy="no-referrer"
                        className="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800"
                      />
                    ))}
                  </div>
                )}
              </div>
            )
          )}

          {note.sourceUrl && !isLoading && (
            <a
              href={note.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-6 inline-flex items-center gap-1.5 text-sm text-violet-600 dark:text-violet-400 hover:underline"
            >
              <ExternalLink size={16} aria-hidden />
              Steam 원문 뉴스 보기
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
