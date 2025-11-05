"use client";
import Image from "next/image";
import { motion } from "framer-motion";
import { FaFacebook, FaTwitter, FaInstagram, FaPhone, FaMailBulk } from 'react-icons/fa';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-oxford-blue font-sans">
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
              initial={{ x: 200, opacity: 0.5 }} // Start off-screen to the right
              whileInView={{ x: 0, opacity: 1 }} // Animate to position when visible
              transition={{
                type: "spring",
                stiffness: 70,
                damping: 15,
                duration: 1.2
              }}
              viewport={{ once: true, amount: 0.6 }} // Trigger once when 60% visible
            >
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
