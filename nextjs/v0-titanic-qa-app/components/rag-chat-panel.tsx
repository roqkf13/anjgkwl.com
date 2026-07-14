"use client";

import { useState, useRef, useEffect, type FormEvent, type KeyboardEvent } from "react";
import { Send, Loader2, AlertCircle, RefreshCw, MessageSquare } from "lucide-react";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

interface Message {
  role: "user" | "assistant";
  text: string;
  ts: string;
}

export function RagChatPanel() {
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
      const res = await fetch(`${apiBaseUrl}/rag/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: thread.map((m) => ({ role: m.role, text: m.text })),
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
      setErrorMessage(
        err instanceof Error
          ? err.message
          : "질의응답에 실패했습니다. 백엔드 POST /rag/chat 으로 전송됩니다.",
      );
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
    <div className="mt-16 w-full max-w-2xl flex flex-col items-center">
      <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-center mb-2">
        질의응답
      </h2>
      <p className="text-sm text-gray-500 text-center mb-8 max-w-md">
        업로드한 문서 내용을 바탕으로 질문에 답변합니다.
      </p>

      <div className="w-full rounded-2xl border border-gray-200 dark:border-gray-800 bg-slate-50 dark:bg-gray-900">
        <div className="max-h-96 overflow-y-auto px-4 py-6">
          <div className="space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-10">
                <div className="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-950 mb-3">
                  <MessageSquare size={24} className="text-blue-800 dark:text-blue-300" aria-hidden />
                </div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  문서 내용에 대해 질문해 보세요.
                </p>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div
                key={`${msg.ts}-${idx}`}
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
            ))}

            {isLoading && (
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
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="문서 내용에 대해 질문하세요… (Enter로 전송)"
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
    </div>
  );
}
