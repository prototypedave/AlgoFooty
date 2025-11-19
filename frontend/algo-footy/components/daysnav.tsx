import { useState } from "react";
import Link from "next/link";
import { FaChevronDown } from "react-icons/fa";
import { usePathname } from "next/navigation";

export default function DaysDropdown({ days }: { days: { label: string; offset: number }[] }) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  const currentDay = days.find((d) => pathname === `/previous/${d.offset}`)?.label || "Yesterday";
  return (
    <div className="relative inline-block text-left w-full lg:max-w-xs">
      <button
        onClick={() => setOpen(!open)}
        className="flex justify-between items-center w-full bg-[#002147] text-white font-semibold px-4 py-2 rounded-md hover:bg-[#003366] transition-colors"
      >
        <span className="text-orange-red">{currentDay.charAt(0).toUpperCase() + currentDay.slice(1)}</span>
        <FaChevronDown
          className={`transition-transform text-orange-red ${open ? "rotate-180" : "rotate-0"}`}
          size={20}
        />
      </button>

      {open && (
        <ul className="absolute mt-2 w-full bg-[#001730] border border-[#003366] rounded-md shadow-lg z-10">
          {days.map(({ label, offset }) => {
            const href = `/previous/${offset}`;
            const isActive = pathname === href;

            return (
              <li key={offset}>
                <Link
                  href={href}
                  onClick={() => setOpen(false)}
                  className={`block px-4 py-2 rounded-md transition-colors
                    ${
                      isActive
                        ? "bg-[#003366] text-orange-red font-bold"
                        : "text-gray-300 hover:bg-white/10 hover:text-white"
                    }`}
                >
                  {label.charAt(0).toUpperCase() + label.slice(1)}
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
