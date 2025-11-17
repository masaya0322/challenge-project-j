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
};

export function Button({ label, onClick }: Button) {
   return (
    <div className="relative inline-block">
      <ShadcnButton
        onClick={onClick}
        variant="default"
        className={`
          ${pixelFont.className}
          relative z-10
          h-16
          px-16
          rounded-xl
          text-white
          text-xl
          tracking-[0.25em]
          border-2
          border-white
          cursor-pointer
          transition
          active:translate-y-[2px]
        `}
        style={{ backgroundColor: "#1F8BFF" }}
      >
        {label.toUpperCase()}
      </ShadcnButton>

      <div className="absolute -bottom-2 left-0 right-0 h-4 bg-[#0a5aa0] rounded-b-xl" />
      <div className="absolute -bottom-1 left-4 right-4 h-1 bg-white rounded-full opacity-90 pointer-events-none" />
    </div>
  );
}
