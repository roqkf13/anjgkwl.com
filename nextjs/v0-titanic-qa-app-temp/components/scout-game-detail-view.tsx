"use client";

import Link from "next/link";
import { useEffect, useRef, useState, type ReactNode } from "react";
import {
  ArrowLeft,
  ChevronDown,
  ChevronRight,
  ExternalLink,
  FileText,
  Loader2,
  Puzzle,
  Shirt,
  Wrench,
  Youtube,
} from "lucide-react";

import { ScoutPatchNoteModal } from "@/components/scout-patch-note-modal";
import { STEAM_CDN, getScoutGenre } from "@/lib/scout-genres";
import {
  fetchPatchNoteKorean,
  fetchScoutGameDetail,
  hasFullPatchBody,
  isPatchNoteReady,
  mergePatchNotesWithCache,
  needsPatchNoteTranslation,
  savePatchNotesToCache,
  type ScoutGameDetail,
  groupModsByCharacter,
  modSourceLinkLabel,
  type ModCharacterSlug,
  type ScoutMod,
  type ScoutPatchNote,
} from "@/lib/scout-game-detail";

type ScoutGameDetailViewProps = {
  genreId: string;
  steamAppId: number;
  initialTitle: string;
};

function ModCard({ mod }: { mod: ScoutMod }) {
  return (
    <li className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-4">
      {mod.sourceUrl ? (
        <a
          href={mod.sourceUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium text-violet-700 dark:text-violet-300 hover:underline"
        >
          {mod.name}
        </a>
      ) : (
        <h4 className="font-medium">{mod.name}</h4>
      )}
      <p className="text-xs text-gray-500 mt-0.5">{mod.author}</p>
      <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 line-clamp-2">
        {mod.summary}
      </p>
      {mod.sourceUrl && (
        <a
          href={mod.sourceUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-2 inline-flex items-center gap-1 text-xs text-violet-600 dark:text-violet-400 hover:underline"
        >
          {modSourceLinkLabel(mod.source)}
          <span aria-hidden>↗</span>
        </a>
      )}
    </li>
  );
}

const MOD_PAGE_SIZE = 8;

function ModList({ mods }: { mods: ScoutMod[] }) {
  const [visible, setVisible] = useState(MOD_PAGE_SIZE);
  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setVisible(MOD_PAGE_SIZE);
  }, [mods]);

  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible((v) => Math.min(v + MOD_PAGE_SIZE, mods.length));
        }
      },
      { threshold: 0.1 },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [mods]);

  const shown = mods.slice(0, visible);
  const remaining = mods.length - visible;

  return (
    <div className="space-y-3">
      <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {shown.map((mod) => (
          <ModCard key={mod.id} mod={mod} />
        ))}
      </ul>
      {remaining > 0 && (
        <div ref={sentinelRef} className="flex items-center justify-center py-3 text-xs text-gray-400 dark:text-gray-600">
          스크롤하면 더 불러옵니다 ({remaining}개 남음)
        </div>
      )}
    </div>
  );
}

function ModSubsection({
  id,
  title,
  icon,
  mods,
  emptyMessage,
}: {
  id: string;
  title: string;
  icon: ReactNode;
  mods: ScoutMod[];
  emptyMessage: string;
}) {
  return (
    <div>
      <div className="flex items-center gap-2 mb-3">
        {icon}
        <h3 id={id} className="text-base font-semibold">
          {title}
        </h3>
      </div>
      {mods.length === 0 ? (
        <p className="text-sm text-gray-500 dark:text-gray-400">{emptyMessage}</p>
      ) : (
        <ModList mods={mods} />
      )}
    </div>
  );
}

