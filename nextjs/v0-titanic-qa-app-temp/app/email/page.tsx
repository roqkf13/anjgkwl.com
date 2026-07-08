"use client";

import { useState, useRef, useCallback, useEffect, type DragEvent, type ChangeEvent, type FormEvent } from "react";
import { Mail, Loader2, CheckCircle, AlertCircle, BookUser, Upload, FolderOpen, CheckCircle2, X, Inbox } from "lucide-react";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type Tab = "mail" | "contacts" | "inbox";
type SendStatus = { type: "idle" } | { type: "loading" } | { type: "success"; subject: string; to: string } | { type: "error"; message: string };
type Feedback = { kind: "success" | "error" | "info"; text: string };

// ────────── 주소록 업로드 모달 ──────────
function ContactUploadModal({ onClose, onUploaded }: { onClose: () => void; onUploaded?: () => void }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [mode, setMode] = useState<"replace" | "upsert">("replace");

  const pickFile = useCallback((f: File | null) => {
    setFeedback(null);
    if (!f) { setFile(null); return; }
    if (!f.name.toLowerCase().endsWith(".csv")) {
      setFile(null);
      setFeedback({ kind: "error", text: "CSV 파일만 선택할 수 있습니다." });
      return;
    }
    setFile(f);
    setFeedback({ kind: "info", text: `선택됨: ${f.name} (${(f.size / 1024).toFixed(1)} KB)` });
  }, []);

  const onInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    pickFile(e.target.files?.[0] ?? null);
    e.target.value = "";
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    pickFile(e.dataTransfer.files?.[0] ?? null);
  };

  const upload = async () => {
    if (!file) return;
    setUploading(true);
    setFeedback(null);
    const body = new FormData();
    body.append("file", file);
    try {
      const res = await fetch(`${apiBaseUrl}/sherlock-homes/watson/contacts/upload?mode=${mode}`, { method: "POST", body });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setFeedback({ kind: "success", text: `업로드 완료 (${data.total ?? 0}건)` });
      setFile(null);
      onUploaded?.();
    } catch {
      setFeedback({ kind: "error", text: "업로드에 실패했습니다." });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="relative w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-6">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
        >
          <X size={20} />
        </button>

        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">주소록 등록</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
          CSV 파일을 업로드하세요. (이름, 이메일 컬럼 포함)
        </p>

        <div className="flex gap-2 mb-5">
          <button
            type="button"
            onClick={() => setMode("replace")}
            className={["flex-1 py-2 rounded-lg text-sm font-medium border transition-colors",
              mode === "replace"
                ? "bg-blue-600 text-white border-blue-600"
                : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:bg-gray-50",
            ].join(" ")}
          >
            전체 교체
          </button>
          <button
            type="button"
            onClick={() => setMode("upsert")}
            className={["flex-1 py-2 rounded-lg text-sm font-medium border transition-colors",
              mode === "upsert"
                ? "bg-blue-600 text-white border-blue-600"
                : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:bg-gray-50",
            ].join(" ")}
          >
            누적 추가
          </button>
        </div>
        <p className="text-xs text-gray-400 dark:text-gray-500 mb-4">
          {mode === "replace" ? "기존 주소록을 전부 삭제하고 CSV로 새로 등록합니다." : "기존 주소록은 유지하고, 이메일 기준으로 없으면 추가·있으면 업데이트합니다."}
        </p>

        <input ref={inputRef} type="file" accept=".csv,text/csv" className="sr-only" onChange={onInputChange} />

        <div
          role="button"
          tabIndex={0}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); inputRef.current?.click(); } }}
          onDrop={onDrop}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={(e) => { e.preventDefault(); setDragOver(false); }}
          className={[
            "w-full rounded-2xl border-2 border-dashed px-6 py-12 text-center cursor-pointer transition-colors outline-none focus-visible:ring-2 focus-visible:ring-blue-500",
            dragOver ? "border-blue-500 bg-blue-50/80" : "border-gray-300 bg-gray-50/80 hover:border-gray-400",
          ].join(" ")}
        >
          <Upload className="mx-auto mb-4 text-gray-400" size={36} strokeWidth={1.5} />
          <p className="text-sm font-medium text-gray-800 dark:text-gray-200 mb-1">업로드 창</p>
          <p className="text-xs text-gray-500">CSV 파일을 끌어다 놓거나 클릭해 선택하세요.</p>
        </div>

        <div className="flex items-center justify-center gap-3 mt-5">
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-xl border border-gray-300 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-50 transition-colors"
          >
            <FolderOpen size={16} /> 파일 선택
          </button>
          <button
            type="button"
            disabled={!file || uploading}
            onClick={upload}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-xl border border-blue-600 bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? <Loader2 size={16} className="animate-spin" /> : <Upload size={16} />}
            업로드
          </button>
        </div>

        {feedback && (
          <div className={[
            "mt-4 flex items-start gap-2 rounded-xl border px-4 py-3 text-sm",
            feedback.kind === "success" && "border-green-200 bg-green-50 text-green-900",
            feedback.kind === "error" && "border-red-200 bg-red-50 text-red-900",
            feedback.kind === "info" && "border-gray-200 bg-gray-50 text-gray-800",
          ].filter(Boolean).join(" ")}>
            {feedback.kind === "success" && <CheckCircle2 size={16} className="shrink-0 text-green-600 mt-0.5" />}
            {feedback.kind === "error" && <AlertCircle size={16} className="shrink-0 text-red-600 mt-0.5" />}
            {feedback.kind === "info" && <CheckCircle2 size={16} className="shrink-0 text-gray-500 mt-0.5" />}
            <span>{feedback.text}</span>
          </div>
        )}
      </div>
    </div>
  );
}

