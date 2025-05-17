import React from "react";

export interface ButtonProps {
  children: React.ReactNode;
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({ children, className = "" }) => {
  return (
    <button
      className={`px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 ${className}`.trim()}
    >
      {children}
    </button>
  );
};
