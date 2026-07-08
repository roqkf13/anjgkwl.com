import { notFound } from "next/navigation";

import { ScoutGameDetailView } from "@/components/scout-game-detail-view";
import { getScoutGameInGenre } from "@/lib/scout-game-lookup";
import { getScoutGenre, SCOUT_GENRES } from "@/lib/scout-genres";

type PageProps = {
  params: Promise<{ genre: string; steamAppId: string }>;
};

export function generateStaticParams() {
  return SCOUT_GENRES.flatMap((genre) =>
    genre.games.map((game) => ({
      genre: genre.id,
      steamAppId: String(game.steamAppId),
    })),
  );
}

export default async function ScoutGameDetailPage({ params }: PageProps) {
  const { genre: genreId, steamAppId: steamAppIdRaw } = await params;
  const steamAppId = Number(steamAppIdRaw);

  if (!Number.isFinite(steamAppId) || steamAppId < 1) {
    notFound();
  }

  const genre = getScoutGenre(genreId);
  const game = getScoutGameInGenre(genreId, steamAppId);

  if (!genre || !game) {
    notFound();
  }

  return (
    <ScoutGameDetailView
      genreId={genreId}
      steamAppId={steamAppId}
      initialTitle={game.title}
    />
  );
}
