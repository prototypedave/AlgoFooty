export interface Match {
  date: string;
  prediction: string;
  country: string;
  league: string;
  home: string;
  away: string;
  odds: number;
  HomeIcon: string;
  AwayIcon: string;
}

export type MatchData = Record<string, Match>;
