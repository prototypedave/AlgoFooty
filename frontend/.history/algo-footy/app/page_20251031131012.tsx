"use client";
import Image from "next/image";
import { motion } from "framer-motion";
import { FaFacebook, FaTwitter, FaInstagram, FaPhone, FaMailBulk } from 'react-icons/fa';
import { GiAzulFlake, GiCartwheel } from "react-icons/gi";
import { FaMoneyBillTrendUp, FaRankingStar } from "react-icons/fa6";
import { TfiStatsUp } from "react-icons/tfi";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-oxford-blue font-sans">
        <main className="grid grid-cols-3">
            <div className="col-span-2 flex flex-col py-34 px-20 gap-4">
                <GiAzulFlake className="text-8xl"/>
                <h1 className="text-8xl font-bold">SURE MATCH PREDICTIONS</h1>
                <p className="text-xl">Maximize your wins with our 100% AI predictions. Our hybrid model ensures top most accuracy while analysing upcoming matches
                  and selects the best matches for different markets. If we can make profits from it so can you, what are you waiting for lets get you started...click
                </p>
            </div>
            <div className="flex">
                <Image
                    className=""
                    src="/foot1.png"
                    alt="Next.js logo"
                    sizes="(max-width: 1080px) 100vw, 33vw"
                    width={500}
                    height={1368}
                    priority
                />
            </div>
        </main>
        <main className="flex my-40 flex-col gap-10 px-20">
            <h1 className="text-8xl font-bold ">KEY MARKETS</h1>
            <div className="grid grid-cols-3">
                <div className="col-span-2 flex gap-8">
                  <Image
                      className=""
                      src="/foot3.png"
                      alt="Next.js logo"
                      width={300}
                      height={400}
                      priority
                  />
                  <Image
                      className=""
                      src="/foot2.png"
                      alt="Next.js logo"
                      sizes="(max-width: 1080px) 100vw, 33vw"
                      width={300}
                      height={400}
                      priority
                  />
                </div>
                <div className="flex flex-col gap-4 pr-20">
                    <GiCartwheel className="text-6xl"/>
                    <p className="text-xl">Discover our top preferred betting markets and those that makes 
                      waves this season, showcasing their winning rates and return on stake, 
                      ranked from the best in terms of ROI and performance</p>
                </div>
            </div>
        </main>
        <main className="flex flex-col w-full px-20">
            <h1 className="text-right text-8xl font-bold">PREDICTION</h1>
            <h1 className="text-right text-8xl font-bold pb-10">TRENDS</h1>
            <div className="grid grid-cols-3">
              <div className="flex flex-col gap-4 pt-10">
                  <FaMoneyBillTrendUp className="text-8xl"/>
                  <p className="text-xl">Dont be in the hideout to track the performance of our betting 
                    tips over given periods and markets to help you in best choices and practices to explore</p>
              </div>
              <div className="col-span-2 flex">
                <Image
                    className=""
                    src="/trends.png"
                    alt="Next.js logo"
                    width={1000}
                    height={200}
                    priority
                />
              </div>
            </div>
        </main> 
        <main className="grid grid-cols-3 px-20 mt-40 gap-10 mb-40">
            <div className="flex flex-col gap-10 w-full h-full">
                <Image
                    className="h-64"
                    src="/chance3.jpeg"
                    alt="Next.js logo"
                    width={300}
                    height={200}
                    priority
                />
                <Image
                    className="h-64"
                    src="/chance4.jpeg"
                    alt="Next.js logo"
                    width={300}
                    height={200}
                    priority
                />
            </div>
            <div className="col-span-2 content-end">
                <FaRankingStar className="text-8xl"/>
                <h1 className="text-8xl font-bold">PROBALISTIC PREDICTIONS</h1>
                <p className="text-xl">Get predictions with probability ratings to act as a guide on 
                  high risky predictions and low risk predictions as well as favourites 
                  to win just to meet your right risk</p>
            </div>
        </main>
        <main className="grid grid-cols-3 gap-10 px-20">
            <div className="content-end">
                <TfiStatsUp className="text-8xl my-4"/>
                <h1 className="text-6xl font-bold my-4">STATISTICAL INSIGHTS</h1>
                <p className="text-xl my-4">Use our diverse and extensive match stats to make correct 
                  prediction based on trends and maximize on your wins</p>
            </div>
            <div className="col-span-2 w-full">
                <Image
                  className="mx-0 px-0"
                  src="/stats.png"
                  alt="Next.js logo"
                  width={850}
                  height={200}
                  priority
                />
            </div>
        </main> 
        <main className="flex flex-col mt-20">
          <Image
            className="mx-0 px-0"
            src="/crowd1.png"
            alt="Next.js logo"
            sizes="(max-width: 1080px) 100vw, 33vw"
            width={1356}
            height={200}
            priority
          />
          <div className="grid grid-cols-3 py-20">
              <div className="span-col-2">
                  <h1 className="text-8xl font-bold my-4 text center">USER TESTIMONIALS</h1>
              </div>  

          </div>
        </main>
        <main className="flex flex-col pr-50 gap-16 mb-20">
            <motion.h1
                className="text-9xl font-bold"
                initial={{ x: 300, opacity: 0.5 }}
                whileInView={{ x: 0, opacity: 1 }}
                transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
                viewport={{ once: true, amount: 0.5 }}>
                GET IN TOUCH
            </motion.h1>
            <div className="text-4xl flex justify-between">
              <div className="flex flex-col gap-4">
                <p className="flex gap-2"><FaFacebook size={40} /> Popup Sure Predicts </p>
                <p className="flex gap-2"><FaTwitter size={40} color="lightblue" />@popup_sure_predicts</p>
                <p className="flex gap-2"><FaInstagram size={40} color="purple" />@popup_sure_predicts</p>
              </div>
              <div className="flex flex-col gap-4">
                <p className="flex gap-2"><FaPhone size={40} />+254712345678</p>
                <p className="flex gap-2"><FaMailBulk size={40} />popupgfj@gmail.com</p>
              </div>
            </div>
        </main>
    </div>
  );
}
