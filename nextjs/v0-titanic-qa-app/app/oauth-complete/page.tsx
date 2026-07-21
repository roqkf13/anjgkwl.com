"use client";

import { Suspense, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import { OAUTH_RESULT_STORAGE_KEY, type OAuthResult } from "@/lib/oauth-result";

function OAuthCompleteInner() {
  const router = useRouter();
  const params = useSearchParams();

  useEffect(() => {
    const status = params.get("oauth") === "success" ? "success" : "error";
    const provider = params.get("provider") ?? "";
    const reason = params.get("reason") ?? undefined;

    const result: OAuthResult = { status, provider, reason, ts: Date.now() };
    try {
      localStorage.setItem(OAUTH_RESULT_STORAGE_KEY, JSON.stringify(result));
    } catch {
      // localStorage 접근 불가(사파리 프라이빗 모드 등) — 팝업이면 opener가 못 받으니 아래 폴백 리다이렉트로 이어짐
    }

    // 팝업으로 열린 경우: 닫으면 이 아래 코드는 실행되지 않는다.
    window.close();

    // 팝업이 아니었거나(차단됨) close()가 허용되지 않는 경우를 위한 폴백.
    const timer = setTimeout(() => {
      if (status === "success") {
        router.replace("/");
      } else {
        const qs = new URLSearchParams({ oauth: "error", provider });
        if (reason) qs.set("reason", reason);
        router.replace(`/login?${qs.toString()}`);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [params, router]);

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 px-4">
      <p className="text-sm text-gray-600 dark:text-gray-400">로그인 처리 중입니다…</p>
    </main>
  );
}

export default function OAuthCompletePage() {
  return (
    <Suspense fallback={null}>
      <OAuthCompleteInner />
    </Suspense>
  );
}
