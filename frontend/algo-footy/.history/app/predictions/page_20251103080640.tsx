"use client";

import Link from "next/link";
import { IoMdFootball } from "react-icons/io";
import { usePathname } from "next/navigation";
import DropdownButton from "@/components/dropdown";

export default function Predictions() {
    const pathname = usePathname();
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
                            <DropdownButton />
                            <DropdownButton />
                            <DropdownButton />
                    </div>
                    <div className="flex w-full">
                        <ol className="flex flex-col w-full gap-4">
                            <li className="flex bg-white/10 backdrop-blur-md w-full shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-white/10 backdrop-blur-md w-full shadow-lg justify-around">
                                <p>icon</p>
                                <div>
                                    <p>team A</p>
                                    <p>team B</p>
                                </div>
                                <p>Prediction</p>
                                <div>odds</div>
                                <div>match time</div>
                            </li>
                            <li className="flex bg-white/10 backdrop-blur-md w-full shadow-lg justify-around">
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