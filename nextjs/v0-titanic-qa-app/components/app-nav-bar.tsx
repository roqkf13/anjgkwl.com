"use client";

import { useState } from "react";
import Link from "next/link";
import { LogIn, Mail, Settings, Sparkles, UserPlus, Menu, X } from "lucide-react";
import { DarkModeToggle } from "@/components/dark-mode-toggle";

export function AppNavBar() {
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);

  return (
    <nav className="sticky top-0 z-50 shrink-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div className="w-full px-4 sm:px-6 h-14 flex items-center gap-3">
        <Link
          href="/"
          className="text-lg font-bold tracking-tight text-gray-900 dark:text-gray-100 hover:opacity-80 transition-opacity shrink-0"
          onClick={close}
        >
          Scout
        </Link>

        {/* 데스크탑(md 이상): 버튼 전부 한 줄 */}
        <div className="ml-auto hidden md:flex items-center gap-2 shrink-0">
          <Link
            href="/chat"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg border border-blue-100 dark:border-blue-400 bg-gradient-to-b from-white to-blue-200 dark:from-gray-100 dark:to-blue-400 text-blue-800 dark:text-blue-900 hover:from-blue-50 hover:to-blue-300 dark:hover:from-white dark:hover:to-blue-300 transition-all shadow-sm"
          >
            <Sparkles size={16} className="text-blue-500 dark:text-blue-600" aria-hidden="true" />
            Gemini
          </Link>
          <Link
            href="/email"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
          >
            <Mail size={16} aria-hidden="true" />
            메일
          </Link>
          <Link
            href="/admin"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg border border-gray-700 bg-gray-900 text-gray-200 hover:bg-gray-800 hover:border-gray-600 transition-colors"
          >
            <Settings size={16} aria-hidden="true" />
            Admin
          </Link>
          <Link
            href="/login"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
          >
            <LogIn size={16} aria-hidden="true" />
            로그인
          </Link>
          <Link
            href="/signup"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg bg-teal-600 text-white hover:bg-teal-700 transition-colors"
          >
            <UserPlus size={16} aria-hidden="true" />
            회원가입
          </Link>
          <Link
            href="/lesson"
            className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
          >
            수업용
          </Link>
          <DarkModeToggle />
        </div>

        {/* 모바일: 햄버거 버튼 */}
        <button
          onClick={() => setOpen(o => !o)}
          className="ml-auto md:hidden w-9 h-9 flex items-center justify-center rounded-lg border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 active:scale-95 transition-transform shrink-0"
          aria-label={open ? "메뉴 닫기" : "메뉴 열기"}
          aria-expanded={open}
        >
          {open ? <X size={18} /> : <Menu size={18} />}
        </button>
      </div>

      {/* 모바일 드롭다운 메뉴 */}
      {open && (
        <div className="md:hidden border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3 flex flex-col gap-2">
          <Link
            href="/chat"
            onClick={close}
            className="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-lg border border-blue-100 dark:border-blue-400 bg-gradient-to-b from-white to-blue-200 dark:from-gray-100 dark:to-blue-400 text-blue-800 dark:text-blue-900"
          >
            <Sparkles size={16} className="text-blue-500 dark:text-blue-600" aria-hidden="true" />
            Gemini
          </Link>
          <Link
            href="/email"
            onClick={close}
            className="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          >
            <Mail size={16} aria-hidden="true" />
            메일
          </Link>
          <Link
            href="/admin"
            onClick={close}
            className="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-lg border border-gray-700 bg-gray-900 text-gray-200"
          >
            <Settings size={16} aria-hidden="true" />
            Admin
          </Link>
          <Link
            href="/login"
            onClick={close}
            className="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          >
            <LogIn size={16} aria-hidden="true" />
            로그인
          </Link>
          <Link
            href="/signup"
            onClick={close}
            className="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-lg bg-teal-600 text-white"
          >
            <UserPlus size={16} aria-hidden="true" />
            회원가입
          </Link>
          <Link
            href="/lesson"
            onClick={close}
            className="inline-flex items-center px-4 py-2.5 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          >
            수업용
          </Link>
          <DarkModeToggle />
        </div>
      )}
    </nav>
  );
}