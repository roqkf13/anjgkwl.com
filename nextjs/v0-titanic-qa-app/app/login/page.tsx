"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useState } from "react";
import { LogIn } from "lucide-react";

import { AuthPageShell } from "@/components/auth-page-shell";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

function OAuthStatusNotice() {
  const params = useSearchParams();
  const oauthStatus = params.get("oauth");
  const providerLabel = params.get("provider") === "naver" ? "네이버" : "구글";

  if (oauthStatus === "success") {
    return (
      <p className="text-sm text-green-600 dark:text-green-400" role="status">
        {providerLabel} 계정으로 로그인되었습니다.
      </p>
    );
  }
  if (oauthStatus === "error") {
    return (
      <p className="text-sm text-red-600 dark:text-red-400" role="alert">
        {providerLabel} 로그인에 실패했습니다. 다시 시도해 주세요.
      </p>
    );
  }
  return null;
}

type LoginUiState = {
  error: string | null;
  success: boolean;
  submitting: boolean;
};

const initialUiState: LoginUiState = {
  error: null,
  success: false,
  submitting: false,
};

export default function LoginPage() {
  const [ui, setUi] = useState<LoginUiState>(initialUiState);

  const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const formProps = Object.fromEntries(formData.entries()) as Record<
      string,
      string
    >;

    const email = (formProps.email ?? "").trim();
    const password = formProps.password ?? "";

    setUi({ error: null, success: false, submitting: false });

    if (!email || !password) {
      setUi((prev) => ({ ...prev, error: "이메일과 비밀번호를 입력해 주세요." }));
      return;
    }

    setUi((prev) => ({ ...prev, submitting: true }));
    try {
      const res = await fetch(`${apiBaseUrl}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const payload = (await res.json()) as {
        detail?: string | unknown;
        message?: string;
      };

      if (!res.ok) {
        const detail = payload.detail;
        const errorMessage =
          typeof detail === "string"
            ? detail
            : `요청 실패 (HTTP ${res.status})`;
        setUi((prev) => ({ ...prev, error: errorMessage }));
        return;
      }

      setUi((prev) => ({ ...prev, success: true }));
    } catch {
      setUi((prev) => ({
        ...prev,
        error: `서버에 연결할 수 없습니다. 백엔드(${apiBaseUrl})가 실행 중인지 확인하세요.`,
      }));
    } finally {
      setUi((prev) => ({ ...prev, submitting: false }));
    }
  };

  return (
    <AuthPageShell
      title="로그인"
      description="Titanic QA 계정으로 로그인하세요."
      footer={
        <>
          계정이 없으신가요?{" "}
          <Link
            href="/signup"
            className="font-medium text-violet-600 dark:text-violet-400 hover:underline"
          >
            회원가입
          </Link>
        </>
      }
    >
      <Suspense fallback={null}>
        <OAuthStatusNotice />
      </Suspense>

      <a
        href={`${apiBaseUrl}/auth/google/login`}
        className="inline-flex w-full items-center justify-center gap-2 rounded-md border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden>
          <path
            fill="#4285F4"
            d="M23.52 12.27c0-.85-.08-1.67-.22-2.45H12v4.64h6.47a5.53 5.53 0 0 1-2.4 3.63v3h3.88c2.27-2.09 3.57-5.17 3.57-8.82z"
          />
          <path
            fill="#34A853"
            d="M12 24c3.24 0 5.95-1.07 7.94-2.91l-3.88-3a7.14 7.14 0 0 1-10.62-3.76H1.44v3.1A12 12 0 0 0 12 24z"
          />
          <path
            fill="#FBBC05"
            d="M5.44 14.33a7.2 7.2 0 0 1 0-4.66v-3.1H1.44a12 12 0 0 0 0 10.86z"
          />
          <path
            fill="#EA4335"
            d="M12 4.76c1.76 0 3.35.6 4.6 1.79l3.44-3.44C17.94 1.19 15.24 0 12 0A12 12 0 0 0 1.44 6.57l4 3.1A7.15 7.15 0 0 1 12 4.76z"
          />
        </svg>
        구글로 로그인
      </a>

      <a
        href="/api/auth/naver/login"
        className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-md bg-[#03C75A] px-4 py-2 text-sm font-medium text-white hover:bg-[#02b350] transition-colors"
      >
        <span
          className="flex h-4 w-4 items-center justify-center text-[13px] font-black leading-none"
          aria-hidden
        >
          N
        </span>
        네이버로 로그인
      </a>

      <div className="my-4 flex items-center gap-3">
        <Separator className="flex-1" />
        <span className="text-xs text-gray-500 dark:text-gray-400">또는</span>
        <Separator className="flex-1" />
      </div>

      <form onSubmit={handleLogin} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="login-email">이메일</Label>
          <Input
            id="login-email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            required
            disabled={ui.submitting}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="login-password">비밀번호</Label>
          <Input
            id="login-password"
            name="password"
            type="password"
            autoComplete="current-password"
            placeholder="비밀번호"
            required
            disabled={ui.submitting}
          />
        </div>

        {ui.error && (
          <p className="text-sm text-red-600 dark:text-red-400" role="alert">
            {ui.error}
          </p>
        )}
        {ui.success && (
          <p
            className="text-sm text-green-600 dark:text-green-400"
            role="status"
          >
            로그인에 성공했습니다.
          </p>
        )}

        <button
          type="submit"
          disabled={ui.submitting}
          className="inline-flex w-full items-center justify-center gap-2 rounded-md bg-violet-600 px-4 py-2 text-sm font-medium text-white hover:bg-violet-700 transition-colors disabled:opacity-50"
        >
          <LogIn size={16} aria-hidden />
          {ui.submitting ? "로그인 중…" : "로그인"}
        </button>
      </form>
    </AuthPageShell>
  );
}
