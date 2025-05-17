import React from "react";

export interface NavbarProps {
  title: string;
}

export const Navbar: React.FC<NavbarProps> = ({ title }) => (
  <nav className="bg-gray-800 text-white px-4 py-3">
    <span className="font-semibold">{title}</span>
  </nav>
);
