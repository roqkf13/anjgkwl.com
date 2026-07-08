import { VisionUploadPanel } from "@/components/vision-upload-panel";
import { FaceRecognitionPanel } from "@/components/face-recognition-panel";

export default function VisionPage() {
  return (
    <main className="flex-1 flex flex-col items-center min-h-0 px-4 py-10 overflow-y-auto">
      <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-gray-500 dark:text-gray-400">
        Lesson · 비전 처리
      </p>
      <VisionUploadPanel />
      <FaceRecognitionPanel />
    </main>
  );
}
