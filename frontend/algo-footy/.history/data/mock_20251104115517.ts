export interface Match {
  date: string;
  prediction: string;
  country: string;
  league: string;
  home: string;
  away: string;
  odds: number;
  hicon: string;
  aicon: string;
  probability: string;
}

export type MatchData = Record<string, Match>;
