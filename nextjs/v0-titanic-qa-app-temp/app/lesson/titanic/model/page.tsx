import { TitanicNeonSidebar } from "@/components/titanic-neon-sidebar";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const learningGoals = [
  "데이터 수집 및 전처리 기술 습득",
  "탐색적 데이터 분석(EDA) 실습",
  "분류 모델 개발 및 성능 평가",
  "실제 데이터 기반 인사이트 도출",
] as const;

const keyTopics = [
  "타이타닉 탑승객 데이터셋 분석",
  "성별, 연령, 좌석 등급에 따른 생존율 분석",
  "로지스틱 회귀 모델을 이용한 생존 예측",
  "모델 성능 평가 및 해석",
] as const;

function formatModelText(data: unknown): string {
  if (data == null) return "";
  if (typeof data === "string") return data;
  if (typeof data === "object") {
    return JSON.stringify(data, null, 2);
  }
  return String(data);
}

export default async function TitanicModelPage() {
  let modelText = "";
  let loadError: string | null = null;
  let neonRows: Array<Record<string, unknown>> = [];
  let neonCount: number | null = null;
  let neonError: string | null = null;

  try {
    const res = await fetch(`${apiBaseUrl}/titanic/model`, { cache: "no-store" });
    if (!res.ok) {
      loadError = `서버 응답 오류 (HTTP ${res.status})`;
    } else {
      const data: unknown = await res.json();
      modelText = formatModelText(data);
    }
  } catch {
    loadError =
      "백엔드에 연결할 수 없습니다. API 서버가 실행 중인지 확인하세요.";
  }

  try {
    const [dataRes, countRes] = await Promise.all([
      fetch(`${apiBaseUrl}/titanic/data`, { cache: "no-store" }),
      fetch(`${apiBaseUrl}/titanic/count`, { cache: "no-store" }),
    ]);

    if (!dataRes.ok) {
      neonError = `데이터 조회 실패 (HTTP ${dataRes.status})`;
    } else {
      const data = (await dataRes.json()) as Array<Record<string, unknown>>;
      neonRows = Array.isArray(data) ? data : [];
    }

    if (countRes.ok) {
      const countPayload = (await countRes.json()) as { count?: number };
      neonCount = typeof countPayload.count === "number" ? countPayload.count : null;
    }
  } catch {
    neonError = "Neon 데이터 조회에 실패했습니다.";
  }

  return (
    <main className="flex-1 overflow-y-auto px-6 sm:px-10 py-10">
      <div className="mx-auto flex max-w-6xl gap-10">
        <article className="min-w-0 flex-1 max-w-3xl">
          <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 dark:text-gray-400 mb-3">
            Lesson
          </p>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-gray-900 dark:text-gray-100 mb-4">
            타이타닉 모델 분석
          </h1>
          <p className="text-sm sm:text-base leading-relaxed text-gray-600 dark:text-gray-400 mb-10">
            1912년 4월 14일 밤, RMS 타이타닉호는 빙산과 충돌한 뒤 2시간 40분 만에
            침몰했습니다. 이 사건은 해상 안전 규정과 구조 설계에 큰 변화를
            가져왔습니다. 본 수업에서는 탑승객 데이터를 바탕으로 머신러닝으로
            생존 가능성을 예측하는 방법을 학습합니다.
          </p>

          <section className="mb-10">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
              학습 목표
            </h2>
            <ul className="list-disc space-y-2 pl-5 text-sm sm:text-base text-gray-700 dark:text-gray-300">
              {learningGoals.map((goal) => (
                <li key={goal}>{goal}</li>
              ))}
            </ul>
          </section>

          <section className="mb-10">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
              주요 내용
            </h2>
            <ul className="list-disc space-y-2 pl-5 text-sm sm:text-base text-gray-700 dark:text-gray-300">
              {keyTopics.map((topic) => (
                <li key={topic}>{topic}</li>
              ))}
            </ul>
          </section>

          <section className="mb-10">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
              실습: 백엔드 모델 API
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              <code className="text-xs">GET /titanic/model</code> 응답으로 학습된
              분류 모델 이름·정확도·특성 목록을 확인합니다.
            </p>
            {loadError ? (
              <p
                role="alert"
                className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-100"
              >
                {loadError}
              </p>
            ) : (
              <pre className="whitespace-pre-wrap break-words rounded-xl border border-gray-200 bg-gray-50 px-5 py-4 text-sm font-mono leading-relaxed dark:border-gray-800 dark:bg-gray-900">
                {modelText || "(모델 정보가 비어 있습니다)"}
              </pre>
            )}
          </section>

          <div className="rounded-xl border border-gray-200 bg-gray-50 px-5 py-4 text-sm text-gray-600 dark:border-gray-800 dark:bg-gray-900/60 dark:text-gray-400">
            <span className="font-medium text-gray-800 dark:text-gray-200">
              퀴즈:
            </span>{" "}
            각 단원 학습 후 확인 문제를 풀어 이해도를 점검하세요.
          </div>
        </article>

        <TitanicNeonSidebar rows={neonRows} count={neonCount} error={neonError} />
      </div>
    </main>
  );
}
