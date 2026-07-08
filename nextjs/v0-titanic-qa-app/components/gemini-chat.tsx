"use client";

import { useState, useRef, useEffect, FormEvent, KeyboardEvent } from "react";
import {
  Plus,
  ChevronDown,
  Mic,
  Loader2,
  AlertCircle,
  RefreshCw,
} from "lucide-react";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const GEMINI_MODELS = [
  { value: "flash", label: "Flash" },
  { value: "pro", label: "Pro" },
] as const;

function parseChatError(data: unknown, status: number): string {
  if (data && typeof data === "object") {
    const obj = data as Record<string, unknown>;
    if (typeof obj.error === "string") return obj.error;
    const detail = obj.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      return detail
        .map((item) =>
          typeof item === "object" && item && "msg" in item
            ? String((item as { msg: unknown }).msg)
            : String(item),
        )
        .join(", ");
    }
  }
  return `요청 실패 (HTTP ${status})`;
}

interface GeminiMessage {
  role: "user" | "assistant";
  text: string;
  ts: string;
}

type ChatUiState = {
  input: string;
  isLoading: boolean;
  errorMessage: string | null;
  model: (typeof GEMINI_MODELS)[number]["value"];
};

const initialChatUi: ChatUiState = {
  input: "",
  isLoading: false,
  errorMessage: null,
  model: "flash",
};

