"""backend/ 에서 실행할 때 apps/main.py 로 위임한다.

  cd backend
  python apps/main.py

동일 앱을 apps/ 에서 직접 띄울 때:

  cd backend/apps
  python main.py

또는:

  python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 ^
    --app-dir backend/apps
"""

from __future__ import annotations

from pathlib import Path

if __name__ == "__main__":
    import runpy

    runpy.run_path(
        str(Path(__file__).resolve().parent / "apps" / "main.py"),
        run_name="__main__",
    )
