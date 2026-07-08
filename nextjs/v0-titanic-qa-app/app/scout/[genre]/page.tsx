import { notFound } from "next/navigation";

import { ScoutGenreHub } from "@/components/scout-genre-hub";
import { getScoutGenre, SCOUT_GENRES } from "@/lib/scout-genres";

type PageProps = {
  params: Promise<{ genre: string }>;
};

export function generateStaticParams() {
  return SCOUT_GENRES.map((genre) => ({ genre: genre.id }));
}

export default async function ScoutGenrePage({ params }: PageProps) {
  const { genre: genreId } = await params;
  const genre = getScoutGenre(genreId);

  if (!genre) {
    notFound();
  }

  return <ScoutGenreHub genreId={genreId} />;
}