type ContactItem = { first_name: string; last_name: string; nickname: string; e_mail_1_value: string; organization_name: string };
type ReceivedEmail = { id: string; gmail_id: string; thread_id: string | null; from_: string | null; to: string | null; subject: string | null; snippet: string | null };

// ────────── 메인 페이지 ──────────
export default function EmailPage() {
  const [tab, setTab] = useState<Tab>("mail");
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [contacts, setContacts] = useState<ContactItem[]>([]);
  const [receivedEmails, setReceivedEmails] = useState<ReceivedEmail[]>([]);
  const [inboxLoading, setInboxLoading] = useState(false);

  const fetchContacts = useCallback(async () => {
    const res = await fetch(`${apiBaseUrl}/sherlock-homes/watson/contacts`);
    if (!res.ok) return;
    const data = await res.json();
    setContacts(data.contacts ?? []);
  }, []);

  const fetchReceivedEmails = useCallback(async () => {
    setInboxLoading(true);
    try {
      const res = await fetch(`${apiBaseUrl}/sherlock-homes/watson/emails`);
      if (!res.ok) return;
      const data = await res.json();
      setReceivedEmails(data.emails ?? []);
    } finally {
      setInboxLoading(false);
    }
  }, []);

  useEffect(() => {
    if (tab === "contacts") fetchContacts();
    if (tab === "inbox") fetchReceivedEmails();
  }, [tab, fetchContacts, fetchReceivedEmails]);

  // 메일 발송 폼 상태
  const [to, setTo] = useState("");
  const [prompt, setPrompt] = useState("");
  const [fromAccount, setFromAccount] = useState("");
  const [status, setStatus] = useState<SendStatus>({ type: "idle" });

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setStatus({ type: "loading" });
    try {
      const res = await fetch(`${apiBaseUrl}/sherlock-homes/watson/send-email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ to, prompt, from_account: fromAccount }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        const msg = typeof data?.detail === "string" ? data.detail : `요청 실패 (HTTP ${res.status})`;
        setStatus({ type: "error", message: msg });
        return;
      }
      const data = await res.json();
      setStatus({ type: "success", subject: data.subject, to: data.to });
    } catch (err) {
      setStatus({ type: "error", message: err instanceof Error ? err.message : "네트워크 오류" });
    }
  }

  return (
    <div className="flex flex-1 min-h-0">
      {/* 사이드바 */}
      <aside className="w-48 shrink-0 border-r border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 flex flex-col pt-6">
        <nav className="flex flex-col gap-1 px-3">
          <button
            onClick={() => setTab("mail")}
            className={[
              "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-left",
              tab === "mail"
                ? "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400"
                : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800",
            ].join(" ")}
          >
            <Mail size={16} />
            메일 관리
          </button>
          <button
            onClick={() => setTab("contacts")}
            className={[
              "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-left",
              tab === "contacts"
                ? "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400"
                : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800",
            ].join(" ")}
          >
            <BookUser size={16} />
            주소록
          </button>
          <button
            onClick={() => setTab("inbox")}
            className={[
              "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-left",
              tab === "inbox"
                ? "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400"
                : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800",
            ].join(" ")}
          >
            <Inbox size={16} />
            받은 메일함
          </button>
        </nav>
      </aside>

      {/* 콘텐츠 영역 */}
      <main className="flex-1 flex flex-col min-h-0 overflow-y-auto">
        {tab === "mail" && (
          <div className="flex flex-col items-center justify-center flex-1 p-6">
            <div className="w-full max-w-lg">
              <div className="flex items-center gap-2 mb-6">
                <Mail size={24} className="text-blue-500" />
                <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">AI 메일 발송</h1>
              </div>

              <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <div className="flex flex-col gap-1.5">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">발신자 계정</label>
                  <input
                    type="email" required value={fromAccount}
                    onChange={(e) => setFromAccount(e.target.value)}
                    placeholder="sender@gmail.com"
                    className="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="flex flex-col gap-1.5">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">수신자</label>
                  <input
                    type="email" required value={to}
                    onChange={(e) => setTo(e.target.value)}
                    placeholder="recipient@example.com"
                    className="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="flex flex-col gap-1.5">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">메일 작성 지시</label>
                  <textarea
                    required value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="예: 프로젝트 일정 변경 안내 메일을 정중하게 작성해줘"
                    rows={4}
                    className="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  />
                  <p className="text-xs text-gray-500 dark:text-gray-400">EXAONE이 제목과 본문을 자동 생성합니다</p>
                </div>
                <button
                  type="submit" disabled={status.type === "loading"}
                  className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium transition-colors"
                >
                  {status.type === "loading" ? (
                    <><Loader2 size={16} className="animate-spin" />EXAONE 작성 중...</>
                  ) : (
                    <><Mail size={16} />발송</>
                  )}
                </button>
              </form>

              {status.type === "success" && (
                <div className="mt-4 flex items-start gap-2 p-3 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                  <CheckCircle size={16} className="text-green-600 dark:text-green-400 mt-0.5 shrink-0" />
                  <div className="text-sm text-green-800 dark:text-green-300">
                    <p className="font-medium">발송 완료</p>
                    <p className="mt-0.5">수신자: {status.to}</p>
                    <p>제목: {status.subject}</p>
                  </div>
                </div>
              )}
              {status.type === "error" && (
                <div className="mt-4 flex items-start gap-2 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                  <AlertCircle size={16} className="text-red-600 dark:text-red-400 mt-0.5 shrink-0" />
                  <p className="text-sm text-red-800 dark:text-red-300">{status.message}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {tab === "contacts" && (
          <div className="flex flex-col flex-1 p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2">
                <BookUser size={22} className="text-blue-500" />
                <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">주소록</h1>
              </div>
              <button
                onClick={() => setShowUploadModal(true)}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium transition-colors"
              >
                <Upload size={15} />
                등록
              </button>
            </div>

            {/* 주소록 목록 (추후 API 연동) */}
            <div className="flex-1 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">이름</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">이메일</th>
                  </tr>
                </thead>
                <tbody>
                  {contacts.length === 0 ? (
                    <tr>
                      <td colSpan={2} className="px-4 py-12 text-center text-sm text-gray-400 dark:text-gray-500">
                        등록된 주소록이 없습니다. 우측 상단 등록 버튼으로 CSV를 업로드하세요.
                      </td>
                    </tr>
                  ) : (
                    contacts.map((c, i) => (
                      <tr key={i} className="border-t border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                        <td className="px-4 py-3 text-gray-900 dark:text-gray-100">
                          {[c.first_name, c.last_name].filter(Boolean).join(" ") || c.nickname || "-"}
                        </td>
                        <td className="px-4 py-3 text-gray-600 dark:text-gray-400">{c.e_mail_1_value || "-"}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
        {tab === "inbox" && (
          <div className="flex flex-col flex-1 p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2">
                <Inbox size={22} className="text-blue-500" />
                <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">받은 메일함</h1>
              </div>
              <button
                onClick={fetchReceivedEmails}
                disabled={inboxLoading}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50 transition-colors"
              >
                {inboxLoading ? <Loader2 size={14} className="animate-spin" /> : null}
                새로고침
              </button>
            </div>

            <div className="flex-1 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide w-48">발신자</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide w-56">제목</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">내용 미리보기</th>
                  </tr>
                </thead>
                <tbody>
                  {inboxLoading ? (
                    <tr>
                      <td colSpan={3} className="px-4 py-12 text-center text-sm text-gray-400">
                        <Loader2 size={20} className="animate-spin mx-auto" />
                      </td>
                    </tr>
                  ) : receivedEmails.length === 0 ? (
                    <tr>
                      <td colSpan={3} className="px-4 py-12 text-center text-sm text-gray-400 dark:text-gray-500">
                        받은 메일이 없습니다.
                      </td>
                    </tr>
                  ) : (
                    receivedEmails.map((email) => (
                      <tr key={email.id} className="border-t border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                        <td className="px-4 py-3 text-gray-900 dark:text-gray-100 truncate max-w-0 w-48">
                          <span className="block truncate">{email.from_ ?? "-"}</span>
                        </td>
                        <td className="px-4 py-3 text-gray-900 dark:text-gray-100 truncate max-w-0 w-56">
                          <span className="block truncate font-medium">{email.subject ?? "(제목 없음)"}</span>
                        </td>
                        <td className="px-4 py-3 text-gray-500 dark:text-gray-400 truncate max-w-0">
                          <span className="block truncate">{email.snippet ?? ""}</span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {showUploadModal && (
        <ContactUploadModal
          onClose={() => setShowUploadModal(false)}
          onUploaded={fetchContacts}
        />
      )}
    </div>
  );
}
