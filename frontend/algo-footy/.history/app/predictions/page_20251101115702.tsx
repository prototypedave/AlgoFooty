import { IoMdFootball } from "react-icons/io";

export default function Predictions() {
    return (
        <div className="relative flex flex-col min-h-screen items-center justify-center bg-oxford-blue font-sans">
            <nav className="absolute inset-x-0 top-0 bg-orange-red h-24 rounded-md mx-4 mt-18 shadow-lg flex flex-col">
                <div className="flex gap-2">
                    <IoMdFootball className="text-4xl"/>
                    <p className="text-lg font-bold leading-tight">
                        <span className="block">POPUP</span>
                        <span className="block">SURE PREDICTS</span>
                    </p>
                </div>
            </nav>
        </div>
    );
}