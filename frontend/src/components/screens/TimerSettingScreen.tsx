import { Layout } from "@/components/layout";
import { TimerDisplay } from "@/components/timer/timer-display";
import { Button } from "@/components/button";
import { useCallback, useMemo} from "react";

type TimerSettingProps = {
  onTop: () => void;
  onStart: () => void;
  time: { seconds: number };
  setTime: (time: { seconds: number }) => void;
}

export const TimerSettingScreen = ({onStart, onTop, time, setTime} : TimerSettingProps) => {
  const updateTime = useCallback((deltaSeconds: number) => {
    const currentTotalSeconds = time.seconds;
    let newTotalSeconds = currentTotalSeconds + deltaSeconds;
    if (newTotalSeconds < 0) {
      newTotalSeconds = 0;
    }
    setTime({seconds: newTotalSeconds});
  }, [time, setTime]);
  const incrementSecond = (seconds :number) => updateTime(seconds);
  const incrementMinute = (minutes :number) => updateTime(minutes * 60);
  const incrementHour = (hours :number) => updateTime(hours * 3600);
  const decrementSecond = (seconds :number) => updateTime(-seconds);
  const decrementMinute = (minutes :number) => updateTime(-minutes * 60);
  const decrementHour = (hours :number) => updateTime(-hours * 3600);
  const handleReset = useCallback(() => {
    setTime({ seconds: 0 });
  }, [setTime]);

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
        <h1 className="text-6xl font-extrabold text-blue-600 mb-4 tracking-tight sm:text-7xl">
          タイマー設定画面です。
        </h1>
        <div className="space-x-8 m-4">
          <Button label="+1h" onClick={() => incrementHour(1)}/>
          <Button label="+10m" onClick={() => incrementMinute(10)}/>
          <Button label="+1m" onClick={() => incrementMinute(1)}/>
          <Button label="+10s" onClick={() => incrementSecond(10)}/>
        </div>
        <TimerDisplay hour={displayHours} minute={displayMinutes} second={displaySeconds}/>
        <div className="space-x-8 m-4">
          <Button label="-1h" onClick={() => decrementHour(1)}/>
          <Button label="-10m" onClick={() => decrementMinute(10)}/>
          <Button label="-1m" onClick={() => decrementMinute(1)}/>
          <Button label="-10s" onClick={() => decrementSecond(10)}/>
        </div>
        <div className="space-x-8 m-4">
          <Button label="RESET" onClick={handleReset}/>
          <Button label="START" onClick={onStart} disabled={time.seconds === 0}/>
          <Button label="TOP" onClick={onTop}/>
        </div>
        <p className="text-xl text-gray-700 mb-8 max-w-lg text-center">
          Tailwind CSS
          が有効化されています。ここからあなたの素晴らしい開発を始めましょう。
        </p>
        <footer className="mt-12 text-sm text-gray-400">
          Next.js + pnpm + Tailwind
        </footer>
      </div>
    </Layout>
  );
}