function AppearanceModsByCharacter({
  mods,
  emptyMessage,
}: {
  mods: ScoutMod[];
  emptyMessage: string;
}) {
  const groups = groupModsByCharacter(mods);
  const [activeCharacter, setActiveCharacter] = useState<ModCharacterSlug | "all">(
    "all",
  );
  const [expandedSections, setExpandedSections] = useState<
    Set<ModCharacterSlug>
  >(new Set());
  const tabInitialized = useRef(false);

  useEffect(() => {
    tabInitialized.current = false;
    setExpandedSections(new Set());
  }, [mods]);

  useEffect(() => {
    if (tabInitialized.current || groups.length === 0) return;
    tabInitialized.current = true;
    setActiveCharacter(groups[0].slug);
  }, [groups]);

  if (mods.length === 0) {
    return (
      <p className="text-sm text-gray-500 dark:text-gray-400">{emptyMessage}</p>
    );
  }

  const visibleGroups =
    activeCharacter === "all"
      ? groups
      : groups.filter((group) => group.slug === activeCharacter);

  function selectTab(next: ModCharacterSlug | "all") {
    setActiveCharacter(next);
    if (next === "all") {
      setExpandedSections(new Set());
    }
  }

  function toggleSection(slug: ModCharacterSlug) {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) {
        next.delete(slug);
      } else {
        next.add(slug);
      }
      return next;
    });
  }

  return (
    <div className="space-y-4">
      <div
        className="flex flex-wrap gap-2"
        role="tablist"
        aria-label="캐릭터별 외형 모드"
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeCharacter === "all"}
          onClick={() => selectTab("all")}
          className={`rounded-full px-3 py-1 text-sm font-medium transition-colors ${
            activeCharacter === "all"
              ? "bg-violet-600 text-white"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700"
          }`}
        >
          전체
        </button>
        {groups.map((group) => (
          <button
            key={group.slug}
            type="button"
            role="tab"
            aria-selected={activeCharacter === group.slug}
            onClick={() => selectTab(group.slug)}
            className={`rounded-full px-3 py-1 text-sm font-medium transition-colors ${
              activeCharacter === group.slug
                ? "bg-violet-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700"
            }`}
          >
            {group.label}
            <span className="ml-1 opacity-80">({group.mods.length})</span>
          </button>
        ))}
      </div>

      {activeCharacter === "all" && (
        <p className="text-xs text-gray-500 dark:text-gray-400">
          전체 보기에서는 섹션을 접어 두었습니다. 펼치려면 제목을 누르거나 캐릭터
          탭을 선택하세요.
        </p>
      )}

      <div className="space-y-3">
        {visibleGroups.map((group) => {
          const isAllView = activeCharacter === "all";
          const isExpanded = !isAllView || expandedSections.has(group.slug);

          return (
            <div
              key={group.slug}
              className={
                isAllView
                  ? "rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 overflow-hidden"
                  : undefined
              }
            >
              {isAllView ? (
                <button
                  type="button"
                  onClick={() => toggleSection(group.slug)}
                  aria-expanded={isExpanded}
                  className="flex w-full items-center justify-between gap-2 px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800/60 transition-colors"
                >
                  <span className="text-sm font-semibold text-gray-800 dark:text-gray-200">
                    {group.label}
                    <span className="ml-1 font-normal text-gray-500">
                      ({group.mods.length})
                    </span>
                  </span>
                  <ChevronDown
                    size={18}
                    className={`shrink-0 text-gray-400 transition-transform ${
                      isExpanded ? "rotate-180" : ""
                    }`}
                    aria-hidden
                  />
                </button>
              ) : null}
              {isExpanded && (
                <div className={isAllView ? "px-4 pb-4" : undefined}>
                  <ModList mods={group.mods} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export function ScoutGameDetailView({
  genreId,
  steamAppId,
  initialTitle,
}: ScoutGameDetailViewProps) {
  const [detail, setDetail] = useState<ScoutGameDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(true);
  const [detailLoadFailed, setDetailLoadFailed] = useState(false);
  const [patchNotes, setPatchNotes] = useState<ScoutPatchNote[]>([]);
  const [openNote, setOpenNote] = useState<ScoutPatchNote | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [detailError, setDetailError] = useState(false);
  const prefetchStarted = useRef(false);

  useEffect(() => {
    prefetchStarted.current = false;
  }, [steamAppId]);

  const genre = getScoutGenre(genreId);
  if (!genre) return null;

  const title = detail?.title ?? initialTitle;
  const showSteamLink =
    detail &&
    detail.steamStoreUrl !== detail.officialSiteUrl;

  const loadGameDetail = () => {
    setDetailLoading(true);
    setDetailLoadFailed(false);
    fetchScoutGameDetail(steamAppId, initialTitle)
      .then((d) => {
        const failed =
          d.appearanceMods.length === 1 &&
          d.appearanceMods[0]?.name === "외형 모드 예시";
        if (failed) {
          setDetail(null);
          setPatchNotes([]);
          setDetailLoadFailed(true);
          return;
        }
        setDetail(d);
        setPatchNotes(mergePatchNotesWithCache(steamAppId, d.patchNotes));
      })
      .finally(() => {
        setDetailLoading(false);
      });
  };

  useEffect(() => {
    loadGameDetail();
  }, [steamAppId, initialTitle]);

  useEffect(() => {
    if (patchNotes.length === 0) return;
    savePatchNotesToCache(steamAppId, patchNotes);
  }, [steamAppId, patchNotes]);

  useEffect(() => {
    if (detailLoading || prefetchStarted.current) return;
    const pending = patchNotes.filter(
      (n) => needsPatchNoteTranslation(n) && !hasFullPatchBody(n),
    );
    if (pending.length === 0) return;
    prefetchStarted.current = true;

    let cancelled = false;
    (async () => {
      for (const note of pending) {
        if (cancelled) return;
        const full = await fetchPatchNoteKorean(steamAppId, note.id);
        if (cancelled || !full) continue;
        setPatchNotes((prev) => {
          const next = prev.map((n) => (n.id === full.id ? full : n));
          savePatchNotesToCache(steamAppId, next);
          return next;
        });
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [detailLoading, patchNotes, steamAppId]);

  function updateNoteInList(note: ScoutPatchNote) {
    setPatchNotes((prev) => {
      const next = prev.map((n) => (n.id === note.id ? note : n));
      savePatchNotesToCache(steamAppId, next);
      return next;
    });
  }

  async function openPatchNote(note: ScoutPatchNote) {
    const current = patchNotes.find((n) => n.id === note.id) ?? note;
    setOpenNote(current);
    setDetailError(false);

    if (isPatchNoteReady(current)) return;

    setLoadingDetail(true);
    try {
      const full = await fetchPatchNoteKorean(steamAppId, note.id);
      if (full && (isPatchNoteReady(full) || hasFullPatchBody(full))) {
        setOpenNote(full);
        updateNoteInList(full);
      } else {
        setDetailError(true);
      }
    } finally {
      setLoadingDetail(false);
    }
  }

  return (
    <main className="flex flex-1 flex-col min-h-0 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <div className="relative h-40 sm:h-48 shrink-0 overflow-hidden bg-gray-950">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`${STEAM_CDN}/${steamAppId}/library_hero.jpg`}
          alt=""
          aria-hidden
          className="absolute inset-0 h-full w-full object-cover object-center opacity-70"
        />
        <div
          className={`absolute inset-0 bg-gradient-to-t ${genre.overlayClass} opacity-90`}
          aria-hidden
        />
        <div className="relative z-10 h-full max-w-7xl mx-auto px-4 sm:px-6 flex flex-col justify-end pb-6">
          <p className="text-xs text-white/70 mb-1">{genre.label}</p>
          <h1 className="text-2xl sm:text-3xl font-bold text-white drop-shadow">
            {title}
          </h1>
          {detail && (
            <div className="flex flex-wrap gap-2 mt-3">
              <a
                href={detail.officialSiteUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-full bg-white/95 text-gray-900 hover:bg-white transition-colors shadow-sm"
              >
                <ExternalLink size={16} aria-hidden />
                공식 사이트
              </a>
              {showSteamLink && (
                <a
                  href={detail.steamStoreUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-full bg-black/40 text-white border border-white/30 hover:bg-black/55 transition-colors"
                >
                  <ExternalLink size={16} aria-hidden />
                  Steam 스토어
                </a>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-10">
          <nav className="flex flex-wrap gap-3 text-sm">
            <Link
              href={genre.href}
              className="inline-flex items-center gap-1.5 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
            >
              <ArrowLeft size={16} aria-hidden />
              {genre.label} 허브
            </Link>
            <span className="text-gray-300 dark:text-gray-600" aria-hidden>
              /
            </span>
            <span className="text-gray-900 dark:text-gray-100 font-medium">
              게임 상세
            </span>
          </nav>

          <section aria-labelledby="patch-notes-heading">
            <div className="flex items-center gap-2 mb-4">
              <FileText size={20} className="text-violet-600" aria-hidden />
              <h2 id="patch-notes-heading" className="text-lg font-semibold">
                최신 패치노트
              </h2>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
              Steam 공식 패치를 한글로 불러옵니다. 항목을 누르면 번역된 전문을
              바로 볼 수 있습니다.
            </p>
            {detailLoading ? (
              <div className="flex items-center gap-2 text-sm text-gray-500 py-6">
                <Loader2 size={18} className="animate-spin" aria-hidden />
                패치·모드 불러오는 중…
              </div>
            ) : detailLoadFailed ? (
              <div className="rounded-xl border border-amber-200 dark:border-amber-900 bg-amber-50 dark:bg-amber-950/40 p-4 text-sm">
                <p className="text-amber-900 dark:text-amber-100">
                  Scout API에 연결하지 못했습니다. 백엔드가 실행 중인지 확인해
                  주세요.
                </p>
                <button
                  type="button"
                  onClick={loadGameDetail}
                  className="mt-3 rounded-full bg-violet-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-violet-700 transition-colors"
                >
                  다시 시도
                </button>
              </div>
            ) : (
              <ul className="flex gap-3 overflow-x-auto pb-2 snap-x snap-mandatory scrollbar-hide">
                {patchNotes.map((note) => (
                  <li key={note.id} className="shrink-0 w-64 snap-start">
                    <button
                      type="button"
                      onClick={() => openPatchNote(note)}
                      className="w-full h-full text-left rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-4 hover:border-violet-300 dark:hover:border-violet-700 hover:shadow-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-2 flex flex-col"
                    >
                      <time
                        dateTime={note.publishedAt}
                        className="text-xs text-gray-500"
                      >
                        {note.publishedAt}
                      </time>
                      <h3 className="font-medium text-gray-900 dark:text-gray-100 mt-1 line-clamp-2 flex-1">
                        {note.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 line-clamp-3">
                        {note.summary}
                      </p>
                      <span className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-violet-600 dark:text-violet-400">
                        한글 전문 보기
                        <ChevronRight size={12} aria-hidden />
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>

          {(detailLoading || detail) && !detailLoadFailed && (
            <>
              <section aria-labelledby="mods-heading" className="space-y-8">
                <div className="flex items-center gap-2">
                  <Puzzle size={20} className="text-violet-600" aria-hidden />
                  <h2 id="mods-heading" className="text-lg font-semibold">
                    모드
                  </h2>
                </div>

                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <Shirt size={18} className="text-pink-600" aria-hidden />
                    <h3 id="appearance-mods-heading" className="text-base font-semibold">
                      외형 모드
                    </h3>
                  </div>
                  {detailLoading || !detail ? (
                    <div className="flex items-center gap-2 text-sm text-gray-500 py-4">
                      <Loader2 size={18} className="animate-spin" aria-hidden />
                      외형 모드 불러오는 중…
                    </div>
                  ) : (
                    <AppearanceModsByCharacter
                      mods={detail.appearanceMods}
                      emptyMessage="등록된 외형 모드가 없습니다."
                    />
                  )}
                </div>
                {detailLoading || !detail ? (
                  <div className="flex items-center gap-2 text-sm text-gray-500 py-4">
                    <Loader2 size={18} className="animate-spin" aria-hidden />
                    기능 모드 불러오는 중…
                  </div>
                ) : (
                  <ModSubsection
                    id="functional-mods-heading"
                    title="기능 모드"
                    icon={
                      <Wrench size={18} className="text-amber-600" aria-hidden />
                    }
                    mods={detail.functionalMods}
                    emptyMessage="등록된 기능 모드가 없습니다."
                  />
                )}
              </section>

              <section aria-labelledby="videos-heading">
                <div className="flex items-center gap-2 mb-4">
                  <Youtube size={20} className="text-red-600" aria-hidden />
                  <h2 id="videos-heading" className="text-lg font-semibold">
                    관련 영상
                  </h2>
                </div>
                {detailLoading || !detail ? (
                  <div className="flex items-center gap-2 text-sm text-gray-500 py-4">
                    <Loader2 size={18} className="animate-spin" aria-hidden />
                    관련 영상 불러오는 중…
                  </div>
                ) : (
                <ul className="space-y-3">
                  {detail.videos.map((video) => (
                    <li
                      key={video.id}
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
                        {video.channel} · {video.publishedAt}
                      </p>
                    </li>
                  ))}
                </ul>
                )}
              </section>
            </>
          )}
        </div>
      </div>

      {openNote && (
        <ScoutPatchNoteModal
          note={openNote}
          gameTitle={title}
          isLoading={loadingDetail}
          loadError={detailError}
          onClose={() => {
            setOpenNote(null);
            setDetailError(false);
          }}
        />
      )}
    </main>
  );
}
