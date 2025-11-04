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
    <div className="flex flex-col p-4 gap-4 w-full font-sans overflow-y-auto">
      <main className="flex justify-center items-center h-84 bg-orange-red w-full">
          <Link href="/predictions" className="rounded-full bg-white h-20 text-orange-red text-4xl font-bold p-6">
            TODAYS PREDICTIONS
          </Link>
      </main>
          <main className="flex flex-col w-full justify-center bg-orange-red px-20 gap-4">
            <motion.h1
                className="text-9xl font-bold mt-10"
                initial={{ x: 300, opacity: 0.5 }}
                whileInView={{ x: 0, opacity: 1 }}
                transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
                viewport={{ once: true, amount: 0.5 }}>
                POPUP SURE PREDICTIONS
            </motion.h1>
            <p className="text-2xl font-bold text-left pb-10">Join us for accurate predictions, insights, and analysis to enhance your betting experience</p>
            <button className="font-bold text-left text-2xl underline py-10">ALGO-FOOTY APP</button>
          </main>        
    </div>
  );
}
