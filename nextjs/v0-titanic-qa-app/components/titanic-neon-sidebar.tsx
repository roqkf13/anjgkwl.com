type TitanicNeonSidebarProps = {
  rows: Array<Record<string, unknown>>;
  count: number | null;
  error: string | null;
};

export function TitanicNeonSidebar({ rows, count, error }: TitanicNeonSidebarProps) {
  const preview = rows.slice(0, 5);

  return (
    <aside className="hidden xl:block w-80 shrink-0">
      <div className="sticky top-6 rounded-2xl border border-gray-200 bg-gray-50/80 p-5 dark:border-gray-800 dark:bg-gray-900/80">
        <h2 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
          구현 확인: Neon 업로드 데이터
        </h2>

        {error ? (
          <p className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-900 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-100">
            {error}
          </p>
        ) : (
          <>
            <div className="mb-4 rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs dark:border-gray-800 dark:bg-gray-950">
              <p className="text-gray-500 dark:text-gray-400">총 레코드</p>
              <p className="text-base font-semibold text-gray-900 dark:text-gray-100">
                {count ?? rows.length}건
              </p>
            </div>

            <p className="mb-2 text-xs font-medium text-gray-700 dark:text-gray-300">
              최근 미리보기 (최대 5건)
            </p>
            <ul className="space-y-2">
              {preview.length === 0 ? (
                <li className="text-xs text-gray-500 dark:text-gray-400">
                  저장된 데이터가 없습니다.
                </li>
              ) : (
                preview.map((item, index) => (
                  <li
                    key={`${String(item.PassengerId ?? index)}-${index}`}
                    className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs dark:border-gray-800 dark:bg-gray-950"
                  >
                    <p className="font-medium text-gray-900 dark:text-gray-100">
                      {String(item.Name ?? "(이름 없음)")}
                    </p>
                    <p className="text-gray-500 dark:text-gray-400">
                      ID {String(item.PassengerId ?? "-")} / gender{" "}
                      {String(item.gender ?? "-")} / Survived{" "}
                      {String(item.Survived ?? "-")}
                    </p>
                  </li>
                ))
              )}
            </ul>
          </>
        )}
      </div>
    </aside>
  );
}
