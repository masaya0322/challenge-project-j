import { Layout } from "@/components/layout";
import { TimerDisplay } from "@/components/timer/timer-display";
import { useMemo, useEffect } from "react";

type TimerRunningProps = {
  time: { seconds: number };
  setTime: (time: { seconds: number }) => void;
  onComplete: () => void;
}

export const TimerRunningScreen = ({ time, setTime, onComplete }: TimerRunningProps) => {
  useEffect(() => {
    if (time.seconds <= 0) {
      return;
    }

    const intervalId = setInterval(() => {
      setTime({ seconds: time.seconds - 1 });

      if (time.seconds - 1 <= 0) {
        clearInterval(intervalId);
        onComplete();
      }
    }, 1000);

    return () => clearInterval(intervalId);
  }, [time.seconds, setTime, onComplete]);

  const { displayHours, displayMinutes, displaySeconds } = useMemo(() => {
    const hours = Math.floor(time.seconds / 3600);
    const remainingAfterHours = time.seconds % 3600;
    const minutes = Math.floor(remainingAfterHours / 60);
    const seconds = remainingAfterHours % 60;

    return {
      displayHours: String(hours).padStart(2, '0'),
      displayMinutes: String(minutes).padStart(2, '0'),
      displaySeconds: String(seconds).padStart(2, '0')
    };
  }, [time.seconds]);

  return (
    <Layout >
      <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-700">
        <h1 className="text-6xl font-extrabold mb-4 tracking-tight sm:text-7xl">
          お片付け前の準備中画面です。
        </h1>
        <TimerDisplay hour={displayHours} minute={displayMinutes} second={displaySeconds}/>
      </div>
    </Layout>
  );
}
