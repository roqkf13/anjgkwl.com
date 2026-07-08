import Link from "next/link";
import type { ReactNode } from "react";

type AuthPageShellProps = {
  title: string;
  description: string;
  footer?: ReactNode;
  children: ReactNode;
};

export function AuthPageShell({
  title,
  description,
  footer,
  children,
}: AuthPageShellProps) {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 px-4 py-12">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <Link
            href="/"
            className="text-sm font-medium text-violet-600 dark:text-violet-400 hover:underline"
          >
            Titanic QA
          </Link>
          <h1 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
            {title}
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {description}
          </p>
        </div>

        <div className="rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-sm">
          {children}
        </div>

        {footer && (
          <p className="text-center text-sm text-gray-600 dark:text-gray-400">
            {footer}
          </p>
        )}
      </div>
    </main>
  );
}
