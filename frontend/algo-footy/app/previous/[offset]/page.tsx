"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useParams } from "next/navigation";
import { getAllowedDays } from "@/lib/days";
import { MatchData, Match } from "@/data/mock";
import Image from 'next/image';
import { TiTick } from "react-icons/ti";
import DaysDropdown from "@/components/daysnav";

export default function PreviousLinksPage() {
  const [data, setData] = useState<MatchData>({});
  const [loading, setLoading] = useState(true);
  const [filtered, setFiltered] = useState<Match[]>([]);
  const days = getAllowedDays();
  const pathname = usePathname();
  const params = useParams();

  const offset = Number(params.offset) || 1;

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(`/api/predictions/?day=${offset}`);
        const json: MatchData = await res.json();
        setData(json);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching data:", err);
        setLoading(false);
      }
    }

    fetchData();
  }, [offset]); 
  useEffect(() => {
        if (!data || Object.keys(data).length === 0) return;

        const matches = Object.values(data);
        const filteredMatches = matches.filter((match) => {
        
        return true;
        })
        .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
        setFiltered(filteredMatches);
    }, [data]);
    console.log(data)

  if (loading) return <p className="text-white p-4">Loading...</p>;

  return (
    <main className="flex flex-col p-4 gap-4 w-full">
      <h1 className="text-3xl font-bold">Previous Predictions</h1>

      <DaysDropdown days={days} />
      <div className="hidden lg:flex lg:w-full lg:overflow-y-auto">
        <ol className="flex flex-col w-full gap-4 pr-2">
          {filtered.map((match, index) => (
            <li key={index} className="flex bg-gradient-to-r from-[#001730] to-[#004080] w-full items-center shadow-lg p-2 h-16">
              <div className="flex gap-4">
                <div className="flex flex-col">
                  <Image className="h-7 w-7" src={match.hicon} width={200} height={200} alt="home team badge"/>
                  <Image className="h-7 w-7" src={match.aicon} width={200} height={200} alt="away team badge"/>
                </div>
                <div className="flex flex-col p-2 w-56">
                  <p>{match.home}</p>
                  <p>{match.away}</p>
                  
                </div>
              </div>
              <div className="font-semibold w-28">
                {new Date(match.date).toLocaleString([], { hour: '2-digit', minute: '2-digit', hour12: false, })}
              </div>
              <div className="font-semibold w-28">{match.prediction}</div>
              <div className="font-semibold w-28">{match.odds}</div>
              <div className="font-semibold w-28">{Math.round(match.probability * 100)}%</div>
              <div className="font-semibold w-28">
                  {(!match.hscore && match.hscore !== 0) ||
                  (!match.ascore && match.ascore !== 0) ||
                  isNaN(Number(match.hscore)) ||
                  isNaN(Number(match.ascore))
                    ? "-" 
                    : `${parseInt(match.hscore.toString())} - ${parseInt(match.ascore.toString())}`}
              </div>


              <div className="font-semibold w-28 flex items-center gap-1">
              <TiTick
                size={25}
                className={
                  match.win === true || match.win === "true" || match.win === 1
                    ? "text-green-500"
                    : match.win === false || match.win === "false" || match.win === 0
                    ? "text-red-500"
                    : "text-white"
                }
              />
            </div>

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
              const winner = match.win === true || match.win === "true" || match.win === 1
                    ? "WON"
                    : match.win === false || match.win === "false" || match.win === 0
                    ? "LOST"
                    : "AWAITING UPDATE" 
           return (
              <li key={index} className="flex text-sm flex-col bg-gradient-to-r from-[#001730] to-[#004080] w-full shadow-lg p-2 h-32">
                  <div className="flex text-sm justify-between">
                      <p className={
                          match.win === true || match.win === "true" || match.win === 1
                          ? "text-green-500"
                          : match.win === false || match.win === "false" || match.win === 0
                          ? "text-red-500"
                          : "text-gray-400"
                      }>{winner}</p>

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
                      <p className={
                          match.win === true || match.win === "true" || match.win === 1
                          ? "text-green-500 font-semifold whitespace-nowrap"
                          : match.win === false || match.win === "false" || match.win === 0
                          ? "text-red-500 font-semifold whitespace-nowrap"
                          : "text-gray-400 font-semifold whitespace-nowrap"}>{(!match.hscore && match.hscore !== 0) ||
                           (!match.ascore && match.ascore !== 0) ||
                           isNaN(Number(match.hscore)) ||
                           isNaN(Number(match.ascore))
                           ? "-" 
                           : `${parseInt(match.hscore.toString())} - ${parseInt(match.ascore.toString())}`}</p>
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
    </main>
  );
}
