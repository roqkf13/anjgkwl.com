export const OAUTH_RESULT_STORAGE_KEY = "titanic_qa_oauth_result";

export type OAuthResult = {
  status: "success" | "error";
  provider: string;
  reason?: string;
  ts: number;
};
