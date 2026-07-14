"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type ChangeEvent,
  type FormEvent,
  type KeyboardEvent,
} from "react";
import {
  AlertCircle,
  CheckCircle2,
  Loader2,
  Paperclip,
  RefreshCw,
  Send,
} from "lucide-react";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const ALLOWED_EXTENSIONS = [
  ".pdf",
  ".txt",
  ".md",
  ".docx",
  ".pptx",
  ".xlsx",
  ".csv",
  ".html",
  ".htm",
  ".json",
  ".sql",
];

function hasAllowedExtension(name: string) {
  const lower = name.toLowerCase();
  return ALLOWED_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

type RagUploadResponse = {
  filename: string;
  content_type: string;
  size_bytes: number;
  chunk_count: number;
  message: string;
};

type UploadStatus = "uploading" | "success" | "error";

type Message =
  | { id: string; role: "user"; text: string }
  | { id: string; role: "assistant"; text: string }
  | { id: string; role: "upload"; fileName: string; status: UploadStatus; text: string };

let messageSeq = 0;
function nextId() {
  messageSeq += 1;
  return `m${messageSeq}`;
}

export function RagPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isAsking, setIsAsking] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const lastUserRef = useRef("");
  const endRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const openFilePicker = () => fileInputRef.current?.click();

  const uploadFile = useCallback(async (file: File) => {
    if (!hasAllowedExtension(file.name)) {
      setMessages((prev) => [
        ...prev,
        {
          id: nextId(),
          role: "upload",
          fileName: file.name,
          status: "error",
          text: "지원하지 않는 형식입니다. pdf, txt, md, docx, pptx, xlsx, csv, html, json, sql 파일만 업로드할 수 있습니다.",
        },
      ]);
      return;
    }

    const id = nextId();
    setMessages((prev) => [
      ...prev,
      { id, role: "upload", fileName: file.name, status: "uploading", text: "업로드 중…" },
    ]);
    setIsUploading(true);

    const body = new FormData();
    body.append("file", file);

    try {
      const res = await fetch(`${apiBaseUrl}/rag/upload`, { method: "POST", body });
      if (!res.ok) {
        const msg = await res.text().catch(() => "");
        throw new Error(msg || `HTTP ${res.status}`);
      }
      const data = (await res.json()) as RagUploadResponse;
      setMessages((prev) =>
        prev.map((m) =>
          m.id === id
            ? { ...m, status: "success", text: data.message }
            : m,
        ),
      );
    } catch {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === id
            ? { ...m, status: "error", text: "업로드에 실패했습니다. 다시 시도해 주세요." }
            : m,
        ),
      );
    } finally {
      setIsUploading(false);
    }
  }, []);

  const onFileInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] ?? null;
    e.target.value = "";
    if (file) uploadFile(file);
  };

  const send = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isAsking) return;

    lastUserRef.current = trimmed;
    setErrorMessage(null);
    setIsAsking(true);

    const userMsg: Message = { id: nextId(), role: "user", text: trimmed };
    const thread = [...messages, userMsg];
    setMessages(thread);
    setInput("");

    try {
      const res = await fetch(`${apiBaseUrl}/rag/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: thread
            .filter((m): m is Extract<Message, { role: "user" | "assistant" }> =>
              m.role === "user" || m.role === "assistant",
            )
            .map((m) => ({ role: m.role, text: m.text })),
        }),
      });

      const data = (await res.json()) as { text?: string; reply?: string; error?: string };
      if (!res.ok) throw new Error(data.error ?? `요청 실패 (HTTP ${res.status})`);

      const answer = (data.text ?? data.reply ?? "").trim();
      if (!answer) throw new Error("빈 응답입니다.");

      setMessages((prev) => [...prev, { id: nextId(), role: "assistant", text: answer }]);
    } catch (err) {
      setMessages((prev) => prev.slice(0, -1));
      setInput(trimmed);
      setErrorMessage(
        err instanceof Error
          ? err.message
          : "질의응답에 실패했습니다. 백엔드 POST /rag/chat 으로 전송됩니다.",
      );
    } finally {
      setIsAsking(false);
      inputRef.current?.focus();
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    send(input);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send(input);
    }
  };

  return (
    <div className="w-full max-w-2xl flex flex-col items-center">
      <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-center mb-2">
        RAG 시스템
      </h1>
      <p className="text-sm text-gray-500 dark:text-gray-400 text-center mb-10 max-w-md">
        문서를 첨부하고 바로 질문하세요. pdf, txt, md, docx, pptx, xlsx, csv, html, json, sql 형식을 지원합니다.
      </p>

      <input
        ref={fileInputRef}
        type="file"
        accept={ALLOWED_EXTENSIONS.join(",")}
        className="sr-only"
        aria-hidden
        onChange={onFileInputChange}
      />

      <div className="w-full rounded-2xl border border-gray-200 dark:border-gray-800 bg-slate-50 dark:bg-gray-900">
        <div className="max-h-96 overflow-y-auto px-4 py-6">
          <div className="space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-10">
                <div className="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-950 mb-3">
                  <Paperclip size={22} className="text-blue-800 dark:text-blue-300" aria-hidden />
                </div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  📎 버튼으로 문서를 첨부하거나, 바로 질문해 보세요.
                </p>
              </div>
            )}

            {messages.map((msg) => {
              if (msg.role === "upload") {
                return (
                  <div key={msg.id} className="flex justify-center">
                    <div
                      className={[
                        "flex max-w-[90%] items-center gap-2 rounded-full border px-4 py-2 text-xs",
                        msg.status === "uploading" &&
                          "border-gray-200 bg-white text-gray-600 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300",
                        msg.status === "success" &&
                          "border-green-200 bg-green-50 text-green-900 dark:border-green-900 dark:bg-green-950 dark:text-green-300",
                        msg.status === "error" &&
                          "border-red-200 bg-red-50 text-red-900 dark:border-red-900 dark:bg-red-950 dark:text-red-300",
                      ]
                        .filter(Boolean)
                        .join(" ")}
                    >
                      {msg.status === "uploading" && (
                        <Loader2 size={14} className="shrink-0 animate-spin" aria-hidden />
                      )}
                      {msg.status === "success" && (
                        <CheckCircle2 size={14} className="shrink-0" aria-hidden />
                      )}
                      {msg.status === "error" && (
                        <AlertCircle size={14} className="shrink-0" aria-hidden />
                      )}
                      <span className="font-medium">{msg.fileName}</span>
                      <span className="text-gray-400 dark:text-gray-500">·</span>
                      <span>{msg.text}</span>
                    </div>
                  </div>
                );
              }

              return (
                <div
                  key={msg.id}
                  className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap break-words ${
                      msg.role === "user"
                        ? "bg-blue-900 text-white"
                        : "bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700 shadow-sm"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              );
            })}

            {isAsking && (
              <div className="flex gap-3 justify-start">
                <div className="rounded-2xl px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm">
                  <Loader2 size={18} className="animate-spin text-blue-800 dark:text-blue-300" aria-label="응답 대기 중" />
                </div>
              </div>
            )}

            <div ref={endRef} />
          </div>
        </div>

        <div className="border-t border-gray-200 dark:border-gray-800 px-4 py-4">
          {errorMessage && (
            <div className="mb-3 flex items-center justify-between gap-2 rounded-xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 px-4 py-2 text-sm text-red-700 dark:text-red-400">
              <div className="flex items-center gap-2 min-w-0">
                <AlertCircle size={15} className="shrink-0" aria-hidden />
                <span className="break-words">{errorMessage}</span>
              </div>
              <button
                type="button"
                onClick={() => { setErrorMessage(null); send(lastUserRef.current); }}
                className="shrink-0 inline-flex items-center gap-1 rounded-full border border-red-300 dark:border-red-700 bg-white dark:bg-gray-800 px-3 py-1 text-xs font-medium hover:bg-red-50 dark:hover:bg-red-900/30 transition-colors"
              >
                <RefreshCw size={12} aria-hidden />
                재시도
              </button>
            </div>
          )}

          <form
            onSubmit={handleSubmit}
            className="flex items-end gap-2 rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-950 px-4 py-3"
          >
            <button
              type="button"
              onClick={openFilePicker}
              disabled={isUploading}
              aria-label="문서 첨부"
              title="문서 첨부"
              className="shrink-0 inline-flex h-9 w-9 items-center justify-center rounded-full text-gray-500 hover:bg-gray-100 hover:text-gray-800 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              {isUploading ? (
                <Loader2 size={18} className="animate-spin" aria-hidden />
              ) : (
                <Paperclip size={18} aria-hidden />
              )}
            </button>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="질문을 입력하세요… (Enter로 전송)"
              rows={1}
              maxLength={2000}
              disabled={isAsking}
              className="flex-1 resize-none bg-transparent text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none disabled:opacity-50 min-h-[24px] max-h-32 leading-relaxed"
            />
            <button
              type="submit"
              disabled={!input.trim() || isAsking}
              aria-label="전송"
              className="shrink-0 inline-flex h-9 w-9 items-center justify-center rounded-full bg-blue-900 text-white hover:bg-blue-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              {isAsking ? (
                <Loader2 size={16} className="animate-spin" aria-hidden />
              ) : (
                <Send size={16} aria-hidden />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
