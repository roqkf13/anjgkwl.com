"use client";

import { useState } from "react";
import Link from "next/link";
import {
  LayoutDashboard, Gamepad2, Tag, Users, Plus, Pencil, Trash2, Eye,
  ChevronRight, ArrowLeft,
} from "lucide-react";

// ─── 데이터 ────────────────────────────────────────────────────────────────────

const GENRES = [
  { name: "소울라이크", eg: "Elden Ring",            color: "#e74c3c", bg: "#ffeaea", text: "#c0392b", count: 94,  desc: "높은 난이도와 보스 전투 중심의 액션 RPG" },
  { name: "로그라이크", eg: "Slay the Spire 2",      color: "#8e44ad", bg: "#f0eeff", text: "#6c5ce7", count: 112, desc: "매 run이 다른 랜덤 던전과 성장" },
  { name: "오픈월드",   eg: "Red Dead Redemption 2", color: "#27ae60", bg: "#edfff5", text: "#1e8449", count: 86,  desc: "넓은 맵을 자유롭게 탐험하는 세계" },
  { name: "메트로배니아", eg: "Hollow Knight",        color: "#e67e22", bg: "#fff5e6", text: "#ca6f1e", count: 92,  desc: "능력 해금으로 맵을 확장하는 탐험" },
];

const GAMES = [
  { name: "Elden Ring",            genre: "소울라이크",   bg: "#ffeaea", text: "#c0392b", dev: "FromSoftware",    year: 2022, score: 9.5 },
  { name: "Slay the Spire 2",      genre: "로그라이크",   bg: "#f0eeff", text: "#6c5ce7", dev: "Mega Crit",       year: 2025, score: 9.2 },
  { name: "Red Dead Redemption 2", genre: "오픈월드",     bg: "#edfff5", text: "#1e8449", dev: "Rockstar Games",  year: 2018, score: 9.7 },
  { name: "Hollow Knight",         genre: "메트로배니아", bg: "#fff5e6", text: "#ca6f1e", dev: "Team Cherry",     year: 2017, score: 9.4 },
  { name: "Dark Souls III",        genre: "소울라이크",   bg: "#ffeaea", text: "#c0392b", dev: "FromSoftware",    year: 2016, score: 9.1 },
  { name: "Hades",                 genre: "로그라이크",   bg: "#f0eeff", text: "#6c5ce7", dev: "Supergiant Games",year: 2020, score: 9.3 },
];

const USERS = [
  { name: "김민준", email: "minjun@mail.com",  genre: "소울라이크",   bg: "#ffeaea", text: "#c0392b", date: "2025.06.18", active: true  },
  { name: "이서연", email: "seoyeon@mail.com", genre: "메트로배니아", bg: "#fff5e6", text: "#ca6f1e", date: "2025.06.17", active: true  },
  { name: "박지호", email: "jiho@mail.com",    genre: "로그라이크",   bg: "#f0eeff", text: "#6c5ce7", date: "2025.06.15", active: true  },
  { name: "최유나", email: "yuna@mail.com",    genre: "오픈월드",     bg: "#edfff5", text: "#1e8449", date: "2025.06.12", active: false },
];

const STATS = [
  { label: "전체 회원",    value: "12,847", sub: "↑ 8.2% 이번 달" },
  { label: "등록된 게임",  value: "384",    sub: "↑ 12 신규 추가" },
  { label: "오늘 검색수",  value: "9,201",  sub: "↑ 3.4% 어제 대비" },
  { label: "장르 카테고리", value: "4",     sub: "활성 장르" },
];

// ─── 타입 / 내비게이션 ──────────────────────────────────────────────────────────

type Tab = "dash" | "genres" | "games" | "users";

const NAV: { key: Tab; label: string; Icon: React.ElementType }[] = [
  { key: "dash",   label: "대시보드",  Icon: LayoutDashboard },
  { key: "genres", label: "장르 관리", Icon: Tag },
  { key: "games",  label: "게임 관리", Icon: Gamepad2 },
  { key: "users",  label: "회원 관리", Icon: Users },
];

// ─── 공통 컴포넌트 ─────────────────────────────────────────────────────────────

function Card({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-4 md:p-5">
      <div className="flex items-center justify-between mb-3 md:mb-4 flex-wrap gap-2">
        <h2 className="text-sm font-semibold text-gray-800 dark:text-gray-100">{title}</h2>
        {action}
      </div>
      {children}
    </div>
  );
}

function GenrePill({ bg, text, children }: { bg: string; text: string; children: React.ReactNode }) {
  return (
    <span className="inline-block text-xs px-2 py-0.5 rounded-md font-medium whitespace-nowrap" style={{ backgroundColor: bg, color: text }}>
      {children}
    </span>
  );
}

