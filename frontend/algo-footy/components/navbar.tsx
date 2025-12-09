"use client";

import { IoMdFootball } from "react-icons/io";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function NavBar() {
    const pathname = usePathname();
    return (
        <div className="hidden xl:flex flex-col">
            <div className="flex gap-2">
                <IoMdFootball className="text-4xl"/>
                <p className="text-lg font-bold leading-none">
                    <span className="block">POPUP SURE </span>
                    <span className="block">PREDICTIONS</span>
                </p>
            </div>
            <div className="flex flex-col items-start gap-2 pt-4 pl-6 font-bold text-lg text-white">
                <Link href="/home" className={`inline-block pb-1 ${ pathname === "/home" ? "border-b-4 border-orange-red font-bold text-orange-red" : "border-b-0 border-orange-red"}`}>Home</Link>
                <Link href="/predictions" className={`inline-block pb-1 ${ pathname === "/predictions"? "border-b-4 border-orange-red font-bold text-orange-red" : "border-b-0 border-orange-red"}`}>Daily Picks</Link>
                <Link href="/sure" className={`inline-block pb-1 ${ pathname === "/sure"? "border-b-4 border-orange-red font-bold text-orange-red" : "border-b-0 border-orange-red"}`}>VIP Sure Tips</Link>
                <Link href="/previous/1" className={`inline-block pb-1 ${ pathname.startsWith("/previous/")? "border-b-4 border-orange-red font-bold text-orange-red" : "border-b-0 border-orange-red"}`}>Previous</Link>
                <Link href="/statistics" className={`inline-block pd-1 ${ pathname.startsWith("/stats/")? "border-b-4 border-orange-red font-bold text-orange-red" : "border-b-0 border-orange-red"}`}>Statistics</Link>
            </div>
        </div>
    )
}
