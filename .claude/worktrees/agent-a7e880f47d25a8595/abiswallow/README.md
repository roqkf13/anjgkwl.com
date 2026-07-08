# com.ragwatson

이 저장소는 **하네스 엔지니어링** 관점으로 정리되어 있다. LLM·에이전트가 기여하기 좋은 일은 **말로 명확히 적을 수 있는 것**과 **검증 가능한 것**에 가깝게 만드는 쪽으로 설계한다. 안드레아 카파시의 구분을 빌리면 다음과 같다.

> Software 1.0 easily automates what you can specify.  
> Software 2.0 easily automates what you can verify.
>
> — Andrej Karpathy, [Verifiability](https://karpathy.bearblog.dev/verifiability/)

즉, 요구사항은 **명세**로 고정하고, 완료는 **테스트·린트·재현 절차·CI** 같은 자동 신호로 닫는다. 추상화나 “느낌상 OK”만으로 루프를 끝내지 않는다.

---

## 문서 (에이전트·인간 공통)

| 파일 | 내용 |
|------|------|
| [`.cursorrules`](.cursorrules) | Cursor에 올라가는 **짧은** 필수 규칙 |
| [`CLAUDE.md`](CLAUDE.md) | 구현 전 사고·단순성·정밀 수정·**검증 가능한** 목표 등 전체 지침 |
| [`CURSOR.md`](CURSOR.md) | Cursor 사용 시 하네스·카파시 **프레임**과 체크리스트 |

상세 출처와 인용은 `CLAUDE.md` 하단의 1차 링크를 본다.

---

## 저장소 루트 개요

- **`docs/`** — 노트·문서 (Obsidian 설정 포함)
- **`scout/`** — 하위 프로젝트·실험 코드 등 (예: `scout/hub.anjgkwl`)

각 하위 디렉터리의 실행 방법·의존성은 해당 경로의 `README` 또는 스크립트를 따른다.

---

## 작업 원칙 요약

1. **명시:** 가정을 적고, 모호하면 질문한다.  
2. **검증:** 재현 → 자동 확인(테스트 등) → 통과로 마무리한다.  
3. **단순:** 요청 범위 밖 기능·과한 추상화를 넣지 않는다.  
4. **작은 diff:** 무관한 포맷/리팩터를 섞지 않는다.

자세한 문장은 위 표의 세 파일을 기준으로 한다.
