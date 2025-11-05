"use client";
import { useState } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

interface DropdownProps {
  label?: string;
  options: string[];
  onSelect: (value: string) => void;
}

export default function Dropdown({ label, options, onSelect }: DropdownProps) {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [selected, setSelected] = useState<string>(options[0]);

  const handleSelect = (option: string) => {
    setSelected(option);
    setIsOpen(false);
    onSelect(option);
  };

  return (
    <div className="relative inline-block w-48 text-white">
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className="flex justify-between items-center w-full bg-[#002147] hover:bg-[#003366] px-4 py-2 rounded-md"
      >
        {label && (
        <span className="mb-1 text-sm text-gray-300 font-medium">{label}</span>
      )}
        <FaChevronDown
          className={`transition-transform ${isOpen ? <FaChevronUp/> : ""}`}
        />
      </button>

      {isOpen && (
        <ul className="absolute left-0 mt-2 w-full bg-[#001730] border border-[#004080] rounded-md z-10 max-h-60 overflow-y-auto">
          {options.map((option) => (
            <li
              key={option}
              onClick={() => handleSelect(option)}
              className="px-4 py-2 cursor-pointer hover:bg-[#004080] transition"
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
