"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const categoryNavItems = [
  { id: "all", label: "ALL", href: "/" },
  { id: "rag", label: "RAG SYSTEM", href: "/lesson" },
  { id: "architecture", label: "ARCHITECTURE", href: "/lesson" },
  { id: "agent", label: "AGENT", href: "/lesson" },
  { id: "backend", label: "BACKEND", href: "/lesson" },
  { id: "mobile", label: "MOBILE", href: "/lesson" },
  { id: "devops", label: "DEVOPS", href: "/lesson" },
  { id: "nlp", label: "NLP", href: "/lesson" },
  { id: "lesson", label: "수업용", href: "/lesson" },
] as const;

function isActive(pathname: string, id: string): boolean {
  if (id === "all") {
    return pathname === "/";
  }
  if (id === "lesson") {
    return pathname === "/lesson" || pathname.startsWith("/lesson/");
  }
  return false;
}

export function LessonCategoryNav() {
  const pathname = usePathname();

  return (
    <nav
      className="border-b border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-950"
      aria-label="카테고리 메뉴"
    >
      <div className="overflow-x-auto">
        <ul className="flex min-w-max items-center gap-6 px-6 sm:px-10 py-3">
          {categoryNavItems.map((item) => {
            const active = isActive(pathname, item.id);
            return (
              <li key={item.id}>
                <Link
                  href={item.href}
                  className={[
                    "whitespace-nowrap text-xs sm:text-sm tracking-wide transition-colors",
                    item.id === "lesson"
                      ? "normal-case"
                      : "uppercase font-medium",
                    active
                      ? "font-semibold text-gray-900 dark:text-gray-100"
                      : "font-medium text-gray-400 hover:text-gray-700 dark:text-gray-500 dark:hover:text-gray-300",
                  ].join(" ")}
                  aria-current={active ? "page" : undefined}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </div>
    </nav>
  );
}
