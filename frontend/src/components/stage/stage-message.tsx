"use client";

import { dodGothicFont } from "@/utils/fonts";

type StageMessageProps = {
  message: string;
};

export const StageMessage = ({ message }: StageMessageProps) => {
  return (
    <div className="w-full max-w-4xl mx-auto px-8">
      <div className="bg-black border-4 border-white p-6 rounded-lg shadow-lg">
        <p className={`${dodGothicFont.className} text-white text-center text-bold sm:text-2xl md:text-3xl lg:text-4xl leading-relaxed`}>
          {message}
        </p>
      </div>
    </div>
  );
}
