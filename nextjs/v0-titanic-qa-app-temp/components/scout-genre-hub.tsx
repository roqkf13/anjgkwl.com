import { ScoutGenreHubBody } from "@/components/scout-genre-hub-body";
import { ScoutGenreHubHeader } from "@/components/scout-genre-hub-header";

type ScoutGenreHubProps = {
  genreId: string;
};

export function ScoutGenreHub({ genreId }: ScoutGenreHubProps) {
  return (
    <main className="flex flex-1 flex-col min-h-0 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <ScoutGenreHubHeader genreId={genreId} />
      <div className="flex-1 overflow-y-auto">
        <ScoutGenreHubBody genreId={genreId} />
      </div>
    </main>
  );
}
