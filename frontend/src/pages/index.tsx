import { TitleScreen } from "@/components/screens/TitleScreen";
import { ModeSelectScreen } from "@/components/screens/ModeSelectScreen";
import { TimerSettingScreen } from "@/components/screens/TimerSettingScreen";
import { TimerRunningScreen } from "@/components/screens/TimerRunningScreen";
import { StageScreen } from "@/components/screens/StageScreen";
import { ResultScreen } from "@/components/screens/ResultScreen";
import { ScreenType } from "@/types/game";
import { useState } from "react";

const GamePage = () => {
  const [currentScreen, setCurrentScreen] = useState<ScreenType>('timer-setting');

  switch (currentScreen) {
    case "title":
      // タイトル画面
      return <TitleScreen onStart={() => setCurrentScreen('mode-select')}/>

    case "mode-select":
      // モード選択画面
      return (
        <ModeSelectScreen />
      );
    case "timer-setting":
      // タイマー設定画面
      return (
        <TimerSettingScreen onTop={() => setCurrentScreen('title')} onStart={() => setCurrentScreen('timer-running')}/>
      );

    case "timer-running":
      // タイマー進行中画面
      return (
        <TimerRunningScreen />
      );

    case "stage":
      // ゲームステージ画面
      return (
        <StageScreen />
      );

    case "result":
      // 結果画面
      return <ResultScreen />;

    default:
      return null;
  }
}

export default GamePage;
