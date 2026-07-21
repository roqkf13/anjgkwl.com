import crypto from "crypto";

export const PENDING_SIGNUP_COOKIE = "naver_pending_signup";
export const PENDING_SIGNUP_TTL_MS = 10 * 60 * 1000;

export type PendingOAuthProfile = {
  provider: "naver";
  oauthId: string;
  email: string;
  name: string;
  issuedAt: number;
};

function getSecret(): string {
  const secret = process.env.INTERNAL_OAUTH_SECRET?.trim();
  if (!secret) throw new Error("INTERNAL_OAUTH_SECRET이 설정되지 않았습니다.");
  return secret;
}

function sign(payload: string): string {
  return crypto.createHmac("sha256", getSecret()).update(payload).digest("base64url");
}

export function signPendingProfile(profile: PendingOAuthProfile): string {
  const payload = Buffer.from(JSON.stringify(profile), "utf8").toString("base64url");
  return `${payload}.${sign(payload)}`;
}

export function verifyPendingProfile(cookieValue: string | undefined): PendingOAuthProfile | null {
  if (!cookieValue) return null;
  const [payload, signature] = cookieValue.split(".");
  if (!payload || !signature) return null;

  const expected = sign(payload);
  const a = Buffer.from(signature);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;

  try {
    const profile = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")) as PendingOAuthProfile;
    if (Date.now() - profile.issuedAt > PENDING_SIGNUP_TTL_MS) return null;
    return profile;
  } catch {
    return null;
  }
}
