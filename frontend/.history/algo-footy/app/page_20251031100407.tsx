"use client";
import Image from "next/image";
import { motion } from "framer-motion";
import { FaFacebook, FaTwitter, FaInstagram, FaPhone, FaMailBulk } from 'react-icons/fa';
import { GiAzulFlake, GiCartwheel } from "react-icons/gi";

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
        <main className="flex my-40 flex-col gap-10">
            <h1 className="text-8xl font-bold">KEY MARKETS</h1>
            <div className="grid grid-cols-3">
                <div className="col-span-2 flex gap-8">
                  <Image
                      className=""
                      src="/foot3.png"
                      alt="Next.js logo"
                      sizes="(max-width: 1080px) 100vw, 33vw"
                      width={300}
                      height={300}
                      priority
                  />
                  <Image
                      className=""
                      src="/foot2.png"
                      alt="Next.js logo"
                      sizes="(max-width: 1080px) 100vw, 33vw"
                      width={300}
                      height={300}
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
        <main>
          <Image
            className="mx-0 px-0 mb-80"
            src="/crowd1.png"
            alt="Next.js logo"
            sizes="(max-width: 1080px) 100vw, 33vw"
            width={1356}
            height={200}
            priority
          />
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
