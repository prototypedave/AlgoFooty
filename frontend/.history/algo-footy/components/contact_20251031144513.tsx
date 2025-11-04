"use client";
import { motion } from "framer-motion";
import { FaFacebook, FaTwitter, FaInstagram, FaPhone, FaMailBulk } from "react-icons/fa";

export default function ContactSection() {
    return (
        <main className="flex flex-col pr-50 gap-16 mb-20">
            <motion.h1
                className="text-9xl font-bold"
                initial={{ x: 300, opacity: 0.5 }}
                whileInView={{ x: 0, opacity: 1 }}
                transition={{ type: "spring", stiffness: 80, damping: 20, duration: 0.8, }}
                viewport={{ once: true, amount: 0.5 }}>
                GET IN TOUCH
            </motion.h1>
            <div className="text-2xl flex justify-between">
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
    );
}