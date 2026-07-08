const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type TitanicRow = Record<string, unknown>;

export default async function TitanicNeonPage() {
  let rows: TitanicRow[] = [];
  let count: number | null = null;
  let error: string | null = null;

  try {
    const [dataRes, countRes] = await Promise.all([
      fetch(`${apiBaseUrl}/titanic/data`, { cache: "no-store" }),
      fetch(`${apiBaseUrl}/titanic/count`, { cache: "no-store" }),
      fetch(`${apiBaseUrl}/titanic/walter/myself`, { cache: "no-store" }),
    ]);

    if (!dataRes.ok) {
      error = `데이터 조회 실패 (HTTP ${dataRes.status})`;
    } else {
      const payload = (await dataRes.json()) as unknown;
      rows = Array.isArray(payload) ? (payload as TitanicRow[]) : [];
    }

    if (countRes.ok) {
      const countPayload = (await countRes.json()) as { count?: number };
      count = typeof countPayload.count === "number" ? countPayload.count : null;
    }
  } catch {
    error = "백엔드에 연결할 수 없습니다. API 서버 실행 여부를 확인하세요.";
  }

  return (
    <main className="flex-1 overflow-y-auto px-6 sm:px-10 py-10">
      <div className="mx-auto max-w-6xl">
        <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-gray-500 dark:text-gray-400">
          Lesson · 3. 구현 데이터 보기
        </p>
        <h1 className="mb-3 text-3xl sm:text-4xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
          Neon 업로드 데이터
        </h1>
        <p className="mb-6 text-sm text-gray-600 dark:text-gray-400">
          <code className="text-xs">GET /titanic/data</code>,{" "}
          <code className="text-xs">GET /titanic/count</code>,{" "}
          <code className="text-xs">GET /titanic/walter/myself</code> 응답을 표시합니다.
        </p>

        {error ? (
          <p
            role="alert"
            className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-100"
          >
            {error}
          </p>
        ) : (
          <>
            <div className="mb-4 rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-700 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-300">
              총 레코드:{" "}
              <span className="font-semibold text-gray-900 dark:text-gray-100">
                {count ?? rows.length}건
              </span>
            </div>

            <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-800">
              <table className="min-w-full bg-white text-sm dark:bg-gray-950">
                <thead className="bg-gray-50 dark:bg-gray-900">
                  <tr>
                    <th className="px-3 py-2 text-left font-medium">PassengerId</th>
                    <th className="px-3 py-2 text-left font-medium">Name</th>
                    <th className="px-3 py-2 text-left font-medium">gender</th>
                    <th className="px-3 py-2 text-left font-medium">Survived</th>
                    <th className="px-3 py-2 text-left font-medium">Pclass</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.length === 0 ? (
                    <tr>
                      <td className="px-3 py-3 text-gray-500 dark:text-gray-400" colSpan={5}>
                        저장된 데이터가 없습니다.
                      </td>
                    </tr>
                  ) : (
                    rows.map((row, index) => (
                      <tr key={`${String(row.PassengerId ?? index)}-${index}`} className="border-t border-gray-200 dark:border-gray-800">
                        <td className="px-3 py-2">{String(row.PassengerId ?? "-")}</td>
                        <td className="px-3 py-2">{String(row.Name ?? "-")}</td>
                        <td className="px-3 py-2">{String(row.gender ?? "-")}</td>
                        <td className="px-3 py-2">{String(row.Survived ?? "-")}</td>
                        <td className="px-3 py-2">{String(row.Pclass ?? "-")}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
