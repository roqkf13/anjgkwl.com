import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

const TOKEN_URL = "https://nid.naver.com/oauth2.0/token";
const PROFILE_URL = "https://openapi.naver.com/v1/nid/me";
const STATE_COOKIE = "naver_oauth_state";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

function redirectToLogin(req: NextRequest, status: "success" | "error", reason?: string) {
  const url = new URL("/login", req.url);
  url.searchParams.set("oauth", status);
  url.searchParams.set("provider", "naver");
  if (reason) url.searchParams.set("reason", reason);
  const response = NextResponse.redirect(url);
  response.cookies.delete(STATE_COOKIE);
  return response;
}

export async function GET(req: NextRequest) {
  const code = req.nextUrl.searchParams.get("code");
  const state = req.nextUrl.searchParams.get("state");
  const error = req.nextUrl.searchParams.get("error");
  const cookieState = req.cookies.get(STATE_COOKIE)?.value;

  if (error || !code || !state || state !== cookieState) {
    console.error("[naver-callback] state/code 검증 실패", {
      error,
      hasCode: !!code,
      hasState: !!state,
      stateMatches: state === cookieState,
    });
    return redirectToLogin(req, "error", "state_mismatch");
  }

  const clientId = process.env.NAVER_CLIENT_ID?.trim();
  const clientSecret = process.env.NAVER_CLIENT_SECRET?.trim();
  const redirectUri = process.env.NAVER_REDIRECT_URI?.trim();
  const internalSecret = process.env.INTERNAL_OAUTH_SECRET?.trim();

  if (!clientId || !clientSecret || !redirectUri || !internalSecret) {
    console.error("[naver-callback] 서버 환경변수 누락", {
      hasClientId: !!clientId,
      hasClientSecret: !!clientSecret,
      hasRedirectUri: !!redirectUri,
      hasInternalSecret: !!internalSecret,
    });
    return redirectToLogin(req, "error", "missing_env");
  }

  try {
    const tokenParams = new URLSearchParams({
      grant_type: "authorization_code",
      client_id: clientId,
      client_secret: clientSecret,
      redirect_uri: redirectUri,
      code,
      state,
    });
    const tokenRes = await fetch(`${TOKEN_URL}?${tokenParams.toString()}`);
    const tokenJson = (await tokenRes.json()) as { access_token?: string; error?: string; error_description?: string };
    if (!tokenRes.ok || !tokenJson.access_token) {
      console.error("[naver-callback] 토큰 교환 실패", tokenRes.status, tokenJson);
      return redirectToLogin(req, "error", "token_exchange");
    }

    const profileRes = await fetch(PROFILE_URL, {
      headers: { Authorization: `Bearer ${tokenJson.access_token}` },
    });
    const profileJson = (await profileRes.json()) as {
      resultcode?: string;
      message?: string;
      response?: { id?: string; email?: string; name?: string; nickname?: string };
    };
    const profile = profileJson.response;
    if (!profileRes.ok || profileJson.resultcode !== "00" || !profile?.id) {
      console.error("[naver-callback] 프로필 조회 실패", profileRes.status, profileJson);
      return redirectToLogin(req, "error", "profile_fetch");
    }

    const email = (profile.email ?? "").trim().toLowerCase();
    const name = profile.name || profile.nickname || email || profile.id;
    if (!email) {
      console.error("[naver-callback] 이메일 없음", profile);
      return redirectToLogin(req, "error", "no_email");
    }

    const upsertRes = await fetch(`${apiBaseUrl}/auth/oauth/upsert`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-internal-secret": internalSecret,
      },
      body: JSON.stringify({
        provider: "naver",
        oauth_id: profile.id,
        email,
        name,
      }),
    });
    if (!upsertRes.ok) {
      const upsertBody = await upsertRes.text();
      console.error("[naver-callback] 백엔드 upsert 실패", upsertRes.status, upsertBody);
      return redirectToLogin(req, "error", "upsert_failed");
    }
  } catch (err) {
    console.error("[naver-callback] 예외 발생", err);
    return redirectToLogin(req, "error", "exception");
  }

  return redirectToLogin(req, "success");
}
