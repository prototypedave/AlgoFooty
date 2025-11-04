"use client";

import Link from "next/link";
import { IoMdFootball } from "react-icons/io";
import { usePathname } from "next/navigation";

export default function Predictions() {
    const pathname = usePathname();
    return (
        <div className="relative flex flex-col min-h-screen items-center justify-center bg-oxford-blue font-sans">
            <nav className="absolute inset-x-0 top-0 bg-white text-orange-red h-32 rounded-md mx-4 mt-18 shadow-lg flex flex-col p-4">
                <div className="flex gap-2">
                    <IoMdFootball className="text-4xl"/>
                    <p className="text-lg font-bold leading-none">
                        <span className="block">POPUP SURE </span>
                        <span className="block">PREDICTIONS</span>
                    </p>
                </div>
                <div className="flex items-center gap-20 pt-6 pl-6 font-bold text-lg text-gray-950">
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
                        className={`pb-1 ${
                            pathname === "/predictions"? "border-b-4 border-black font-bold rounded-sm" : "border-b-0"
                        }`}>Predictions</Link>
                    <Link href={"/statistics"}>Statistics</Link>
                </div>
            </nav>
        </div>
    );
}