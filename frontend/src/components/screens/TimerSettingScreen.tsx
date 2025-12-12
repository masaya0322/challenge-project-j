import { Layout } from "@/components/layout";
import { TimerDisplay } from "@/components/timer/timer-display";
import { Button } from "@/components/button";

export const TimerSettingScreen = () => {
  return (
    <Layout >
      <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-700">
        <h1 className="text-6xl font-extrabold text-blue-600 mb-4 tracking-tight sm:text-7xl">
          タイマー設定画面です。
        </h1>
        <div className="space-x-8 m-4">
          <Button label="+1h" onClick={() => (null)}/>
          <Button label="+10m" onClick={() => (null)}/>
          <Button label="+1m" onClick={() => (null)}/>
          <Button label="+10s" onClick={() => (null)}/>
        </div>
        <TimerDisplay hour="00" minute="00" second="00"/>
        <div className="space-x-8 m-4">
          <Button label="-1h" onClick={() => (null)}/>
          <Button label="-10m" onClick={() => (null)}/>
          <Button label="-1m" onClick={() => (null)}/>
          <Button label="-10s" onClick={() => (null)}/>
        </div>
        <div className="space-x-8 m-4">
          <Button label="RESET" onClick={() => (null)}/>
          <Button label="START" onClick={() => (null)}/>
          <Button label="TOP" onClick={() => (null)}/>
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
