import React from "react";
import Link from "next/link";

export interface NavItem {
  href: string;
  label: string;
}

export interface NavbarProps {
  items: NavItem[];
  className?: string;
}

export const Navbar: React.FC<NavbarProps> = ({ items, className = "" }) => (
  <nav className={`bg-gray-800 text-white p-4 ${className}`.trim()}>
    <ul className="flex space-x-4">
      {items.map((item) => (
        <li key={item.href}>
          <Link href={item.href}>{item.label}</Link>
        </li>
      ))}
    </ul>
  </nav>
);
