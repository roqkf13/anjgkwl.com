"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { UserPlus } from "lucide-react";

import { AuthPageShell } from "@/components/auth-page-shell";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type SignupUiState = {
  error: string | null;
  success: boolean;
  submitting: boolean;
};

const initialUiState: SignupUiState = {
  error: null,
  success: false,
  submitting: false,
};

export default function SignupPage() {
  const [ui, setUi] = useState<SignupUiState>(initialUiState);

  const handleSignup = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const formProps = Object.fromEntries(formData.entries()) as Record<
      string,
      string
    >;

    const name = (formProps.name ?? "").trim();
    const email = (formProps.email ?? "").trim();
    const password = formProps.password ?? "";
    const passwordConfirm = formProps.passwordConfirm ?? "";
    const role = "user";

    setUi({ error: null, success: false, submitting: false });

    if (!name || !email || !password) {
      setUi((prev) => ({ ...prev, error: "모든 항목을 입력해 주세요." }));
      return;
    }
    if (password.length < 8) {
      setUi((prev) => ({
        ...prev,
        error: "비밀번호는 8자 이상이어야 합니다.",
      }));
      return;
    }
    if (password !== passwordConfirm) {
      setUi((prev) => ({ ...prev, error: "비밀번호가 일치하지 않습니다." }));
      return;
    }

    setUi((prev) => ({ ...prev, submitting: true }));
    try {
      const res = await fetch(`${apiBaseUrl}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, passwordConfirm, role }),
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
      e.currentTarget.reset();
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
      title="회원가입"
      description="Titanic QA 계정을 만들어 서비스를 이용하세요."
      footer={
        <>
          이미 계정이 있으신가요?{" "}
          <Link
            href="/login"
            className="font-medium text-violet-600 dark:text-violet-400 hover:underline"
          >
            로그인
          </Link>
        </>
      }
    >
      <form onSubmit={handleSignup} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="signup-name">이름</Label>
          <Input
            id="signup-name"
            name="name"
            type="text"
            autoComplete="name"
            placeholder="홍길동"
            required
            disabled={ui.submitting}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="signup-email">이메일</Label>
          <Input
            id="signup-email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            required
            disabled={ui.submitting}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="signup-password">비밀번호</Label>
          <Input
            id="signup-password"
            name="password"
            type="password"
            autoComplete="new-password"
            placeholder="8자 이상"
            minLength={8}
            required
            disabled={ui.submitting}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="signup-password-confirm">비밀번호 확인</Label>
          <Input
            id="signup-password-confirm"
            name="passwordConfirm"
            type="password"
            autoComplete="new-password"
            placeholder="비밀번호 다시 입력"
            minLength={8}
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
            가입 요청이 완료되었습니다. 로그인 페이지에서 로그인해 주세요.
          </p>
        )}

        <button
          type="submit"
          disabled={ui.submitting}
          className="inline-flex w-full items-center justify-center gap-2 rounded-md bg-violet-600 px-4 py-2 text-sm font-medium text-white hover:bg-violet-700 transition-colors disabled:opacity-50"
        >
          <UserPlus size={16} aria-hidden />
          {ui.submitting ? "전송 중…" : "회원가입"}
        </button>
      </form>
    </AuthPageShell>
  );
}
