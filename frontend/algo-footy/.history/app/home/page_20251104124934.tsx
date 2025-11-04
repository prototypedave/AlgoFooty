"use client";
import Image from "next/image";
import { motion } from "framer-motion";
import { FaFacebook, FaTwitter, FaInstagram, FaPhone, FaMailBulk } from 'react-icons/fa';
import { GiAzulFlake, GiCartwheel, GiJusticeStar } from "react-icons/gi";
import { FaMoneyBillTrendUp, FaRankingStar } from "react-icons/fa6";
import { TfiStatsUp } from "react-icons/tfi";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col p-4 gap-4 w-full justify-center font-sans">
      <main className="flex justify-center items-center h-48">
          <Link href="/predictions" className="rounded-full bg-white h-20 text-orange-red text-4xl font-bold p-6">
            TODAYS PREDICTIONS
          </Link>
      </main>
        
    </div>
  );
}