export function GeminiChat() {
  const [messages, setMessages] = useState<GeminiMessage[]>([]);
  const [ui, setUi] = useState<ChatUiState>(initialChatUi);
  const lastUserRef = useRef<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const hasMessages = messages.length > 0;

  useEffect(() => {
    if (hasMessages) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, hasMessages]);

  const send = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || ui.isLoading) return;

    lastUserRef.current = trimmed;
    setUi((prev) => ({ ...prev, errorMessage: null, isLoading: true }));

    const userMsg: GeminiMessage = {
      role: "user",
      text: trimmed,
      ts: new Date().toISOString(),
    };
    const nextThread = [...messages, userMsg];
    setMessages(nextThread);
    setUi((prev) => ({ ...prev, input: "" }));

    try {
      const res = await fetch(`${apiBaseUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: nextThread.map((m) => ({ role: m.role, text: m.text })),
        }),
      });

      const data = (await res.json()) as {
        text?: string;
        reply?: string;
        error?: string;
        detail?: string | unknown[];
      };
      if (!res.ok) {
        throw new Error(parseChatError(data, res.status));
      }

      const answer = (data.text ?? data.reply ?? "").trim();
      if (!answer) {
        throw new Error("빈 응답입니다.");
      }

      const assistantMsg: GeminiMessage = {
        role: "assistant",
        text: answer,
        ts: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => prev.slice(0, -1));
      setUi((prev) => ({
        ...prev,
        input: trimmed,
        errorMessage:
          err instanceof Error ? err.message : "요청에 실패했습니다.",
      }));
    } finally {
      setUi((prev) => ({ ...prev, isLoading: false }));
      inputRef.current?.focus();
    }
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    send(ui.input);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send(ui.input);
    }
  };

  const handleRetry = () => {
    if (lastUserRef.current) {
      setUi((prev) => ({ ...prev, errorMessage: null }));
      send(lastUserRef.current);
    }
  };

  return (
    <div className="flex flex-1 flex-col min-h-0 bg-[radial-gradient(ellipse_at_center_bottom,_#dbeafe_0%,_#f8fafc_45%,_#ffffff_100%)] dark:bg-[radial-gradient(ellipse_at_center_bottom,_#1e293b_0%,_#0f172a_55%,_#020617_100%)]">
      {hasMessages && (
        <div className="flex-1 overflow-y-auto px-4 py-8 min-h-0">
          <div className="max-w-3xl mx-auto space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={`${msg.ts}-${idx}`}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] rounded-3xl px-5 py-3 ${
                    msg.role === "user"
                      ? "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      : "bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 shadow-sm border border-gray-100 dark:border-gray-800"
                  }`}
                >
                  <p className="text-[15px] leading-relaxed whitespace-pre-wrap break-words">
                    {msg.text}
                  </p>
                </div>
              </div>
            ))}

            {ui.isLoading && (
              <div className="flex justify-start">
                <div className="rounded-3xl px-5 py-3 bg-white dark:bg-gray-900 shadow-sm border border-gray-100 dark:border-gray-800">
                  <Loader2
                    size={20}
                    className="animate-spin text-blue-500"
                    aria-label="Gemini 응답 대기 중"
                  />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      <div
        className={`flex flex-col items-center px-4 sm:px-6 w-full ${
          hasMessages
            ? "pb-8 pt-2 shrink-0"
            : "flex-1 justify-center pb-16"
        }`}
      >
        {ui.errorMessage && (
          <div className="w-full max-w-2xl mb-3 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-2xl flex items-center justify-between gap-2">
            <div className="flex items-center gap-2 text-red-700 dark:text-red-400 text-sm min-w-0">
              <AlertCircle size={16} className="shrink-0" aria-hidden />
              <span className="break-words">{ui.errorMessage}</span>
            </div>
            <button
              type="button"
              onClick={handleRetry}
              className="shrink-0 inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-full border border-red-300 dark:border-red-700 bg-white dark:bg-gray-800 text-red-700 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 transition-colors"
            >
              <RefreshCw size={14} aria-hidden />
              재시도
            </button>
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="w-full max-w-2xl rounded-full bg-white dark:bg-gray-900 shadow-[0_2px_12px_rgba(0,0,0,0.08)] dark:shadow-[0_2px_12px_rgba(0,0,0,0.35)] border border-gray-100 dark:border-gray-800 flex items-center gap-1 pl-3 pr-2 py-2"
        >
          <button
            type="button"
            aria-label="첨부 추가"
            className="shrink-0 inline-flex items-center justify-center w-9 h-9 rounded-full text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <Plus size={20} strokeWidth={1.75} aria-hidden />
          </button>

          <label htmlFor="gemini-input" className="sr-only">
            Gemini 에게 물어보기
          </label>
          <textarea
            ref={inputRef}
            id="gemini-input"
            name="message"
            value={ui.input}
            onChange={(e) =>
              setUi((prev) => ({ ...prev, input: e.target.value }))
            }
            onKeyDown={handleKeyDown}
            placeholder="Gemini에게 물어보기"
            maxLength={4000}
            rows={1}
            disabled={ui.isLoading}
            className="flex-1 resize-none bg-transparent px-1 py-2 text-[15px] text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none disabled:opacity-50 min-h-[40px] max-h-32 leading-relaxed"
          />

          <div className="relative shrink-0">
            <select
              aria-label="Gemini 모델 선택"
              value={ui.model}
              disabled={ui.isLoading}
              onChange={(e) =>
                setUi((prev) => ({
                  ...prev,
                  model: e.target.value as ChatUiState["model"],
                }))
              }
              className="appearance-none pl-3 pr-7 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-transparent hover:bg-gray-50 dark:hover:bg-gray-800 rounded-full cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 disabled:opacity-50"
            >
              {GEMINI_MODELS.map((m) => (
                <option key={m.value} value={m.value}>
                  {m.label}
                </option>
              ))}
            </select>
            <ChevronDown
              size={16}
              className="pointer-events-none absolute right-1.5 top-1/2 -translate-y-1/2 text-gray-500"
              aria-hidden
            />
          </div>

          <button
            type={ui.input.trim() ? "submit" : "button"}
            disabled={ui.isLoading}
            aria-label={ui.input.trim() ? "전송" : "음성 입력"}
            className="shrink-0 inline-flex items-center justify-center w-10 h-10 rounded-full text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
          >
            {ui.isLoading ? (
              <Loader2 size={20} className="animate-spin" aria-hidden />
            ) : (
              <Mic size={20} strokeWidth={1.75} aria-hidden />
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
