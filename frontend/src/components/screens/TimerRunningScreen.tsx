import { TimerSettings } from "@/types/game";
import { useEffect, useState } from "react";

type TimerRunningScreenProps = {
  timerSettings: TimerSettings;
  onComplete: () => void;
};

export function TimerRunningScreen({
  timerSettings,
  onComplete,
}: TimerRunningScreenProps) {
  const [remainingSeconds, setRemainingSeconds] = useState(() => {
    return (
      timerSettings.hours * 3600 +
      timerSettings.minutes * 60 +
      timerSettings.seconds
    );
  });

  useEffect(() => {
    if (remainingSeconds <= 0) {
      onComplete();
      return;
    }

    const timer = setInterval(() => {
      setRemainingSeconds((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [remainingSeconds, onComplete]);

  const hours = Math.floor(remainingSeconds / 3600);
  const minutes = Math.floor((remainingSeconds % 3600) / 60);
  const seconds = remainingSeconds % 60;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-yellow-400 to-orange-500">
      <h1 className="text-4xl font-bold text-white mb-12 drop-shadow-lg">
        準備時間カウントダウン
      </h1>
      <div className="bg-white rounded-lg p-12 shadow-xl">
        <div className="text-center">
          <div className="text-7xl font-bold text-orange-600 mb-4 font-mono">
            {String(hours).padStart(2, "0")}:{String(minutes).padStart(2, "0")}
            :{String(seconds).padStart(2, "0")}
          </div>
          <p className="text-gray-600 text-xl">おもちゃを準備しよう！</p>
        </div>
      </div>
    </div>
  );
}
