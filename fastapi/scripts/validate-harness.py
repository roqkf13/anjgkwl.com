"""
하네스 검증 스크립트 (Harness Validator)

스타 토폴로지 구조가 깨지지 않았는지 MD 파일 기반으로 검사한다.

검사 항목:
  1. frontmatter 필수 필드 존재 여부 (type, id, links)
  2. 허브가 정확히 1개인지
  3. 스포크 → 스포크 직접 링크 금지
  4. 고립 노드 (아무것도 연결되지 않은 노드) 탐지
  5. 순환 참조 탐지

사용법:
  python scripts/validate-harness.py [MD_파일_디렉토리]
  기본 탐색 경로: 프로젝트 루트의 _docs/

MD frontmatter 예시:
  ---
  type: hub          # 또는 spoke
  id: ontology
  title: "허브 이름"
  links:
    - friday13th
    - scout
  ---
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML이 설치되어 있지 않습니다: pip install pyyaml")
    sys.exit(1)


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
REQUIRED_FIELDS = {"type", "id", "links"}


# ── 파싱 ──────────────────────────────────────────────────────────────────────

def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"  [WARN] YAML 파싱 실패 ({path.name}): {e}")
        return None


def load_nodes(root: Path) -> dict[str, dict]:
    """MD 파일을 탐색하여 {id: frontmatter} 딕셔너리로 반환."""
    nodes: dict[str, dict] = {}
    for md_file in root.rglob("*.md"):
        fm = parse_frontmatter(md_file)
        if fm is None:
            continue
        node_id = fm.get("id")
        if node_id:
            fm["_file"] = str(md_file.relative_to(root))
            nodes[node_id] = fm
    return nodes


# ── 검사 ──────────────────────────────────────────────────────────────────────

def check_required_fields(nodes: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for node_id, fm in nodes.items():
        missing = REQUIRED_FIELDS - set(fm.keys())
        if missing:
            errors.append(
                f"[필수 필드 누락] {fm.get('_file', node_id)}: {missing}"
            )
        if fm.get("type") not in ("hub", "spoke"):
            errors.append(
                f"[type 오류] {fm.get('_file', node_id)}: type은 'hub' 또는 'spoke'여야 함 (현재: {fm.get('type')!r})"
            )
    return errors


def check_single_hub(nodes: dict[str, dict]) -> list[str]:
    hubs = [nid for nid, fm in nodes.items() if fm.get("type") == "hub"]
    if len(hubs) == 0:
        return ["[허브 없음] type: hub 노드가 존재하지 않습니다."]
    if len(hubs) > 1:
        return [f"[허브 중복] 허브는 1개여야 합니다. 발견: {hubs}"]
    return []


def check_spoke_to_spoke(nodes: dict[str, dict]) -> list[str]:
    """스포크 노드의 links에 다른 스포크가 있으면 위반."""
    hub_ids = {nid for nid, fm in nodes.items() if fm.get("type") == "hub"}
    errors: list[str] = []
    for node_id, fm in nodes.items():
        if fm.get("type") != "spoke":
            continue
        links: list[str] = fm.get("links") or []
        for link in links:
            if link not in hub_ids and link in nodes:
                errors.append(
                    f"[스포크→스포크 금지] {fm.get('_file', node_id)} "
                    f"→ {link} (허브를 경유해야 함)"
                )
    return errors


def check_isolated_nodes(nodes: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for node_id, fm in nodes.items():
        links: list[str] = fm.get("links") or []
        if not links:
            errors.append(
                f"[고립 노드] {fm.get('_file', node_id)}: links가 비어 있음"
            )
    return errors


def check_unknown_links(nodes: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for node_id, fm in nodes.items():
        links: list[str] = fm.get("links") or []
        for link in links:
            if link not in nodes:
                errors.append(
                    f"[깨진 링크] {fm.get('_file', node_id)} → {link!r} (존재하지 않는 노드)"
                )
    return errors


def check_cycles(nodes: dict[str, dict]) -> list[str]:
    """DFS로 순환 참조를 탐지한다."""
    graph: dict[str, list[str]] = {
        nid: (fm.get("links") or []) for nid, fm in nodes.items()
    }
    visited: set[str] = set()
    path: set[str] = set()
    cycles: list[str] = []

    def dfs(node: str) -> None:
        visited.add(node)
        path.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in nodes:
                continue
            if neighbor in path:
                cycles.append(f"[순환 참조] {node} → {neighbor}")
            elif neighbor not in visited:
                dfs(neighbor)
        path.discard(node)

    for nid in nodes:
        if nid not in visited:
            dfs(nid)

    return cycles


# ── 진입점 ────────────────────────────────────────────────────────────────────

def main() -> None:
    search_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "_docs"

    if not search_root.exists():
        print(f"[ERROR] 경로가 존재하지 않습니다: {search_root}")
        sys.exit(1)

    print(f"하네스 검증 시작: {search_root}\n")
    nodes = load_nodes(search_root)

    if not nodes:
        print("frontmatter가 있는 MD 파일을 찾지 못했습니다.")
        sys.exit(0)

    print(f"노드 {len(nodes)}개 발견: {list(nodes.keys())}\n")

    all_errors: list[str] = []
    all_errors += check_required_fields(nodes)
    all_errors += check_single_hub(nodes)
    all_errors += check_spoke_to_spoke(nodes)
    all_errors += check_isolated_nodes(nodes)
    all_errors += check_unknown_links(nodes)
    all_errors += check_cycles(nodes)

    if all_errors:
        print("── 위반 항목 ──────────────────────────────────")
        for err in all_errors:
            print(f"  {err}")
        print(f"\n총 {len(all_errors)}개 위반. 하네스 검증 실패.")
        sys.exit(1)
    else:
        print("모든 하네스 검증 통과.")


if __name__ == "__main__":
    main()
