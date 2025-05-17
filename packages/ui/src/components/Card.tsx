import React from "react";

export interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className = "" }) => (
  <div className={`p-4 rounded shadow bg-white ${className}`.trim()}>
    {children}
  </div>
);
