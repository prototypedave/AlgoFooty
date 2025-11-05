export interface Match {
  datetime: string;
  prediction: string;
  country: string;
  league: string;
  home: string;
  away: string;
  odds: number;
}

export type MatchData = Record<string, Match>;
