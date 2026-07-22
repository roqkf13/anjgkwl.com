import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

_here = Path(__file__).parent

# apps/ → "titanic.*" 임포트 활성화
_apps_dir = str(_here.parent.parent)
if _apps_dir not in sys.path:
    sys.path.insert(0, _apps_dir)

# fastapi/ → "core.*" 임포트 활성화
_fastapi_dir = str(_here.parent.parent.parent)
if _fastapi_dir not in sys.path:
    sys.path.insert(0, _fastapi_dir)
