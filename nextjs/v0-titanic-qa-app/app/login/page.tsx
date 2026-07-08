"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { LogIn } from "lucide-react";

import { AuthPageShell } from "@/components/auth-page-shell";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

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
