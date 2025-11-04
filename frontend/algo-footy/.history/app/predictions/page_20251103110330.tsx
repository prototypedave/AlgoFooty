"use client";
import { useState } from "react";
import Link from "next/link";
import { IoMdFootball } from "react-icons/io";
import { usePathname } from "next/navigation";
import Dropdown from "@/components/dropdown";
import {data as rawData } from "@/data/mock";

export default function Predictions() {
    const [timeFilter, setTimeFilter] = useState("Next 1hr");
    const [countryFilter, setCountryFilter] = useState("All");
    const [leagueFilter, setLeagueFilter] = useState("All");
    const [marketFilter, setMarketFilter] = useState("All");
    const pathname = usePathname();
    const data = Object.values(rawData);

    const filteredData = data.filter((match) => {
        const now = new Date();
        const matchTime = new Date(match.datetime);

        if (timeFilter !== "All") {
            const hours = parseInt(timeFilter.match(/\d+/)?.[0] || 0);
            const cutoff = new Date(now.getTime() + hours * 60 * 60 * 1000);
            if (matchTime > cutoff) return false;
        }
        if (countryFilter !== "All" && match.country !== countryFilter) return false;
        if (leagueFilter !== "All" && match.league !== leagueFilter) return false;
        if (marketFilter !== "All" && match.market !== marketFilter) return false;

        return true;
    });

    const countries = ["All", ...new Set(data.map((d) => d.country))];
    const leagues = ["All", ...new Set(data.map((d) => d.league))];
    const markets = ["All", ...new Set(data.map((d) => d.market))];

    return (
        <div className="relative flex flex-col min-h-screen items-center justify-center bg-oxford-blue font-sans">
            <nav className="absolute inset-x-0 top-0 bottom-0 bg-gradient-to-r from-[#001730] to-[#004080] text-white max-h-full rounded-md mx-8 my-14 shadow-lg flex gap-10 p-4">
                <div className="flex flex-col">
                    <div className="flex gap-2">
                        <IoMdFootball className="text-4xl"/>
                        <p className="text-lg font-bold leading-none">
                            <span className="block">POPUP SURE </span>
                            <span className="block">PREDICTIONS</span>
                        </p>
                    </div>
                    <div className="flex flex-col items-start gap-2 pt-4 pl-6 font-bold text-lg text-white">
                        <Link
                            href="/home"
                            className={`pb-1 ${
                            pathname === "/home"
                                ? "border-b-4 border-black font-bold"
                                : "border-b-0"
                            }`}
                        >
                            Home
                        </Link>
                        <Link href="/predictions"
                            className={`inline-block pb-1 ${
                                pathname === "/predictions"? "border-b-4 border-orange-red font-bold text-orange-red" : "border-b-0 border-orange-red"
                            }`}>Predictions</Link>
                        <Link href={"/statistics"}>Statistics</Link>
                    </div>
                </div>
                <div className="flex flex-col p-4 gap-4 w-full">
                    <h1 className="text-3xl font-bold">Predictions</h1>
                    <div className="flex gap-10 w-full">
                        <Dropdown
                            label="Time"
                            options={["Next 1hr", "Next 3hrs", "Next 6hrs", "Next 12hrs", "All"]}
                            onSelect={setTimeFilter}
                        />
                        <Dropdown label="Country" options={countries} onSelect={setCountryFilter} />
                        <Dropdown label="League" options={leagues} onSelect={setLeagueFilter} />
                        <Dropdown label="Market" options={markets} onSelect={setMarketFilter} />
                    </div>
                    <div className="flex w-full overflow-y-auto">
                        <ol className="flex flex-col w-full gap-4 pr-2">
                            <li className="flex bg-gradient-to-r from-[#001730] to-[#004080] w-full shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-gradient-to-r from-[#001730] to-[#004080] w-full shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-gradient-to-r from-[#001730] to-[#004080] shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-gradient-to-r from-[#001730] to-[#004080] shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-gradient-to-r from-[#001730] to-[#004080] shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-gradient-to-r from-[#001730] to-[#004080] shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-gradient-to-r from-[#001730] to-[#004080] shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                        </ol>
                    </div>
                </div>
            </nav>
        </div>
    );
}