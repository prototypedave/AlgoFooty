import Image from "next/image";
import { FaFacebook, FaTwitter, FaInstagram, FaPhone, FaMailBulk } from 'react-icons/fa';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-oxford-blue font-sans">
        <main>
          <Image
            className="dark:invert"
            src="/next.svg"
            alt="Next.js logo"
            width={100}
            height={20}
            priority
        />
        </main>
        <main className="flex flex-col pr-50 gap-16">
            <h1 className="text-9xl font-bold">GET IN TOUCH</h1>
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
