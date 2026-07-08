"use client";

import { Menu } from "lucide-react";
import { useState } from "react";

import { LessonCategoryNav } from "@/components/lesson-category-nav";
import { LessonSideNav } from "@/components/lesson-side-nav";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

type LessonLayoutShellProps = {
  children: React.ReactNode;
};

export function LessonLayoutShell({ children }: LessonLayoutShellProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex flex-1 min-h-0 bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <aside className="hidden md:block w-56 lg:w-64 shrink-0 border-r border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 px-3 py-6">
        <LessonSideNav />
      </aside>

      <div className="flex flex-1 flex-col min-w-0 min-h-0">
        <div className="md:hidden sticky top-0 z-20 flex items-center gap-3 border-b border-gray-200 bg-white/95 px-4 py-3 backdrop-blur dark:border-gray-800 dark:bg-gray-950/95">
          <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger asChild>
              <Button
                type="button"
                variant="outline"
                size="icon"
                aria-label="수업용 메뉴 열기"
              >
                <Menu size={18} aria-hidden />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-72 p-0">
              <SheetHeader className="border-b border-gray-200 px-4 py-4 dark:border-gray-800">
                <SheetTitle>수업용 메뉴</SheetTitle>
                <SheetDescription>
                  타이타닉 학습 메뉴를 선택하세요.
                </SheetDescription>
              </SheetHeader>
              <div className="px-3 py-4">
                <LessonSideNav onNavigate={() => setOpen(false)} />
              </div>
            </SheetContent>
          </Sheet>

          <div className="min-w-0">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
              Lesson
            </p>
            <p className="truncate text-sm font-semibold text-gray-900 dark:text-gray-100">
              타이타닉
            </p>
          </div>
        </div>

        <LessonCategoryNav />
        <div className="flex flex-1 flex-col min-w-0 min-h-0">{children}</div>
      </div>
    </div>
  );
}
