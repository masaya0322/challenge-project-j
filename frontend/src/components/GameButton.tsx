// frontend/src/components/GameButton.tsx
"use client";

import React from "react";
import { Button } from "./ui/button";
import { Press_Start_2P } from "next/font/google";

const pixelFont = Press_Start_2P({
  subsets: ["latin"],
  weight: "400",
});

type GameButtonProps = {
  label: string;
  onChange?: (value: string) => void;
  value?: string;
  color?: string;
};

export default function GameButton({
  label,
  onChange,
  value,
  color = "#1F8BFF",
}: GameButtonProps) {
  const handleClick = () => {
    onChange?.(value ?? label);
  };

  return (
    <div className="relative inline-block">
      {/* ボタン本体 */}
      <Button
        onClick={handleClick}
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
        style={{ backgroundColor: color }}
      >
        {label.toUpperCase()}
      </Button>

      {/* 下の青いパーツ（横幅をボタンと同じに、はみ出さない） */}
      <div className="absolute -bottom-2 left-0 right-0 h-4 bg-[#0a5aa0] rounded-b-xl" />

      {/* 中の白いラインもボタンと同じ幅の中におさめる */}
      <div className="absolute -bottom-1 left-4 right-4 h-1 bg-white rounded-full opacity-90 pointer-events-none" />
    </div>
  );
}
