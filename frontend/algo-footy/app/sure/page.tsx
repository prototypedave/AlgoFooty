"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { IoMdFootball } from "react-icons/io";
import { usePathname } from "next/navigation";
import Dropdown from "@/components/dropdown";
import { MatchData, Match } from "@/data/mock";
import Image from 'next/image';

interface LocalTimeFromNYProps {
  date: string; // ISO string like "2025-11-02T07:30:00"
}

const LocalTimeFromNY: React.FC<LocalTimeFromNYProps> = ({ date }) => {
  const nyTime = new Date(date);

  const localTime = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false, // 24-hour format
  }).format(nyTime);

  return <div>{localTime}</div>;
};


export default function Predictions() {
    const [data, setData] = useState<MatchData>({});
    const [filtered, setFiltered] = useState<Match[]>([]);
    const [loading, setLoading] = useState(true);

    const [timeFilter, setTimeFilter] = useState("All");
    const [countryFilter, setCountryFilter] = useState("All");
    const [leagueFilter, setLeagueFilter] = useState("All");
    const [marketFilter, setMarketFilter] = useState("All");
    const pathname = usePathname();

    useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch('api/vip'); 
        const json: MatchData = await res.json();
        setData(json);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching data:", err);
        setLoading(false);
      }
    }
        fetchData();
    }, []);

    useEffect(() => {
  if (!data || Object.keys(data).length === 0) return;

  const matches = Object.values(data);
  const now = new Date();

  const filteredMatches = matches
    .filter((match) => {
      const matchTime = new Date(match.date);

      if (timeFilter !== "All") {
        const hours = parseInt(timeFilter.match(/\d+/)?.[0] || "0");
        const cutoff = new Date(now.getTime() + hours * 60 * 60 * 1000);
        if (matchTime > cutoff) return false;
      }

      if (countryFilter !== "All" && match.country !== countryFilter) return false;
      if (leagueFilter !== "All" && match.league !== leagueFilter) return false;
      if (marketFilter !== "All" && match.prediction !== marketFilter) return false;

      return true;
    })
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  setFiltered(filteredMatches);
}, [data, timeFilter, countryFilter, leagueFilter, marketFilter]);


    if (loading) return <p className="text-white p-4">Loading...</p>;

    const allMatches = Object.values(data);
    const countries = ["All", ...new Set(allMatches.map((m) => m.country))];
    const leagues = ["All", ...new Set(allMatches.map((m) => m.league))];
    const markets = ["All", ...new Set(allMatches.map((m) => m.prediction))];

    return (
        <div className="flex flex-col p-4 gap-4 w-full">
            <h1 className="text-3xl font-bold">Predictions</h1>
            <div className="hidden lg:flex lg:gap-10 w-full">
                    <Dropdown
                        label="Time"
                        options={["Next 1hr", "Next 3hrs", "Next 6hrs", "Next 12hrs", "All"]}
                        onSelect={setTimeFilter}
                    />
                    <Dropdown label="Country" options={countries} onSelect={setCountryFilter} />
                    <Dropdown label="League" options={leagues} onSelect={setLeagueFilter} />
                    <Dropdown label="Market" options={markets} onSelect={setMarketFilter} />
            </div>
            <div className="hidden lg:flex lg:w-full lg:overflow-y-auto">
                <ol className="flex flex-col w-full gap-4 pr-2">
                    {filtered.map((match, index) => (
                        <li key={index} className="flex bg-gradient-to-r from-[#001730] to-[#004080] w-full items-center shadow-lg p-2 h-16">
                            <div className="flex gap-4">
                                <div className="flex gap-6 w-56">
                                    <Image 
                                        className="h-7 w-7"
                                        src={match.hicon}
                                        width={200}
                                        height={200}
                                        alt="Picture of the author"
                                    />
                                    <p>{match.home}</p>
                                </div>
                                <p className="w-14">vs</p>
                                <div className="flex gap-6 w-56">
                                    <p>{match.away}</p>
                                    <Image 
                                        className="h-7 w-7"
                                        src={match.aicon}
                                        width={200}
                                        height={200}
                                        alt="Picture of the author"
                                    />
                                </div>
                            </div>
                            <div className="font-semibold w-28">
                                {new Date(match.date).toLocaleString([], {
                                    hour: '2-digit',
                                    minute: '2-digit',
                                    hour12: false, 
                                })}
                            </div>
                            <div className="font-semibold w-28">{match.prediction}</div>
                            <div className="font-semibold w-28">{match.odds}</div>
                            <div className="font-semibold w-28">{Math.round(match.probability * 100)}%</div>
                        </li>
                    ))}
                </ol>
            </div>
            <div className="flex flex-col w-full gap-4 lg:hidden">
                {filtered.map((match, index) => {
                    const date = new Date(match.date);
                    const formattedDate = date.toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                    });
                    return (
                        <li key={index} className="flex flex-col bg-gradient-to-r from-[#001730] to-[#004080] w-full shadow-lg p-2 h-32">
                            <div className="flex text-sm justify-between">
                                <p className="left-0 text-gray-400">{formattedDate}, {new Date(match.date).toLocaleString([], {
                                    hour: '2-digit',
                                    minute: '2-digit',
                                    hour12: false, 
                                })}</p>
                 
                            </div>
                            <div className="flex pt-4 gap-4 justify-between items-center">
                                 <div className="flex justify-between items-center font-bold">
                                    <Image 
                                        className="h-10 w-10 pr-2"
                                        src={match.hicon}
                                        width={500}
                                        height={500}
                                        alt="home icon"
                                    />
                                    <p>{match.home}</p>
                                </div>
                                <p className="">vs</p>
                                <div className="flex justify-between items-center justify-center font-bold">
                                    <p>{match.away}</p>
                                    <Image 
                                        className="h-10 w-10 pl-2"
                                        src={match.aicon}
                                        width={500}
                                        height={500}
                                        alt="away icon"
                                    />
                                </div>
                            </div>
			                <div className="flex pt-4 text-sm justify-between text-gray-300 font-semibold">
                                <p>Pick: <span className="text-orange-red">{match.prediction}</span></p>
                                <p>Odds: <span>{match.odds}</span></p>
                                <p>Chance: <span> {Math.round(match.probability * 100)}%</span></p>

                            </div>
                        </li>
                    );
                })}
            </div>
        </div>
    );
}
