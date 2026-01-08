import { TitleScreen } from "@/components/screens/TitleScreen";
import { ModeSelectScreen } from "@/components/screens/ModeSelectScreen";
import { TimerSettingScreen } from "@/components/screens/TimerSettingScreen";
import { TimerRunningScreen } from "@/components/screens/TimerRunningScreen";
import { StageScreen } from "@/components/screens/StageScreen";
import { ResultScreen } from "@/components/screens/ResultScreen";
import { ScreenType, GameState, GameProgress } from "@/types/game";
import { useState, useEffect } from "react";
import { useGameProgress } from "@/hooks/useGameProgress";
import { useGameState } from "@/hooks/useGameState";
import { isGameFinished } from "@/lib/game/score";
import type { GetServerSideProps } from "next";
import { getGameProgress } from "@/lib/api/game";

type GamePageProps = {
  initialGameProgress: GameProgress;
};

export const getServerSideProps: GetServerSideProps<GamePageProps> = async () => {
  try {
    const progress = await getGameProgress();

    return {
      props: {
        initialGameProgress: progress,
      },
    };
  } catch (error) {
    console.error("Failed to fetch initial game progress:", error);

    // エラー時のデフォルト値
    return {
      props: {
        initialGameProgress: {
          total_toys: 0,
          cleaned_toys: 0,
        },
      },
    };
  }
};

const GamePage = ({ initialGameProgress }: GamePageProps) => {
  const [currentScreen, setCurrentScreen] = useState<ScreenType>("title");
  const [time, setTime] = useState({ seconds: 0 });
  const [finalGameState, setFinalGameState] = useState<GameState | null>(null);

  // StageScreen表示中のみポーリング
  const { progress } = useGameProgress(
    currentScreen === "stage",
    initialGameProgress
  );
  const gameState = useGameState(progress);

  // ゲーム終了判定
  useEffect(() => {
    if (currentScreen === "stage" && gameState) {
      const { totalToys, cleanedToys } = gameState;
  
      // おもちゃが9個以上になったか、または全クリア判定（isGameFinished）でリザルトへ
      if (cleanedToys >= 9 || isGameFinished(totalToys, cleanedToys)) {
        // 最終的なスコアをセット
        setFinalGameState(gameState);
        // リザルト画面へ遷移
        setCurrentScreen("result");
      }
    }
  }, [gameState, currentScreen]);

  switch (currentScreen) {
    case "title":
      // タイトル画面
      return <TitleScreen onStart={() => setCurrentScreen('mode-select')}/>

    case "mode-select":
      // モード選択画面
      return (
        <ModeSelectScreen onPlayNowButtonClick={() => setCurrentScreen('stage')} onTimerSettingButtonClick={() => setCurrentScreen('timer-setting')}/>
      );
    case "timer-setting":
      // タイマー設定画面
      return (
        <TimerSettingScreen
          onTop={() => setCurrentScreen('title')}
          onStart={() => setCurrentScreen('timer-running')}
          time={time}
          setTime={setTime}
        />
      );

    case "timer-running":
      // タイマー進行中画面
      return (
        <TimerRunningScreen
          time={time}
          setTime={setTime}
          onComplete={() => setCurrentScreen('stage')}
        />
      );

      case "stage":
        return (
          <StageScreen
            gameState={gameState} // ここで渡す
            onComplete={() => {
              setFinalGameState(gameState);
              setCurrentScreen("result");
            }}
          />
        );

    case "result":
      // 結果画面
      return (
        <ResultScreen
          gameState={finalGameState || undefined}
          onBackToTitle={() => {
            setCurrentScreen("title");
            setFinalGameState(null);
          }}
        />
      );

    default:
      return null;
  }
}

export default GamePage;
