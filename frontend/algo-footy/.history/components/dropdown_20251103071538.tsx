"use client";
import { useState } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

export default function DropdownButton() {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative inline-block text-left">
      {/* Button */}
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center justify-between gap-10 text-white-500 px-4 py-2 shadow-md hover:text-orange-red transition"
      >
        Time
        {open ? (
          <FaChevronUp className="text-sm" />
        ) : (
          <FaChevronDown className="text-sm" />
        )}
      </button>

      {/* Dropdown Menu */}
      {open && (
        <div className="absolute right-0 mt-2 w-48 shadow-lg">
          <ul className="py-1">
            <li>
              <a
                href="#profile"
                className="block px-4 py-2 text-white-300 hover:bg-orange-red"
              >
                Next 1hr
              </a>
            </li>
            <li>
              <a
                href="#settings"
                className="block px-4 py-2 text-white-200 hover:bg-orange-red"
              >
                Next 3hrs
              </a>
            </li>
            <li>
              <a
                href="#logout"
                className="block px-4 py-2 text-white-300 hover:bg-orange-red"
              >
                Next 6hrs
              </a>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}
