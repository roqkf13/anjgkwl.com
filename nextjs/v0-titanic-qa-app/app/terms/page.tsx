import Link from "next/link";

// TODO: 아래는 플레이스홀더입니다. 정식 서비스 전 반드시 법률 검토를 거친
// 실제 이용약관 문구로 교체하세요.
export default function TermsPage() {
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
          이용약관
        </h1>
        <p className="text-sm text-amber-600 dark:text-amber-400">
          ※ 아래 내용은 예시(placeholder)입니다. 정식 서비스 전 반드시 법률 검토를 거친 문구로 교체해 주세요.
        </p>

        <div className="space-y-4 text-sm leading-relaxed text-gray-700 dark:text-gray-300">
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">제1조 (목적)</h2>
            <p>
              이 약관은 Titanic QA(이하 &quot;서비스&quot;)가 제공하는 서비스의 이용과 관련하여
              서비스와 이용자 간의 권리, 의무 및 책임사항을 규정함을 목적으로 합니다.
            </p>
          </section>
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">제2조 (회원가입)</h2>
            <p>
              이용자는 이메일 또는 소셜 로그인(구글, 네이버)을 통해 서비스에 가입할 수 있으며,
              가입 시 본 약관 및 개인정보 처리방침에 동의한 것으로 봅니다.
            </p>
          </section>
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">제3조 (서비스의 제공 및 변경)</h2>
            <p>
              서비스는 운영상, 기술상의 필요에 따라 제공하는 서비스의 내용을 변경할 수 있습니다.
            </p>
          </section>
          <section>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">제4조 (책임의 한계)</h2>
            <p>
              서비스는 천재지변, 불가항력적 사유로 인한 서비스 중단에 대해 책임을 지지 않습니다.
            </p>
          </section>
        </div>
      </div>
    </main>
  );
}
