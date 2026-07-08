"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronDown } from "lucide-react";
import { useEffect, useState } from "react";

const lessonNavSections = [
  {
    id: "titanic",
    label: "타이타닉",
    hrefPrefix: "/lesson/titanic",
    items: [
      { href: "/lesson/titanic/upload", label: "1. 데이터 수집" },
      { href: "/lesson/titanic/model", label: "2. 모델 분석" },
      { href: "/lesson/titanic/neon", label: "3. 구현 데이터 보기" },
      { href: "/lesson/titanic/smith", label: "4. 스미스 선장과 대화" },
    ],
  },
  {
    id: "vision",
    label: "비전 처리",
    hrefPrefix: "/lesson/vision",
    items: [{ href: "/lesson/vision", label: "1. 이미지 업로드" }],
  },
] as const;

type LessonSideNavProps = {
  onNavigate?: () => void;
};

export function LessonSideNav({ onNavigate }: LessonSideNavProps) {
  const pathname = usePathname();
  const [openSections, setOpenSections] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(
      lessonNavSections.map((section) => [
        section.id,
        pathname.startsWith(section.hrefPrefix),
      ]),
    ),
  );

  useEffect(() => {
    setOpenSections((prev) => {
      let changed = false;
      const next = { ...prev };
      for (const section of lessonNavSections) {
        if (pathname.startsWith(section.hrefPrefix) && !next[section.id]) {
          next[section.id] = true;
          changed = true;
        }
      }
      return changed ? next : prev;
    });
  }, [pathname]);

  return (
    <nav
      className="flex flex-col gap-1"
      aria-label="수업용 사이드 메뉴"
    >
      <p className="px-3 pb-2 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
        수업용
      </p>
      {lessonNavSections.map((section) => {
        const active = pathname.startsWith(section.hrefPrefix);
        const open = openSections[section.id];
        return (
          <div key={section.id} className="rounded-xl">
            <div
              className={[
                "flex w-full items-center rounded-lg text-sm font-medium transition-colors",
                active
                  ? "bg-teal-50 text-teal-900 dark:bg-teal-950 dark:text-teal-100"
                  : "text-gray-800 dark:text-gray-200",
              ].join(" ")}
            >
              <Link
                href={section.items[0].href}
                onClick={onNavigate}
                className="min-w-0 flex-1 rounded-lg px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                {section.label}
              </Link>
              <button
                type="button"
                onClick={() =>
                  setOpenSections((prev) => ({
                    ...prev,
                    [section.id]: !prev[section.id],
                  }))
                }
                className="mr-1 rounded-md p-2 hover:bg-gray-100 dark:hover:bg-gray-800"
                aria-expanded={open}
                aria-controls={`${section.id}-submenu`}
                aria-label={`${section.label} 하위 메뉴 ${open ? "접기" : "펼치기"}`}
              >
                <ChevronDown
                  size={16}
                  className={[
                    "shrink-0 transition-transform",
                    open ? "rotate-180" : "",
                  ].join(" ")}
                  aria-hidden
                />
              </button>
            </div>

            {open && (
              <div
                id={`${section.id}-submenu`}
                className="ml-3 mt-1 flex flex-col gap-1 border-l border-gray-200 pl-3 dark:border-gray-800"
              >
                {section.items.map((item) => {
                  const itemActive =
                    pathname === item.href || pathname.startsWith(`${item.href}/`);
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={onNavigate}
                      className={[
                        "rounded-md px-3 py-2 text-sm transition-colors",
                        itemActive
                          ? "bg-blue-50 text-blue-900 dark:bg-blue-950 dark:text-blue-100"
                          : "text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800",
                      ].join(" ")}
                      aria-current={itemActive ? "page" : undefined}
                    >
                      {item.label}
                    </Link>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </nav>
  );
}
