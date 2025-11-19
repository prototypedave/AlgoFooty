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
  probability: number;
  hscore: number | string;
  ascore: number | string;
  win: boolean | string | number;
}

export type MatchData = Record<string, Match>;
