"use client";

import { useCallback, useEffect, useRef, useState, type DragEvent, type ChangeEvent } from "react";
import { Upload, FolderOpen, Loader2, AlertCircle, ScanFace } from "lucide-react";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const ALLOWED_TYPES = ["image/jpeg", "image/png"];

type Feedback = {
  kind: "error" | "info";
  text: string;
};

type UploadUiState = {
  dragOver: boolean;
  uploading: boolean;
  feedback: Feedback | null;
};

type FaceRecognitionResponse = {
  name: string;
  confidence: number;
};

const initialUploadUi: UploadUiState = {
  dragOver: false,
  uploading: false,
  feedback: null,
};

export function FaceRecognitionPanel() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [ui, setUi] = useState<UploadUiState>(initialUploadUi);
  const [result, setResult] = useState<FaceRecognitionResponse | null>(null);

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const pickFile = useCallback((f: File | null) => {
    setUi((prev) => ({ ...prev, feedback: null }));
    setResult(null);
    if (!f) {
      setFile(null);
      return;
    }
    if (!ALLOWED_TYPES.includes(f.type)) {
      setFile(null);
      setUi((prev) => ({
        ...prev,
        feedback: { kind: "error", text: "jpg, png 파일만 선택할 수 있습니다." },
      }));
      return;
    }
    setFile(f);
  }, []);

  const onInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] ?? null;
    pickFile(f);
    e.target.value = "";
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setUi((prev) => ({ ...prev, dragOver: false }));
    pickFile(e.dataTransfer.files?.[0] ?? null);
  };

  const onDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setUi((prev) => ({ ...prev, dragOver: true }));
  };

  const onDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setUi((prev) => ({ ...prev, dragOver: false }));
  };

  const openFilePicker = () => inputRef.current?.click();

  const recognize = async () => {
    if (!file) return;
    setUi((prev) => ({ ...prev, uploading: true, feedback: null }));
    setResult(null);
    const body = new FormData();
    body.append("file", file);

    try {
      const res = await fetch(`${apiBaseUrl}/vision/recognize-face`, {
        method: "POST",
        body,
      });
      if (!res.ok) {
        const msg = await res.text().catch(() => "");
        throw new Error(msg || `HTTP ${res.status}`);
      }
      const data = (await res.json()) as FaceRecognitionResponse;
      setResult(data);
    } catch {
      setUi((prev) => ({
        ...prev,
        feedback: {
          kind: "error",
          text: "얼굴 인식에 실패했습니다. 백엔드 POST /vision/recognize-face 로 전송됩니다.",
        },
      }));
    } finally {
      setUi((prev) => ({ ...prev, uploading: false }));
    }
  };

  return (
    <div className="mt-16 w-full max-w-md flex flex-col items-center">
      <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-center mb-2">
        객체 탐지
      </h2>
      <p className="text-sm text-gray-500 text-center mb-8 max-w-md">
        사람 얼굴 사진을 업로드하면 학습된 YOLO 분류 모델이 누구인지 추론합니다.
      </p>

      <input
        ref={inputRef}
        type="file"
        accept=".jpg,.jpeg,.png,image/jpeg,image/png"
        className="sr-only"
        aria-hidden
        onChange={onInputChange}
      />

      <div
        role="button"
        tabIndex={0}
        aria-label="얼굴 이미지 파일을 끌어다 놓거나 클릭하여 선택"
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            openFilePicker();
          }
        }}
        onClick={openFilePicker}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        className={[
          "w-full max-w-md rounded-2xl border-2 border-dashed px-6 py-14 text-center cursor-pointer transition-colors outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2",
          ui.dragOver
            ? "border-blue-500 bg-blue-50/80"
            : "border-gray-300 bg-gray-50/80 hover:border-gray-400 hover:bg-gray-50",
        ].join(" ")}
      >
        {previewUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={previewUrl}
            alt="업로드 미리보기"
            className="mx-auto mb-4 max-h-40 rounded-lg object-contain"
          />
        ) : (
          <ScanFace
            className="mx-auto mb-4 text-gray-400"
            size={40}
            strokeWidth={1.5}
            aria-hidden
          />
        )}
        <p className="text-base font-medium text-gray-800 mb-1">얼굴 이미지 업로드</p>
        <p className="text-sm text-gray-500">
          jpg, png 이미지를 여기에 끌어다 놓거나, 이 영역을 클릭해 선택하세요.
        </p>
      </div>

      <div className="flex flex-wrap items-center justify-center gap-3 w-full max-w-md mt-6">
        <button
          type="button"
          onClick={openFilePicker}
          className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium rounded-xl border border-gray-300 bg-white text-gray-800 hover:bg-gray-50 transition-colors"
        >
          <FolderOpen size={18} aria-hidden />
          파일 선택
        </button>
        <button
          type="button"
          disabled={!file || ui.uploading}
          onClick={recognize}
          className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium rounded-xl border border-blue-600 bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {ui.uploading ? (
            <Loader2 size={18} className="animate-spin" aria-hidden />
          ) : (
            <Upload size={18} aria-hidden />
          )}
          이름 맞추기
        </button>
      </div>

      {ui.feedback && (
        <div
          role="status"
          className="mt-8 flex max-w-md items-start gap-2 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-900"
        >
          <AlertCircle className="shrink-0 text-red-600" size={18} aria-hidden />
          <span>{ui.feedback.text}</span>
        </div>
      )}

      {result && (
        <div
          role="status"
          className="mt-8 flex w-full max-w-md flex-col items-center gap-1 rounded-xl border border-green-200 bg-green-50 px-4 py-4 text-green-900"
        >
          <span className="text-xs font-medium uppercase tracking-widest text-green-700">
            인식 결과
          </span>
          <span className="text-xl font-bold">{result.name}</span>
          <span className="text-sm text-green-700">
            확신도 {(result.confidence * 100).toFixed(1)}%
          </span>
        </div>
      )}
    </div>
  );
}
