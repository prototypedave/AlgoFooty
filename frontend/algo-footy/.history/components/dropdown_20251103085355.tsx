"use client";
import { useState, useEffect, useRef } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

interface DropdownProps {
  label?: string;
  options: string[];
  onSelect: (value: string) => void;
}

export default function Dropdown({ label, options, onSelect }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(options[0]);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleSelect = (option: string) => {
    setSelected(option);
    setIsOpen(false);
    onSelect(option);
  };

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={dropdownRef} className="relative inline-block w-48 text-white">
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className="flex justify-between items-center w-full bg-[#002147] hover:bg-[#003366] px-4 py-2 rounded-md"
      >
        <span className="text-sm font-medium">
          {label ? `${label}: ${selected}` : selected}
        </span>
        {isOpen ? (
          <FaChevronUp className="ml-2 transition-transform" />
        ) : (
          <FaChevronDown className="ml-2 transition-transform" />
        )}
      </button>

      {isOpen && (
        <ul className="absolute left-0 mt-2 w-full bg-[#001730] border border-[#004080] rounded-md z-10 max-h-60 overflow-y-auto shadow-lg">
          {options.map((option) => (
            <li
              key={option}
              onClick={() => handleSelect(option)}
              className={`px-4 py-2 cursor-pointer transition ${
                option === selected
                  ? "bg-[#004080] font-semibold"
                  : "hover:bg-[#003366]"
              }`}
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
