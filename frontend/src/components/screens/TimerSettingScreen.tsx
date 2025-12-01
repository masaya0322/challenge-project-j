import { Button } from "@/components/button";
import { TimerSettings } from "@/types/game";

type TimerSettingScreenProps = {
  timerSettings: TimerSettings;
  onTimerUpdate: (settings: TimerSettings) => void;
  onStart: () => void;
  onBack: () => void;
};

export function TimerSettingScreen({
  timerSettings,
  onTimerUpdate,
  onStart,
  onBack,
}: TimerSettingScreenProps) {
  const handleChange = (field: keyof TimerSettings, value: number) => {
    onTimerUpdate({
      ...timerSettings,
      [field]: value,
    });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-green-400 to-green-600">
      <h1 className="text-4xl font-bold text-white mb-8 drop-shadow-lg">
        準備時間を設定
      </h1>
      <div className="bg-white rounded-lg p-8 shadow-xl w-full max-w-md">
        <div className="space-y-6">
          <div>
            <label className="block text-gray-700 font-semibold mb-2">
              時間
            </label>
            <input
              type="number"
              min="0"
              max="23"
              value={timerSettings.hours}
              onChange={(e) =>
                handleChange("hours", parseInt(e.target.value) || 0)
              }
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-gray-700 font-semibold mb-2">
              分
            </label>
            <input
              type="number"
              min="0"
              max="59"
              value={timerSettings.minutes}
              onChange={(e) =>
                handleChange("minutes", parseInt(e.target.value) || 0)
              }
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-gray-700 font-semibold mb-2">
              秒
            </label>
            <input
              type="number"
              min="0"
              max="59"
              value={timerSettings.seconds}
              onChange={(e) =>
                handleChange("seconds", parseInt(e.target.value) || 0)
              }
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
            />
          </div>
        </div>
        <div className="flex gap-4 mt-8">
          <Button label="戻る" onClick={onBack} />
          <Button label="開始" onClick={onStart} />
        </div>
      </div>
    </div>
  );
}
