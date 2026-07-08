import json

import pandas as pd

_DORO_ROWS: list[dict[str, object]] = [
    {
        "기준연도": 2022,
        "노선명": "경부선",
        "구간": "서울TG-수원신갈IC",
        "사고건수": 32,
        "사망자수": 1,
        "부상자수": 41,
        "주요원인": "전방주시 태만",
    },
    {
        "기준연도": 2023,
        "노선명": "영동선",
        "구간": "여주JC-문막IC",
        "사고건수": 21,
        "사망자수": 0,
        "부상자수": 28,
        "주요원인": "안전거리 미확보",
    },
    {
        "기준연도": 2024,
        "노선명": "서해안선",
        "구간": "서서울TG-매송IC",
        "사고건수": 18,
        "사망자수": 1,
        "부상자수": 19,
        "주요원인": "졸음운전",
    },
]


class DoroReader:
    def __init__(self):
        pass

    def _frame(self) -> pd.DataFrame:
        return pd.DataFrame(_DORO_ROWS)

    def get_data(self):
        df = self._frame()
        row = df.iloc[[1]] if len(df) > 1 else df.head(1)
        return row.astype(object).where(row.notna(), None)

    def head_records(self, n: int = 10) -> list[dict]:
        return json.loads(self._frame().head(n).to_json(orient="records"))