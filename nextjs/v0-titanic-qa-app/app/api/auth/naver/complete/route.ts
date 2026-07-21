import { NextRequest, NextResponse } from "next/server";
import { PENDING_SIGNUP_COOKIE, verifyPendingProfile } from "@/lib/oauth-pending-signup";

export const runtime = "nodejs";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function POST(req: NextRequest) {
  const body = (await req.json().catch(() => null)) as { agreed?: boolean } | null;
  if (!body?.agreed) {
    return NextResponse.json({ error: "약관에 동의해야 가입을 완료할 수 있습니다." }, { status: 400 });
  }

  const profile = verifyPendingProfile(req.cookies.get(PENDING_SIGNUP_COOKIE)?.value);
  if (!profile) {
    return NextResponse.json(
      { error: "가입 세션이 만료되었습니다. 네이버 로그인을 다시 시도해 주세요." },
      { status: 400 }
    );
  }

  const internalSecret = process.env.INTERNAL_OAUTH_SECRET?.trim();
  if (!internalSecret) {
    return NextResponse.json({ error: "서버 설정 오류입니다." }, { status: 503 });
  }

  const upsertRes = await fetch(`${apiBaseUrl}/auth/oauth/upsert`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-internal-secret": internalSecret,
    },
    body: JSON.stringify({
      provider: profile.provider,
      oauth_id: profile.oauthId,
      email: profile.email,
      name: profile.name,
    }),
  });

  if (!upsertRes.ok) {
    const detail = await upsertRes.text();
    console.error("[naver-complete] 백엔드 upsert 실패", upsertRes.status, detail);
    return NextResponse.json({ error: "가입 처리에 실패했습니다." }, { status: 502 });
  }

  const response = NextResponse.json({ ok: true });
  response.cookies.delete(PENDING_SIGNUP_COOKIE);
  return response;
}
