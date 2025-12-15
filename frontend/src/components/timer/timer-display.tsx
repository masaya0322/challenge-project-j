import { Press_Start_2P } from "next/font/google";

const pixelFont = Press_Start_2P({
  subsets: ["latin"],
  weight: "400",
});

type TimerDisplayProps = {
  hour: string;
  minute: string;
  second: string;
};

export const TimerDisplay = ( time :TimerDisplayProps ) => {
  return (
      <div
        className={`
          ${pixelFont.className}
          bg-[#002A4C]
          relative
          inline-block
          p-8
          text-white
          text-6xl
          border-2
          border-white
        `}
      >
          {`${time.hour}:${time.minute}:${time.second}`}
      </div>
  );
}
