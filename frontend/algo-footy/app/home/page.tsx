"use client";
import Image from "next/image";
import { motion } from "framer-motion";
import { FaFacebook, FaTwitter, FaInstagram, FaPhone, FaMailBulk } from 'react-icons/fa';
import { GiAzulFlake, GiCartwheel, GiJusticeStar } from "react-icons/gi";
import { FaMoneyBillTrendUp, FaRankingStar } from "react-icons/fa6";
import { TfiStatsUp } from "react-icons/tfi";
import Link from "next/link";
import { useState, useEffect } from "react";

export default function Home() {
  const slides = [
    (
      <main className="flex flex-col w-full justify-center lg:bg-orange-red/95 px-10 lg:px-20 py-10 lg:py-10 gap-6 text-white lg:rounded-md shadow-xl">
        <div className="flex flex-col">
          <motion.h1
            className="text-3xl lg:text-3xl font-extrabold tracking-tight"
            initial={{ x: 120, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 70, damping: 18, duration: 0.7 }}
            viewport={{ once: true, amount: 0.4 }}
          >
            POPUP SURE
          </motion.h1>

          <motion.h1
            className="text-3xl lg:text-4xl font-extrabold tracking-tight -mt-1"
            initial={{ x: 120, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 70, damping: 18, duration: 0.7, delay: 0.1 }}
            viewport={{ once: true, amount: 0.4 }}
          >
            PREDICTIONS
          </motion.h1>
        </div>

        <motion.p
          className="text-lg lg:text-xl font-medium max-w-3xl leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          viewport={{ once: true, amount: 0.4 }}
        >
          Daily football predictions selected by our deep learning models.  
          Free tips for all users, and elite hand-picked VIP selections  
          for bettors who value <span className="font-bold">consistency wins with 100% accuracy</span> over risky high odds.
        </motion.p>

        <motion.p
          className="text-base lg:text-lg font-light text-white/90"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.7, delay: 0.35 }}
          viewport={{ once: true, amount: 0.4 }}
        >
          Smarter betting starts with reliable insights, accurate match analysis, and a winning strategy.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.45 }}
          viewport={{ once: true, amount: 0.4 }}
        >
          <Link
            href="/predictions"
            className="inline-block bg-white text-orange-red font-bold text-lg lg:text-2xl px-6 py-3 lg:px-10 lg:py-4 rounded-full shadow-lg hover:scale-105 transition-transform duration-200"
          >
            Explore Predictions →
          </Link>
        </motion.div>
      </main>
    ),

    ( 
      <main className="grid grid-cols-1 lg:grid-cols-3 lg:bg-orange-red/95 text-white lg:rounded-md shadow-xl lg:h-full">
        <div className="col-span-2 flex flex-col py-16 lg:py-10 px-10 lg:px-20 lg:gap-4">
          <GiAzulFlake className="text-2xl lg:text-3xl lg:pb-0 pb-2 lg:hidden"/>
          <motion.h1
            className="text-4xl lg:text-4xl font-extrabold tracking-tight text-white"
    
          >
            VIP SURE MATCH
          </motion.h1>
          <motion.h1
            className="text-3xl lg:text-3xl font-extrabold tracking-tight -mt-2"
          >
            PREDICTIONS
          </motion.h1>
          <motion.p
            className="text-base lg:text-lg leading-relaxed max-w-2xl text-white/95"
          >
            Unlock exclusive hand-picked VIP tips built for bettors who value
            <span className="font-bold"> consistency, accuracy, and long-term profits</span>.
            Our hybrid AI model analyzes hundreds of datasets to select only the
            safest matches for our premium users.
            <br /><br />
            Join VIP today and bet with confidence — because winning shouldn’t depend on luck.
          </motion.p>

          {/* CTA */}
          <motion.div
          >
            <Link
              href="/vip"
              className="inline-block bg-white text-orange-red font-bold text-lg lg:text-2xl px-6 py-3 lg:px-10 lg:py-4 rounded-full shadow-lg hover:scale-105 transition-transform duration-200"
            >
              Join VIP & Start Winning →
            </Link>
          </motion.div>
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
    ),
    
    (
      <main className="flex my-20 lg:my-0 lg:py-10 flex-col gap-8 lg:gap-10 px-10 lg:px-20">
        {/* SECTION TITLE */}
        <motion.h1
          className="text-xl lg:text-4xl font-extrabold tracking-tight"
          initial={{ x: 150, opacity: 0.4 }}
          whileInView={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8 }}
          viewport={{ once: true, amount: 0.5 }}
        >
          KEY BETTING MARKETS WE SPECIALIZE IN
        </motion.h1>

        {/* GRID LAYOUT */}
        <div className="grid grid-cols-1 lg:grid-cols-3">
          
          {/* IMAGES */}
          <div className="col-span-1 flex gap-4 lg:gap-8 justify-center">
            <Image
              src="/foot3.png"
              alt="Football analytics visualization"
              width={300}
              height={400}
              className="rounded-xl shadow-lg"
              priority
            />

          </div>

          {/* TEXT RIGHT */}
          <div className="col-span-2 flex flex-col gap-5 lg:pl-20 mt-10 lg:mt-0">
            <GiCartwheel className="text-2xl lg:text-4xl text-orange-300 drop-shadow lg:hidden" />

            <h2 className="text-2xl lg:text-3xl font-bold">
              Our High-Confidence Betting Markets
            </h2>

            <p className="lg:text-md text-base leading-relaxed">
              Our AI-powered engine analyzes thousands of variables to deliver the 
              strongest markets this season — proven for consistency and profit:
            </p>

            <ul className="list-disc pl-5 space-y-2 lg:text-md text-base font-medium">
              <li><strong>Home Win (1)</strong> – Strong value when home form dominates.</li>
              <li><strong>Away Win (2)</strong> – High-precision picks powered by form and tactical models.</li>
              <li><strong>Over 2.5 Goals</strong> – Our top-ranked goals market for reliability.</li>
            </ul>

            <p className="lg:text-md text-base leading-relaxed">
              These markets consistently show the highest ROI across all leagues we track.
              Whether you're betting casually or professionally, these predictions 
              ensure stable long-term returns.
            </p>
          </div>

        </div>
      </main>
    ),
    (
      <main className="flex flex-col w-full px-10 lg:px-20 my-20 lg:my-0 lg:py-10">
        {/* Section Title */}
        <div className="lg:text-right text-left">
          <motion.h1
            className="text-xl lg:text-3xl font-extrabold tracking-tight"
          >
            PREDICTION PERFORMANCE
          </motion.h1>

          <motion.h2
            className="text-3xl lg:text-4xl font-extrabold tracking-tight text-orange-red pb-5 lg:pb-10"
          >
            TRENDS & INSIGHTS
          </motion.h2>
        </div>

        {/* Body */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          
          {/* Left Column — Explanation */}
          <div className="lg:col-span-2 flex flex-row gap-4 items-start">
            <p className="text-base lg:text-lg leading-relaxed">
              Track the real performance of our daily football predictions — including wins,
              losses, profit margins, and overall return on stake.
              <br /><br />
              We believe in full transparency. Our trends show exactly how each market 
              performs over time, helping you make smarter decisions and follow the 
              best-performing strategies for consistent returns.
            </p>
          </div>

          {/* Right Column — Image */}
          <div className="col-span-2 lg:col-span-1 flex justify-center">
            <Image
              src="/trends.png"
              alt="Football prediction performance trends"
              width={1000}
              height={400}
              priority
              className="object-contain"
            />
          </div>
        </div>
      </main>
    ),

    (
      <main className="grid grid-cols-1 lg:grid-cols-3 px-10 lg:px-20 mt-20 lg:mt-0 gap-10 mb-20 lg:mb-0">
        
        {/* IMAGES */}
        <div className="flex flex-col gap-6 lg:gap-10 w-full h-full">
          <Image
            className="h-64 object-cover lg:object-contain lg:h-48 rounded-xl shadow-lg"
            src="/chance3.jpeg"
            alt="Match probability predictions"
            width={300}
            height={200}
            priority
          />

          <Image
            className="h-64 object-cover lg:object-contain lg:h-48 rounded-xl shadow-lg hidden lg:block"
            src="/chance4.jpeg"
            alt="AI confidence levels for football predictions"
            width={300}
            height={200}
            priority
          />
        </div>

        {/* TEXT CONTENT */}
        <div className="col-span-2 flex flex-col justify-center lg:pl-10">
          <FaRankingStar className="lg:text-4xl text-3xl text-orange-red mb-3" />

          <motion.h1
            className="lg:text-4xl text-3xl font-extrabold tracking-tight"
            initial={{ x: 120, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20 }}
            viewport={{ once: true, amount: 0.4 }}
          >
            PROBABILISTIC
          </motion.h1>

          <motion.h1
            className="lg:text-3xl text-2xl font-extrabold tracking-tight -mt-1 mb-4"
            initial={{ x: 120, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            transition={{ type: "spring", stiffness: 80, damping: 20, delay: 0.1 }}
            viewport={{ once: true, amount: 0.4 }}
          >
            PREDICTIONS
          </motion.h1>

          <p className="lg:text-base text-base leading-relaxed text-gray-200/90">
            Every match on our platform includes a confidence rating — a percentage 
            score powered by our AI model that reflects the likelihood of each outcome.
            <br /><br />
            These probability scores help you instantly identify:
            <br />• <strong>High-confidence picks</strong> for safer betting  
            <br />• <strong>Medium-risk opportunities</strong> with better payouts  
            <br />• <strong>High-risk, high-reward selections</strong> for strategic bettors  
            <br /><br />
            Whether you prefer safer choices or bold predictors, our probability 
            engine guides you toward better, more informed decisions.
          </p>
        </div>
      </main>
    ),

    (
      <main className="grid grid-cols-1 lg:grid-cols-3 gap-10 px-10 lg:px-20 py-10 lg:py-10 items-center">
        {/* LEFT TEXT SECTION */}
        <div className="flex flex-col justify-center lg:pr-8">
          <TfiStatsUp className="text-2xl lg:text-4xl mb-3 text-orange-400 lg:hidden" />

          <motion.h1
            className="text-2xl lg:text-3xl font-extrabold leading-tight"
          >
            STATISTICAL INSIGHTS
          </motion.h1>

          <p className="text-base lg:text-lg mt-4 opacity-90">
            Deep insights into leagues, teams, and countries. Discover which clubs 
            consistently hit our predictions — and which markets perform best over time.
          </p>
        </div>

        {/* IMAGE */}
        <div className="col-span-2 w-full flex justify-center">
          <Image
            src="/stats.png"
            alt="Team and league betting statistics insights"
            width={950}
            height={400}
            className="rounded-xl shadow-lg w-full h-auto object-contain"
            priority
          />
        </div>
      </main>

    ),
    ( 
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
    ),
    (
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
    ),
  ];
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex(i => (i + 1) % slides.length);
    }, 10000); 

    return () => clearInterval(timer);
  }, []);  
  return (
    <div className="flex flex-col lg:p-4 w-full font-sans overflow-y-auto hide-scrollbar">
      <div className="flex flex-col lg:hidden w-full">
        {slides.map((slide, i) => (
          <div key={i} className="w-full">
            {slide}
          </div>
        ))}
      </div>

      <div className="hidden lg:flex w-full h-auto relative overflow-hidden">
        <motion.div
          key={index}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.8 }}
          className="w-full"
        >
          {slides[index]}
        </motion.div>
      </div>
      
        
    </div>
  );
}
