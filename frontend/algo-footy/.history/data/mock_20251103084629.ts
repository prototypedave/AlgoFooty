// mockData.ts
export const data: {
  [id: string]: {
    datetime: string;
    market: string;
    country: string;
    league: string;
    home: string;
    away: string;
    odds: number;
  };
} = (() => {
  // Define reusable types
type Market = "Home Win" | "Away Win" | "Over 2.5";
type Country = "England" | "Spain" | "Germany" | "Italy" | "France";

type LeagueMap = Record<Country, string[]>;
type TeamMap = Record<Country, string[]>;

// Actual data
const markets: Market[] = ["Home Win", "Away Win", "Over 2.5"];

const countries: Country[] = ["England", "Spain", "Germany", "Italy", "France"];

const leagues: LeagueMap = {
  England: ["Premier League", "Championship"],
  Spain: ["La Liga", "Segunda Division"],
  Germany: ["Bundesliga", "2. Bundesliga"],
  Italy: ["Serie A", "Serie B"],
  France: ["Ligue 1", "Ligue 2"],
};

const teams: TeamMap = {
  England: ["Arsenal", "Chelsea", "Liverpool", "Man City", "Man United"],
  Spain: ["Real Madrid", "Barcelona", "Atletico Madrid", "Valencia"],
  Germany: ["Bayern Munich", "Dortmund", "Leipzig", "Leverkusen"],
  Italy: ["Juventus", "AC Milan", "Inter", "Napoli"],
  France: ["PSG", "Lyon", "Marseille", "Lille"],
};


  const generated: Record<string, any> = {};
  const now = new Date();

  for (let i = 0; i < 30; i++) {
    const country = countries[Math.floor(Math.random() * countries.length)];
    const league =
      leagues[country][Math.floor(Math.random() * leagues[country].length)];
    const home =
      teams[country][Math.floor(Math.random() * teams[country].length)];
    let away = teams[country][Math.floor(Math.random() * teams[country].length)];
    while (away === home) {
      away = teams[country][Math.floor(Math.random() * teams[country].length)];
    }

    const datetime = new Date(
      now.getTime() + Math.floor(Math.random() * 12) * 60 * 60 * 1000
    ).toISOString();

    generated[`match_${i + 1}`] = {
      datetime,
      market: markets[Math.floor(Math.random() * markets.length)],
      country,
      league,
      home,
      away,
      odds: (1.5 + Math.random() * 2.5).toFixed(2),
    };
  }

  return generated;
})();
