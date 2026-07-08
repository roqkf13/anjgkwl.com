import { Bot, Search, Ship, Users } from "lucide-react";

const facts = [
  {
    icon: Ship,
    title: "Titanic",
    lines: ["Sunk in 1912", "Over 1,500 deaths"],
  },
  {
    icon: Users,
    title: "2,224 passengers",
    lines: [] as string[],
  },
  {
    icon: Search,
    title: "Data Analysis",
    lines: [] as string[],
  },
  {
    icon: Bot,
    title: "Machine Learning Model",
    lines: [] as string[],
  },
] as const;

export function TitanicLessonAside() {
  return (
    <aside className="hidden xl:block w-72 shrink-0">
      <div className="sticky top-6 rounded-2xl border border-gray-200 bg-gray-50/80 p-5 dark:border-gray-800 dark:bg-gray-900/80">
        <ul className="space-y-5">
          {facts.map((fact) => (
            <li key={fact.title} className="flex gap-3">
              <fact.icon
                className="mt-0.5 shrink-0 text-gray-500 dark:text-gray-400"
                size={22}
                strokeWidth={1.5}
                aria-hidden
              />
              <div>
                <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                  {fact.title}
                </p>
                {fact.lines.map((line) => (
                  <p
                    key={line}
                    className="text-xs text-gray-500 dark:text-gray-400"
                  >
                    {line}
                  </p>
                ))}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}
