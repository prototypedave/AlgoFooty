import { IoMdFootball } from "react-icons/io";

export default function Predictions() {
    return (
        <div className="relative flex flex-col min-h-screen items-center justify-center bg-oxford-blue font-sans">
            <nav className="absolute inset-x-0 top-0 bg-orange-red h-24 rounded-md mx-4 mt-18 shadow-lg flex flex-col">
                <div className="flex">
                    <IoMdFootball />
                    <h1>POPUP <br /> SURE PREDICTS</h1>
                </div>
            </nav>
        </div>
    );
}