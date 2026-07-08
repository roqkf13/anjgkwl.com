import { ScoutZones } from "@/components/scout-zones";

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col min-h-0 bg-[radial-gradient(ellipse_at_center_bottom,_#dbeafe_0%,_#f8fafc_45%,_#ffffff_100%)] dark:bg-[radial-gradient(ellipse_at_center_bottom,_#1e293b_0%,_#0f172a_55%,_#020617_100%)]">
      <ScoutZones />
    </main>
  );
}
