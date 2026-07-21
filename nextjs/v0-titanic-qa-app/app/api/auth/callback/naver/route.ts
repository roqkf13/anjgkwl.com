import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

const TOKEN_URL = "https://nid.naver.com/oauth2.0/token";
const PROFILE_URL = "https://openapi.naver.com/v1/nid/me";
const STATE_COOKIE = "naver_oauth_state";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

function redirectToLogin(req: NextRequest, status: "success" | "error") {
  const url = new URL("/login", req.url);
  url.searchParams.set("oauth", status);
  url.searchParams.set("provider", "naver");
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
    return redirectToLogin(req, "error");
  }

  const clientId = process.env.NAVER_CLIENT_ID?.trim();
  const clientSecret = process.env.NAVER_CLIENT_SECRET?.trim();
  const redirectUri = process.env.NAVER_REDIRECT_URI?.trim();
  const internalSecret = process.env.INTERNAL_OAUTH_SECRET?.trim();

  if (!clientId || !clientSecret || !redirectUri || !internalSecret) {
    return redirectToLogin(req, "error");
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
    if (!tokenRes.ok) return redirectToLogin(req, "error");
    const tokenJson = (await tokenRes.json()) as { access_token?: string };
    if (!tokenJson.access_token) return redirectToLogin(req, "error");

    const profileRes = await fetch(PROFILE_URL, {
      headers: { Authorization: `Bearer ${tokenJson.access_token}` },
    });
    if (!profileRes.ok) return redirectToLogin(req, "error");
    const profileJson = (await profileRes.json()) as {
      resultcode?: string;
      response?: { id?: string; email?: string; name?: string; nickname?: string };
    };
    const profile = profileJson.response;
    if (profileJson.resultcode !== "00" || !profile?.id) {
      return redirectToLogin(req, "error");
    }

    const email = (profile.email ?? "").trim().toLowerCase();
    const name = profile.name || profile.nickname || email || profile.id;
    if (!email) return redirectToLogin(req, "error");

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
    if (!upsertRes.ok) return redirectToLogin(req, "error");
  } catch {
    return redirectToLogin(req, "error");
  }

  return redirectToLogin(req, "success");
}
