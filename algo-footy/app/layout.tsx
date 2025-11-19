
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import NavBar from "@/components/navbar";
import MobileNavBar from "@/components/mobar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Popup Sure Predictions",
  description: "100% Sure predictions that maximizes on your wins and returns",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="relative flex flex-col min-h-screen bg-oxford-blue font-sans">
	  <MobileNavBar />
          <nav className="lg:absolute inset-x-0 top-0 bottom-0 bg-gradient-to-r from-[#001730] to-[#004080] text-white max-h-full rounded-md lg:mx-8 lg:my-14 shadow-lg flex gap-10 lg:p-4">
              <NavBar/>
              {children}
          </nav>
        </div>
      </body>
    </html>
  );
}
