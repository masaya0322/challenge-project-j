import { Button } from "@/components/button";

type ModeSelectScreenProps = {
  onCleanNow: () => void;
  onSetTime: () => void;
};

export function ModeSelectScreen({
  onCleanNow,
  onSetTime,
}: ModeSelectScreenProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-blue-400 to-blue-600">
      <h1 className="text-5xl font-bold text-white mb-12 drop-shadow-lg">
        モードを選択してね
      </h1>
      <div className="flex flex-col gap-6 w-full max-w-md">
        <div className="bg-white rounded-lg p-8 shadow-xl">
          <h2 className="text-2xl font-bold text-blue-600 mb-3">CLEAN NOW</h2>
          <p className="text-gray-600 mb-4">すぐに片付けを始めよう！</p>
          <Button label="すぐに開始" onClick={onCleanNow} />
        </div>
        <div className="bg-white rounded-lg p-8 shadow-xl">
          <h2 className="text-2xl font-bold text-green-600 mb-3">SET TIME</h2>
          <p className="text-gray-600 mb-4">
            準備時間を設定してから始めよう！
          </p>
          <Button label="時間設定" onClick={onSetTime} />
        </div>
      </div>
    </div>
  );
}
