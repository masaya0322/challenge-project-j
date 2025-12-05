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
    <div className="relative inline-block">
      <p
        className={`
          ${pixelFont.className}
          relative z-10
          p-8
          text-white
          text-6xl
          tracking-[0.25em]
          border-2
          border-white
          transition
          active:translate-y-[2px]
        `}
        style={{ backgroundColor: "#002A4C" }}
      >
        {`${time.hour}:${time.minute}:${time.second}`}
      </p>
      <div className="absolute -bottom-1 left-0 right-0 h-4 bg-white rounded-b" />
    </div>
  );
}
