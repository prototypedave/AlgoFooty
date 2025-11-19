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
    <div className="flex flex-col lg:p-4 w-full font-sans overflow-y-auto hide-scrollbar">
      <main className="hidden lg:flex lg:justify-center lg:items-center lg:h-64 lg:w-full lg:p-6">
        <Link href="/predictions" className="rounded-full bg-white text-orange-red text-2xl font-bold p-4">
          Get Todays Predictions
        </Link>
      </main>
      <main className="flex flex-col w-full justify-center bg-orange-red px-10 lg:px-20 gap-4">
        <div className="flex flex-col">
          <motion.h1
            className="text-2xl lg:text-5xl font-bold mt-5 lg:mt-10"
            initial={{ x: 150, opacity: 0.7 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
            viewport={{ once: true, amount: 0.5 }}>
            POPUP SURE
          </motion.h1>
          <motion.h1
            className="text-2xl lg:text-5xl font-bold"
            initial={{ x: 150, opacity: 0.7 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
            viewport={{ once: true, amount: 0.5 }}>
            PREDICTIONS
          </motion.h1>
        </div>
        <p className="text-lg lg:text-xl font-bold text-left pb-5 lg:pb-10">Join us for accurate predictions, insights, and analysis to enhance your betting experience</p>
        <Link href="/predictions" className="font-bold text-left text-lg lg:text-2xl underline py-5 lg:py-10">ALGO-FOOTY APP</Link>
      </main>    
      <main className="grid grid-cols-1 lg:grid-cols-3">
        <div className="col-span-2 flex flex-col py-17 lg:py-34 px-10 lg:px-20 lg:gap-4">
          <GiAzulFlake className="text-2xl lg:text-3xl lg:pb-0 pb-2"/>
          <motion.h1
            className="text-2xl lg:text-4xl font-bold"
            initial={{ x: 150, opacity: 0.7 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
            viewport={{ once: true, amount: 0.5 }}>
            SURE MATCH
          </motion.h1>
          <motion.h1
            className="text-3xl lg:text-6xl font-bold lg:pb-0 pb-4"
            initial={{ x: 150, opacity: 0.5 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
            viewport={{ once: true, amount: 0.5 }}>
            PREDICTIONS
          </motion.h1>
          <p className="lg:text-md text-base">Maximize your wins with our 100% AI predictions. Our hybrid model ensures top most accuracy while analysing upcoming matches
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
      <main className="flex my-20 lg:my-40 flex-col gap-5 lg:gap-10 px-10 lg:px-20">
        <motion.h1
          className="text-xl lg:text-3xl font-bold"
          initial={{ x: 150, opacity: 0.7 }}
          whileInView={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
          viewport={{ once: true, amount: 0.5 }}>
          KEY MARKETS
        </motion.h1>
        <div className="grid grid-cols-1 lg:grid-cols-3">
          <div className="col-span-2 flex lg:gap-8">
            <Image
              className=""
              src="/foot3.png"
              alt="Next.js logo"
              width={300}
              height={400}
              priority
            />
            <Image
              className="hidden lg:block"
              src="/foot2.png"
              alt="Next.js logo"
              width={300}
              height={400}
              priority
            />
          </div>
          <div className="flex flex-col gap-4 pt-17 lg:pt-0 lg:gap-4 lg:pl-20">
            <GiCartwheel className="lg:text-3xl text-xl font-bold"/>
            <p className="lg:text-md text-base">Discover our top preferred betting markets and those that makes 
              waves this season, showcasing their winning rates and return on stake, 
              ranked from the best in terms of ROI and performance</p>
          </div>
        </div>
      </main>
      <main className="flex flex-col w-full px-10 lg:px-20">
        <motion.h1
          className="lg:text-3xl text-xl font-bold text-right"
          initial={{ x: -150, opacity: 0.7 }}
          whileInView={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
          viewport={{ once: true, amount: 0.8 }}>
          PREDICTIONS
        </motion.h1>
        <motion.h1
          className="lg:text-5xl text-3xl font-bold text-right pb-5 lg:pb-10"
          initial={{ x: -150, opacity: 0.7 }}
          whileInView={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
          viewport={{ once: true, amount: 0.8 }}>
          TRENDS
        </motion.h1>
        <div className="grid lg:grid-cols-3 grid-cols-1">
          <div className="flex flex-row gap-2 lg:gap-4 items-end">
            <div className="flex flex-col gap-4">
              <FaMoneyBillTrendUp className="lg:text-3xl text-xl"/>
              <p className="text-md">Dont be in the hideout to track the performance of our betting 
                tips over given periods and markets to help you in best choices and practices to explore
              </p>
            </div>
          </div>
          <div className="col-span-2 flex pt-7 lg:pt-0">
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
      <main className="grid grid-cols-1 lg:grid-cols-3 px-10 lg:px-20 mt-20 lg:mt-40 gap-5 lg:gap-10 mb-20 lg:mb-40">
        <div className="flex flex-col lg:gap-10 w-full h-full">
          <Image
            className="h-64"
            src="/chance3.jpeg"
            alt="Next.js logo"
            width={300}
            height={200}
            priority
          />
          <Image
            className="h-64 hidden lg:block"
            src="/chance4.jpeg"
            alt="Next.js logo"
            width={300}
            height={200}
            priority
          />
        </div>
        <div className="col-span-2 content-center">
          <FaRankingStar className="lg:text-3xl text-2xl"/>
          <motion.h1
            className="lg:text-6xl text-3xl font-bold"
            initial={{ x: 150, opacity: 0.7 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
            viewport={{ once: true, amount: 0.5 }}>
            PROBALISTIC
          </motion.h1>
          <motion.h1
            className="lg:text-4xl text-2xl font-bold"
            initial={{ x: 150, opacity: 0.7 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
            viewport={{ once: true, amount: 0.5 }}>
            PREDICTIONS
          </motion.h1>
          <p className="lg:text-md text-base">Get predictions with probability ratings to act as a guide on 
            high risky predictions and low risk predictions as well as favourites 
            to win just to meet your right risk</p>
        </div>
      </main>
      <main className="grid lg:grid-cols-3 grid-cols-1 gap-5 lg:gap-10 px-10 lg:px-20">
        <div className="content-end">
          <TfiStatsUp className="lg:text-3xl text-xl my-2 lg:my-4"/>
          <motion.h1
            className="lg:text-4xl text-2xl font-bold"
            initial={{ x: 150, opacity: 0.7 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
            viewport={{ once: true, amount: 0.5 }}>
            STATISTICAL INSIGHTS
          </motion.h1>
          <p className="lg:text-md text-base my-2 lg:my-4">Use our diverse and extensive match stats to make correct 
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
      <main className="flex flex-col mt-10 lg:mt-20">
        <Image
          className="mx-0 px-0 h-64 lg:h-auto"
          src="/crowd1.png"
          alt="Next.js logo"
          sizes="(max-width: 1080px) 100vw, 33vw"
          width={1356}
          height={200}
          priority
        />
        <div className="grid lg:grid-cols-3 grid-cols-1 py-10 lg:py-20 mb-30 lg:mb-60 px-10 lg:px-20">
          <div className="col-span-2 pt-10 lg:pt-10">
            <motion.h1
              className="lg:text-4xl text-2xl font-bold"
              initial={{ x: 150, opacity: 0.7 }}
              whileInView={{ x: 0, opacity: 1 }}
              transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
              viewport={{ once: true, amount: 0.5 }}>
              USER
            </motion.h1>
            <motion.h1
              className="lg:text-6xl text-3xl font-bold"
              initial={{ x: 150, opacity: 0.7 }}
              whileInView={{ x: 0, opacity: 1 }}
              transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
              viewport={{ once: true, amount: 0.5 }}>
              TESTIMONIALS
            </motion.h1>
          </div> 
          <div className="span-col-1 pt-5 lg:pt-0">
            <GiJusticeStar className="lg:text-3xl text-xl my-2 lg:my-4"/>
              <p className="lg:text-md txt-base my-2 lg:my-4">Discover how our app has transformed football predictions for fans and bettors alike. 
                Join our community of successul users who have tried our app and liked it.</p>
          </div>   

        </div>
      </main>
      <main className="flex flex-col px-10 lg:px-0 lg:pr-50 gap-8 lg:gap-16 mb-10 lg:mb-20">
        <motion.h1
          className="lg:text-5xl text-3xl font-bold"
          initial={{ x: 150, opacity: 0.7 }}
          whileInView={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
          viewport={{ once: true, amount: 0.5 }}>
          GET IN TOUCH
        </motion.h1>
        <div className="lg:text-xl text-lg flex flex-col lg:flex-row gap-2 lg:gap-0 lg:justify-between">
          <div className="flex flex-col gap-2 lg:gap-4">
            <p className="flex gap-2"><FaFacebook size={30} /> Popup Sure Predicts </p>
            <p className="flex gap-2"><FaTwitter size={30} color="lightblue" />@popup_sure_predicts</p>
            <p className="flex gap-2"><FaInstagram size={30} color="purple" />@popup_sure_predicts</p>
          </div>
          <div className="flex flex-col gap-2 lg:gap-4">
            <p className="flex gap-2"><FaPhone size={30} />+254712345678</p>
            <p className="flex gap-2"><FaMailBulk size={30} />popupgfj@gmail.com</p>
          </div>
        </div>
      </main>    
          
        
    </div>
  );
}
