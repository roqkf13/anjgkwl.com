import Link from "next/link";

// TODO: 아래는 플레이스홀더입니다. 정식 서비스 전 반드시 법률 검토를 거친
// 실제 개인정보 처리방침 문구로 교체하세요.
export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-950 px-4 py-12">
      <div className="mx-auto max-w-2xl space-y-6">
        <Link
          href="/"
          className="text-sm font-medium text-violet-600 dark:text-violet-400 hover:underline"
        >
          Titanic QA
        </Link>
        <h1 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
          개인정보 처리방침
        </h1>
        <p className="text-sm text-amber-600 dark:text-amber-400">
          ※ 아래 내용은 예시(placeholder)입니다. 정식 서비스 전 반드시 법률 검토를 거친 문구로 교체해 주세요.
        </p>

        <div className="space-y-4 text-sm leading-relaxed text-gray-700 dark:text-gray-300">
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">1. 수집하는 개인정보 항목</h2>
            <p>
              이메일 회원가입: 이름, 이메일, 비밀번호(암호화 저장)
              <br />
              소셜 로그인(구글/네이버): 이름, 이메일, 소셜 계정 식별자
            </p>
          </section>
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">2. 개인정보의 수집 및 이용 목적</h2>
            <p>
              회원 식별 및 로그인, 서비스 제공, 문의 응대를 위해 개인정보를 수집·이용합니다.
            </p>
          </section>
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">3. 개인정보의 보유 및 이용 기간</h2>
            <p>
              회원 탈퇴 시까지 보유하며, 탈퇴 요청 시 관련 법령이 정한 기간을 제외하고 지체 없이 파기합니다.
            </p>
          </section>
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">4. 제3자 제공</h2>
            <p>
              법령에 근거하지 않는 한 이용자의 개인정보를 제3자에게 제공하지 않습니다.
            </p>
          </section>
        </div>
      </div>
    </main>
  );
}
