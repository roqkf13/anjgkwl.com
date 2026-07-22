"""import-linter wrapper — fastapi/ 디렉토리에서 lint-imports를 실행한다."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).parent.parent
result = subprocess.run(["lint-imports"], cwd=root, check=False)
sys.exit(result.returncode)
