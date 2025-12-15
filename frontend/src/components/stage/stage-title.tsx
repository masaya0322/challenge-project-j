"use client";

import { pixelFont } from "@/utils/fonts";

type StageTitleProps = {
  stageName: string;
};

export const StageTitle = ({ stageName }: StageTitleProps) => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-black animate-fade-in">
      <h1 className={`${pixelFont.className} text-6xl text-white animate-pulse`}>
        {stageName}
      </h1>
    </div>
  );
}
