"use client";

import { useState, useRef, useEffect, FormEvent, KeyboardEvent } from "react";
import { Send, Loader2, AlertCircle, RefreshCw, Anchor } from "lucide-react";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

// 스미스 선장 페르소나를 주입하는 숨겨진 시스템 컨텍스트
const SMITH_SYSTEM_CONTEXT = [
  {
    role: "user" as const,
    text: "지금부터 당신은 타이타닉의 선장 에드워드 존 스미스(Edward John Smith) 역할을 맡아주세요. 1912년 4월 14일 밤, 빙산과 충돌하기 직전의 상황입니다. 항상 선장의 말투와 시각으로 답변해 주세요.",
  },
  {
    role: "assistant" as const,
    text: "알겠습니다. 저는 타이타닉의 선장 에드워드 존 스미스입니다. 1912년 4월, 이 위대한 선박과 함께 대서양을 항해하고 있습니다. 무엇이든 물어보십시오.",
  },
];

interface Message {
  role: "user" | "assistant";
  text: string;
  ts: string;
}

export default function SmithChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const lastUserRef = useRef("");
  const endRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    lastUserRef.current = trimmed;
    setErrorMessage(null);
    setIsLoading(true);

    const userMsg: Message = { role: "user", text: trimmed, ts: new Date().toISOString() };
    const thread = [...messages, userMsg];
    setMessages(thread);
    setInput("");

    try {
      const res = await fetch(`${apiBaseUrl}/titanic/smith/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [
            ...SMITH_SYSTEM_CONTEXT,
            ...thread.map((m) => ({ role: m.role, text: m.text })),
          ],
        }),
      });

      const data = (await res.json()) as { text?: string; reply?: string; error?: string };
      if (!res.ok) throw new Error(data.error ?? `요청 실패 (HTTP ${res.status})`);

      const answer = (data.text ?? data.reply ?? "").trim();
      if (!answer) throw new Error("빈 응답입니다.");

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: answer, ts: new Date().toISOString() },
      ]);
    } catch (err) {
      setMessages((prev) => prev.slice(0, -1));
      setInput(trimmed);
      setErrorMessage(err instanceof Error ? err.message : "요청에 실패했습니다.");
    } finally {
      setIsLoading(false);
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
    <main className="flex flex-1 flex-col min-h-0">
      {/* 헤더 */}
      <div className="shrink-0 px-6 sm:px-10 py-6 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950">
        <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-gray-500 dark:text-gray-400">
          Lesson · 4. 스미스 선장과 대화
        </p>
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-900 text-white shrink-0">
            <Anchor size={20} aria-hidden />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
              선장 에드워드 존 스미스
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              1912년 4월 14일 · RMS 타이타닉
            </p>
          </div>
        </div>
      </div>

      {/* 메시지 영역 */}
      <div className="flex-1 overflow-y-auto px-4 py-6 min-h-0 bg-slate-50 dark:bg-gray-900">
        <div className="max-w-2xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-16">
              <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-950 mb-4">
                <Anchor size={28} className="text-blue-800 dark:text-blue-300" aria-hidden />
              </div>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                스미스 선장에게 질문해 보세요.
              </p>
              <p className="mt-1 text-xs text-gray-400 dark:text-gray-600">
                예: "선장님, 빙산 경고를 받으셨나요?"
              </p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={`${msg.ts}-${idx}`}
              className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role === "assistant" && (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-900 text-white mt-1">
                  <Anchor size={14} aria-hidden />
                </div>
              )}
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
          ))}

          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-900 text-white mt-1">
                <Anchor size={14} aria-hidden />
              </div>
              <div className="rounded-2xl px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm">
                <Loader2 size={18} className="animate-spin text-blue-800 dark:text-blue-300" aria-label="응답 대기 중" />
              </div>
            </div>
          )}

          <div ref={endRef} />
        </div>
      </div>

      {/* 입력 영역 */}
      <div className="shrink-0 px-4 py-4 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950">
        <div className="max-w-2xl mx-auto">
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
            className="flex items-end gap-2 rounded-2xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 px-4 py-3"
          >
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="선장님께 질문하세요… (Enter로 전송)"
              rows={1}
              maxLength={2000}
              disabled={isLoading}
              className="flex-1 resize-none bg-transparent text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none disabled:opacity-50 min-h-[24px] max-h-32 leading-relaxed"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              aria-label="전송"
              className="shrink-0 inline-flex h-9 w-9 items-center justify-center rounded-full bg-blue-900 text-white hover:bg-blue-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <Loader2 size={16} className="animate-spin" aria-hidden />
              ) : (
                <Send size={16} aria-hidden />
              )}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