function StatusBadge({ active, onLabel = "활성", offLabel = "휴면" }: { active: boolean; onLabel?: string; offLabel?: string }) {
  return (
    <span className={`text-xs px-2 py-0.5 rounded-md whitespace-nowrap ${active ? "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400" : "bg-gray-100 dark:bg-gray-700 text-gray-400"}`}>
      {active ? onLabel : offLabel}
    </span>
  );
}

function IconBtn({ icon: Icon, label }: { icon: React.ElementType; label: string }) {
  return (
    <button
      aria-label={label}
      className="w-8 h-8 md:w-7 md:h-7 flex items-center justify-center rounded-md border border-gray-200 dark:border-gray-600 text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 active:scale-95 transition-all"
    >
      <Icon size={14} />
    </button>
  );
}

function AddButton({ label }: { label: string }) {
  return (
    <button className="inline-flex items-center gap-1.5 px-3 py-2 md:py-1.5 text-xs font-medium rounded-lg bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-700 dark:hover:bg-white active:scale-[0.97] transition-all">
      <Plus size={13} /> {label}
    </button>
  );
}

function Th({ children }: { children: React.ReactNode }) {
  return <th className="text-left text-xs font-medium text-gray-400 dark:text-gray-500 px-3 py-2 border-b border-gray-100 dark:border-gray-700">{children}</th>;
}
function Td({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <td className={`px-3 py-2.5 text-sm text-gray-700 dark:text-gray-300 ${className}`}>{children}</td>;
}

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between py-1 text-sm">
      <span className="text-gray-400 dark:text-gray-500 text-xs">{label}</span>
      <span className="text-gray-700 dark:text-gray-300 text-right">{value}</span>
    </div>
  );
}

function MobileCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-gray-50 dark:bg-gray-900/50 border border-gray-100 dark:border-gray-700 rounded-lg p-3 mb-2 last:mb-0">
      {children}
    </div>
  );
}

// ─── 패널: 대시보드 ────────────────────────────────────────────────────────────

