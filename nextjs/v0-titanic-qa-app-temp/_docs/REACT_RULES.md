# React 코딩 규칙 (Cursor / 에이전트용)

이 문서는 프론트엔드(`frontend/v0-titanic-qa-app` 등) 작업 시 **매번 같은 지시를 반복하지 않도록** Cursor에서 `@docs/DevOps/Frontend/REACT_RULES.md` 로 참조한다.

---

## 1. `useState`는 적게 쓴다

- **관련 없는 상태마다 `useState`를 나누지 않는다.** 훅이 많아질수록 리렌더·동기화·유지보수 비용이 커진다.
- **폼 입력값**은 가능하면 `useState`로 들고 있지 않고, `<form>` + `name` + 제출 시 `FormData`로 읽는다.
- **UI 전용 상태**(에러, 로딩, 성공 여부 등)만 모아 **하나의 객체**로 `useState` 한다.

### 권장

| 상황 | 방식 |
|------|------|
| 로그인/회원가입 폼 필드 | `FormData` + `Object.fromEntries` |
| `error`, `success`, `submitting` 등 UI 플래그 | `useState<UiState>({ ... })` 한 개 |
| 서버/전역 데이터 | React Query, SWR, Context 등 (필요 시) |

### 비권장

```tsx
const [name, setName] = useState("");
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [error, setError] = useState<string | null>(null);
const [submitting, setSubmitting] = useState(false);
// … 필드마다 useState 남발
```

---

## 2. 표준 패턴: UI 상태 객체 + FormData

### 타입과 초기값

```tsx
type FormUiState = {
  error: string | null;
  success: boolean;
  submitting: boolean;
};

const initialUiState: FormUiState = {
  error: null,
  success: false,
  submitting: false,
};

const [ui, setUi] = useState<FormUiState>(initialUiState);
```

### 제출 핸들러 (참조 구현)

```tsx
const handleSignup = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
  const formProps = Object.fromEntries(formData.entries()) as Record<
    string,
    string
  >;

  const name = (formProps.name ?? "").trim();
  const email = (formProps.email ?? "").trim();
  const password = formProps.password ?? "";
  const passwordConfirm = formProps.passwordConfirm ?? "";
  const role = formProps.role ?? "user";

  setUi({ error: null, success: false, submitting: false });

  // 검증 후 API 호출 …
  setUi((prev) => ({ ...prev, submitting: true }));
  try {
    // fetch …
    setUi((prev) => ({ ...prev, success: true }));
    e.currentTarget.reset();
  } catch {
    setUi((prev) => ({ ...prev, error: "…" }));
  } finally {
    setUi((prev) => ({ ...prev, submitting: false }));
  }
};
```

### JSX

- 각 `<Input>` / `<select>`에 **`name`** 과 동일한 키를 둔다 (`name`, `email`, `password` …).
- `disabled={ui.submitting}`, 메시지는 `{ui.error}`, `{ui.success}`.

### 프로젝트 내 예시 파일

- `frontend/v0-titanic-qa-app/app/signup/page.tsx`

---

## 3. Cursor에 붙여 넣을 프롬프트 (복사용)

아래 블록을 그대로 사용하거나, `@docs/DevOps/Frontend/REACT_RULES.md` 를 멘션한다.

```text
@docs/DevOps/Frontend/REACT_RULES.md

React에서 useState는 많이 사용하면 안 됩니다.
다음 코드를 참조하여, 여러 개의 useState를 하나의 useState 객체로 압축하고,
폼 필드는 FormData로 읽도록 변경해줘.

const handleSignup = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
  const formProps = Object.fromEntries(formData.entries());
  // formProps에서 name, email 등 추출 후 검증·API 호출
};

- UI 상태(error, success, submitting 등)만 { error, success, submitting } 형태의 단일 useState 객체로 관리
- 입력 필드마다 useState 쓰지 말 것
- 기존 동작(검증, API URL, 메시지)은 유지
```

### 짧은 버전

```text
@docs/DevOps/Frontend/REACT_RULES.md 적용해서 이 폼/refactor 해줘. useState 객체 압축 + FormData 패턴.
```

---

## 4. 에이전트 체크리스트

리팩터·신규 폼 작성 후 스스로 확인:

- [ ] `useState`가 3개 이상이면, UI 상태는 1개 객체로 합칠 수 있는지 검토했는가?
- [ ] 폼 값을 `value` + `onChange` + 개별 state로 두지 않았는가?
- [ ] `name` 속성과 `FormData` 키가 일치하는가?
- [ ] `setUi((prev) => ({ ...prev, ... }))` 로 부분 업데이트하는가?
- [ ] `window.alert` / `console.log` 에 비밀번호·이메일 등 폼 값을 넣지 않았는가?

---

## 5. 민감 정보 노출 금지

- **`window.alert` / `confirm` / `prompt`에 폼 입력값(이름, 이메일, 비밀번호 등)을 넣지 않는다.** 디버깅·데모용이라도 사용하지 않는다.
- 사용자에게 보여줄 메시지는 **일반 문구**만 (`ui.error`, `ui.success`, `role="status"` 등). 서버 `detail`을 그대로 노출할 때도 비밀번호·토큰이 포함되지 않는지 확인한다.
- `console.log(formProps)`, `JSON.stringify(formData)` 등으로 폼 전체를 출력하지 않는다.

### 비권장

```tsx
alert(`이름: ${name}\n비밀번호: ${password}`);
console.log("signup", formProps);
```

### 권장

```tsx
setUi((prev) => ({ ...prev, error: "모든 항목을 입력해 주세요." }));
setUi((prev) => ({ ...prev, success: true }));
```

---

## 6. `useState` / FormData 예외

다음은 **개별 `useState` 또는 다른 도구**가 맞을 수 있다.

- 단일 토글 하나만 있는 아주 작은 컴포넌트
- `useReducer`가 명확한 상태 전이가 많을 때
- 제어 컴포넌트가 꼭 필요한 실시간 미리보기·디바운스 검색
- 서버 상태는 React Query 등 전용 라이브러리 우선
