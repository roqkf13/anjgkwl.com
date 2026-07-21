"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { UserCheck } from "lucide-react";

import { AuthPageShell } from "@/components/auth-page-shell";

export default function NaverConsentPage() {
  const router = useRouter();
  const [termsAgreed, setTermsAgreed] = useState(false);
  const [privacyAgreed, setPrivacyAgreed] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = termsAgreed && privacyAgreed && !submitting;

  const handleAgree = async () => {
    setError(null);
    setSubmitting(true);
    try {
      const res = await fetch("/api/auth/naver/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agreed: true }),
      });
      const payload = (await res.json()) as { error?: string };
      if (!res.ok) {
        setError(payload.error ?? "가입 처리에 실패했습니다.");
        return;
      }
      router.push("/oauth-complete?oauth=success&provider=naver");
    } catch {
      setError("서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthPageShell
      title="약관 동의"
      description="네이버 계정으로 가입을 완료하려면 아래 약관에 동의해 주세요."
    >
      <div className="space-y-4">
        <label className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-200">
          <input
            type="checkbox"
            className="mt-1"
            checked={termsAgreed}
            onChange={(e) => setTermsAgreed(e.target.checked)}
          />
          <span>
            <span className="font-medium">[필수]</span>{" "}
            <Link
              href="/terms"
              target="_blank"
              className="text-violet-600 dark:text-violet-400 hover:underline"
            >
              이용약관
            </Link>
            에 동의합니다.
          </span>
        </label>

        <label className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-200">
          <input
            type="checkbox"
            className="mt-1"
            checked={privacyAgreed}
            onChange={(e) => setPrivacyAgreed(e.target.checked)}
          />
          <span>
            <span className="font-medium">[필수]</span>{" "}
            <Link
              href="/privacy"
              target="_blank"
              className="text-violet-600 dark:text-violet-400 hover:underline"
            >
              개인정보 처리방침
            </Link>
            에 동의합니다.
          </span>
        </label>

        {error && (
          <p className="text-sm text-red-600 dark:text-red-400" role="alert">
            {error}
          </p>
        )}

        <button
          type="button"
          disabled={!canSubmit}
          onClick={handleAgree}
          className="inline-flex w-full items-center justify-center gap-2 rounded-md bg-violet-600 px-4 py-2 text-sm font-medium text-white hover:bg-violet-700 transition-colors disabled:opacity-50"
        >
          <UserCheck size={16} aria-hidden />
          {submitting ? "처리 중…" : "동의하고 가입 완료"}
        </button>

        <Link
          href="/oauth-complete?oauth=error&provider=naver&reason=cancelled"
          className="block text-center text-sm text-gray-500 dark:text-gray-400 hover:underline"
        >
          취소
        </Link>
      </div>
    </AuthPageShell>
  );
}