function DashPanel({ setTab }: { setTab: (t: Tab) => void }) {
  return (
    <>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 md:gap-3 mb-4 md:mb-5">
        {STATS.map(s => (
          <div key={s.label} className="bg-gray-50 dark:bg-gray-900 rounded-lg px-3 py-2.5 md:px-4 md:py-3">
            <p className="text-[11px] md:text-xs text-gray-400 dark:text-gray-500 mb-1">{s.label}</p>
            <p className="text-xl md:text-2xl font-semibold text-gray-900 dark:text-gray-100">{s.value}</p>
            <p className="text-[11px] md:text-xs text-emerald-500 mt-1">{s.sub}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card
          title="장르별 현황"
          action={
            <button onClick={() => setTab("genres")} className="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 flex items-center gap-0.5 transition-colors">
              전체 보기 <ChevronRight size={12} />
            </button>
          }
        >
          <div className="divide-y divide-gray-100 dark:divide-gray-700">
            {GENRES.map(g => (
              <div key={g.name} className="flex items-center gap-2 py-2.5">
                <span className="w-2 h-2 rounded-full shrink-0" style={{ background: g.color }} />
                <span className="text-sm font-medium text-gray-800 dark:text-gray-100 flex-1 min-w-0 truncate">{g.name}</span>
                <span className="hidden sm:inline text-xs text-gray-400 truncate max-w-[120px]">{g.eg}</span>
                <span className="text-xs text-gray-500 dark:text-gray-400 w-9 text-right shrink-0">{g.count}개</span>
                <StatusBadge active />
              </div>
            ))}
          </div>
        </Card>

        <Card
          title="최근 가입 회원"
          action={
            <button onClick={() => setTab("users")} className="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 flex items-center gap-0.5 transition-colors">
              전체 보기 <ChevronRight size={12} />
            </button>
          }
        >
          <div className="divide-y divide-gray-100 dark:divide-gray-700">
            {USERS.map(u => (
              <div key={u.email} className="flex items-center gap-2 py-2.5">
                <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold shrink-0" style={{ background: u.bg, color: u.text }}>{u.name[0]}</div>
                <span className="text-sm text-gray-800 dark:text-gray-100 flex-1 min-w-0 truncate">{u.name}</span>
                <GenrePill bg={u.bg} text={u.text}>{u.genre}</GenrePill>
                <span className="hidden sm:inline shrink-0">
                  <StatusBadge active={u.active} onLabel="신규" offLabel="일반" />
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </>
  );
}

// ─── 패널: 장르 관리 ───────────────────────────────────────────────────────────

function GenresPanel() {
  return (
    <Card title="장르 목록" action={<AddButton label="장르 추가" />}>
      <div className="md:hidden">
        {GENRES.map(g => (
          <MobileCard key={g.name}>
            <div className="flex items-center justify-between mb-1.5">
              <span className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ background: g.color }} />
                <span className="font-medium text-sm text-gray-800 dark:text-gray-100">{g.name}</span>
              </span>
              <StatusBadge active />
            </div>
            <p className="text-xs text-gray-400 mb-2">{g.desc}</p>
            <Row label="대표 게임" value={g.eg} />
            <Row label="게임 수" value={`${g.count}개`} />
            <div className="flex gap-1.5 justify-end mt-2">
              <IconBtn icon={Pencil} label="수정" />
              <IconBtn icon={Trash2} label="삭제" />
            </div>
          </MobileCard>
        ))}
      </div>

      <table className="hidden md:table w-full text-sm">
        <thead>
          <tr><Th>장르</Th><Th>대표 게임</Th><Th>설명</Th><Th>게임 수</Th><Th>상태</Th><Th>작업</Th></tr>
        </thead>
        <tbody className="divide-y divide-gray-50 dark:divide-gray-700/50">
          {GENRES.map(g => (
            <tr key={g.name} className="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
              <Td>
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full" style={{ background: g.color }} />
                  <span className="font-medium text-gray-800 dark:text-gray-100">{g.name}</span>
                </span>
              </Td>
              <Td className="text-gray-500 dark:text-gray-400">{g.eg}</Td>
              <Td className="text-gray-500 dark:text-gray-400">{g.desc}</Td>
              <Td>{g.count}</Td>
              <Td><StatusBadge active /></Td>
              <Td>
                <div className="flex gap-1">
                  <IconBtn icon={Pencil} label="수정" />
                  <IconBtn icon={Trash2} label="삭제" />
                </div>
              </Td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}

// ─── 패널: 게임 관리 ───────────────────────────────────────────────────────────

function GamesPanel() {
  return (
    <Card title="게임 목록" action={<AddButton label="게임 등록" />}>
      <div className="md:hidden">
        {GAMES.map(g => (
          <MobileCard key={g.name}>
            <div className="flex items-center justify-between mb-1.5">
              <span className="font-medium text-sm text-gray-800 dark:text-gray-100">{g.name}</span>
              <span className="text-xs text-gray-500">★ {g.score}</span>
            </div>
            <div className="flex items-center gap-2 mb-2">
              <GenrePill bg={g.bg} text={g.text}>{g.genre}</GenrePill>
            </div>
            <Row label="개발사" value={g.dev} />
            <Row label="출시 연도" value={g.year} />
            <div className="flex gap-1.5 justify-end mt-2">
              <IconBtn icon={Pencil} label="수정" />
              <IconBtn icon={Trash2} label="삭제" />
            </div>
          </MobileCard>
        ))}
      </div>

      <table className="hidden md:table w-full text-sm">
        <thead>
          <tr><Th>게임명</Th><Th>장르</Th><Th>개발사</Th><Th>출시</Th><Th>평점</Th><Th>작업</Th></tr>
        </thead>
        <tbody className="divide-y divide-gray-50 dark:divide-gray-700/50">
          {GAMES.map(g => (
            <tr key={g.name} className="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
              <Td><span className="font-medium text-gray-800 dark:text-gray-100">{g.name}</span></Td>
              <Td><GenrePill bg={g.bg} text={g.text}>{g.genre}</GenrePill></Td>
              <Td className="text-gray-500 dark:text-gray-400">{g.dev}</Td>
              <Td className="text-gray-500 dark:text-gray-400">{g.year}</Td>
              <Td>★ {g.score}</Td>
              <Td>
                <div className="flex gap-1">
                  <IconBtn icon={Pencil} label="수정" />
                  <IconBtn icon={Trash2} label="삭제" />
                </div>
              </Td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}

// ─── 패널: 회원 관리 ───────────────────────────────────────────────────────────

function UsersPanel() {
  return (
    <Card title="회원 목록">
      <div className="md:hidden">
        {USERS.map(u => (
          <MobileCard key={u.email}>
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-2 min-w-0">
                <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold shrink-0" style={{ background: u.bg, color: u.text }}>{u.name[0]}</div>
                <span className="font-medium text-sm text-gray-800 dark:text-gray-100 truncate">{u.name}</span>
              </div>
              <StatusBadge active={u.active} />
            </div>
            <p className="text-xs text-gray-400 mb-2 truncate">{u.email}</p>
            <Row label="선호 장르" value={<GenrePill bg={u.bg} text={u.text}>{u.genre}</GenrePill>} />
            <Row label="가입일" value={u.date} />
            <div className="flex gap-1.5 justify-end mt-2">
              <IconBtn icon={Eye} label="상세" />
              <IconBtn icon={Trash2} label="삭제" />
            </div>
          </MobileCard>
        ))}
      </div>

      <table className="hidden md:table w-full text-sm">
        <thead>
          <tr><Th>회원</Th><Th>이메일</Th><Th>선호 장르</Th><Th>가입일</Th><Th>상태</Th><Th>작업</Th></tr>
        </thead>
        <tbody className="divide-y divide-gray-50 dark:divide-gray-700/50">
          {USERS.map(u => (
            <tr key={u.email} className="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
              <Td>
                <div className="flex items-center gap-2">
                  <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold shrink-0" style={{ background: u.bg, color: u.text }}>{u.name[0]}</div>
                  <span className="font-medium text-gray-800 dark:text-gray-100">{u.name}</span>
                </div>
              </Td>
              <Td className="text-gray-400 dark:text-gray-500">{u.email}</Td>
              <Td><GenrePill bg={u.bg} text={u.text}>{u.genre}</GenrePill></Td>
              <Td className="text-gray-400 dark:text-gray-500">{u.date}</Td>
              <Td><StatusBadge active={u.active} /></Td>
              <Td>
                <div className="flex gap-1">
                  <IconBtn icon={Eye} label="상세" />
                  <IconBtn icon={Trash2} label="삭제" />
                </div>
              </Td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}

// ─── 메인 페이지 ───────────────────────────────────────────────────────────────

export default function AdminPage() {
  const [tab, setTab] = useState<Tab>("dash");
  const current = NAV.find(n => n.key === tab)!;

  return (
    <div className="flex flex-col md:flex-row min-h-[calc(100vh-56px)] bg-gray-50 dark:bg-gray-950">

      {/* 데스크탑 전용 사이드바 */}
      <aside className="hidden md:flex md:w-48 shrink-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex-col">
        <nav className="flex-1 p-2 pt-4">
          <p className="text-[10px] text-gray-400 dark:text-gray-500 px-2 mb-1 uppercase tracking-widest">메뉴</p>
          {NAV.map(({ key, label, Icon }) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`w-full flex items-center gap-2 px-2.5 py-2 rounded-lg text-sm mb-0.5 transition-colors ${
                tab === key
                  ? "bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 font-medium"
                  : "text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 hover:text-gray-700 dark:hover:text-gray-200"
              }`}
            >
              <Icon size={15} />
              {label}
            </button>
          ))}
        </nav>
        <div className="p-3 border-t border-gray-100 dark:border-gray-700">
          <Link href="/" className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
            <ArrowLeft size={13} /> 사이트로 돌아가기
          </Link>
        </div>
      </aside>

      {/* 컨텐츠 영역 */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* 상단 바 */}
        <div className="h-12 px-3 md:px-6 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between shrink-0 gap-2">
          <div className="flex items-center gap-2 min-w-0">
            <Link href="/" className="md:hidden w-7 h-7 flex items-center justify-center text-gray-400 shrink-0" aria-label="사이트로 돌아가기">
              <ArrowLeft size={16} />
            </Link>
            <current.Icon size={16} className="text-gray-400 shrink-0" />
            <span className="text-sm font-semibold text-gray-800 dark:text-gray-100 truncate">{current.label}</span>
          </div>
          <AddButton label="게임 추가" />
        </div>

        {/* 패널 */}
        <main className="flex-1 p-3 md:p-6 pb-20 md:pb-6 overflow-y-auto">
          {tab === "dash"   && <DashPanel setTab={setTab} />}
          {tab === "genres" && <GenresPanel />}
          {tab === "games"  && <GamesPanel />}
          {tab === "users"  && <UsersPanel />}
        </main>
      </div>

      {/* 모바일 전용 하단 탭바 */}
      <nav
        className="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex items-stretch z-40"
        style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
      >
        {NAV.map(({ key, label, Icon }) => (
          <button
            key={key}
            onClick={() => setTab(key)}
            className={`flex-1 flex flex-col items-center justify-center gap-0.5 py-2 text-[11px] transition-colors ${
              tab === key ? "text-gray-900 dark:text-gray-100 font-medium" : "text-gray-400 dark:text-gray-500"
            }`}
          >
            <Icon size={18} />
            {label}
          </button>
        ))}
      </nav>
    </div>
  );
}
