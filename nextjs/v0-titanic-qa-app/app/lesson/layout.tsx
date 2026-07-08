import { LessonLayoutShell } from "@/components/lesson-layout-shell";

export default function LessonLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <LessonLayoutShell>{children}</LessonLayoutShell>;
}
