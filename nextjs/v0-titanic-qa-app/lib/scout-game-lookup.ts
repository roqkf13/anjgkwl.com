import {
  getScoutGenre,
  SCOUT_GENRES,
  type ScoutGame,
  type ScoutGenre,
} from "@/lib/scout-genres";

export function scoutGameDetailPath(genreId: string, steamAppId: number): string {
  return `/scout/${genreId}/games/${steamAppId}`;
}

export function findScoutGame(
  steamAppId: number,
): { game: ScoutGame; genre: ScoutGenre } | undefined {
  for (const genre of SCOUT_GENRES) {
    const game = genre.games.find((g) => g.steamAppId === steamAppId);
    if (game) return { game, genre };
  }
  return undefined;
}

/** 장르 페이지 컨텍스트에서 게임 조회 (병합 장르 카드용 genreId 지원) */
export function getScoutGameInGenre(
  genreId: string,
  steamAppId: number,
): ScoutGame | undefined {
  return getScoutGenre(genreId)?.games.find((g) => g.steamAppId === steamAppId);
}
