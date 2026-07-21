import { NextResponse } from "next/server";
import crypto from "crypto";

export const runtime = "nodejs";

const AUTHORIZE_URL = "https://nid.naver.com/oauth2.0/authorize";
const STATE_COOKIE = "naver_oauth_state";

export async function GET() {
  const clientId = process.env.NAVER_CLIENT_ID?.trim();
  const redirectUri = process.env.NAVER_REDIRECT_URI?.trim();

  if (!clientId || !redirectUri) {
    return NextResponse.json(
      { error: "서버에 NAVER_CLIENT_ID / NAVER_REDIRECT_URI 가 설정되지 않았습니다." },
      { status: 503 }
    );
  }

  const state = crypto.randomBytes(16).toString("hex");
  const params = new URLSearchParams({
    response_type: "code",
    client_id: clientId,
    redirect_uri: redirectUri,
    state,
  });

  const response = NextResponse.redirect(`${AUTHORIZE_URL}?${params.toString()}`);
  response.cookies.set(STATE_COOKIE, state, {
    httpOnly: true,
    sameSite: "lax",
    maxAge: 300,
    path: "/",
  });
  return response;
}
