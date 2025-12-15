"use client";

import { Button as ShadcnButton } from "./ui/button";
import { Press_Start_2P } from "next/font/google";

const pixelFont = Press_Start_2P({
  subsets: ["latin"],
  weight: "400",
});

type Button = {
  label: string;
  onClick: () => void;
  disabled?: boolean;
};

export function Button({ label, onClick, disabled = false }: Button) {
  return (
    <div className="relative inline-block">
      <ShadcnButton
        onClick={onClick}
        disabled={disabled}
        variant="default"
        className={`
          ${pixelFont.className}
          relative z-10
          p-8
          text-white
          text-xl
          tracking-[0.25em]
          border-2
          border-white
          cursor-pointer
          transition
          active:translate-y-[2px]
          ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
        `}
        style={{ backgroundColor: "#1F8BFF" }}
      >
        {label.toUpperCase()}
      </ShadcnButton>
      <div className="absolute -bottom-1 left-0 right-0 h-4 bg-white rounded-b" />
    </div>
  );
}
