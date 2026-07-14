import { RagDocumentUploadPanel } from "@/components/rag-document-upload-panel";
import { RagChatPanel } from "@/components/rag-chat-panel";

export default function RagPage() {
  return (
    <main className="flex-1 flex flex-col items-center min-h-0 px-4 py-10 overflow-y-auto">
      <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-gray-500 dark:text-gray-400">
        Lesson · RAG 시스템
      </p>
      <RagDocumentUploadPanel />
      <RagChatPanel />
    </main>
  );
}
