import { useState } from "react";
import { ScreenType, GameState } from "@/types/game";
import { TitleScreen } from "@/components/screens/TitleScreen";
import { ModeSelectScreen } from "@/components/screens/ModeSelectScreen";
import { TimerSettingScreen } from "@/components/screens/TimerSettingScreen";
import { TimerRunningScreen } from "@/components/screens/TimerRunningScreen";
import { StageScreen } from "@/components/screens/StageScreen";
import { ResultScreen } from "@/components/screens/ResultScreen";

function GamePage() {
  const [currentScreen, setCurrentScreen] = useState<ScreenType>("title");
  const [gameState, setGameState] = useState<GameState>({
    score: 0,
    toysCollected: 0,
    currentStage: 1,
    timerSettings: { hours: 0, minutes: 0, seconds: 0 },
  });

  const resetGame = () => {
    setGameState({
      score: 0,
      toysCollected: 0,
      currentStage: 1,
      timerSettings: { hours: 0, minutes: 0, seconds: 0 },
    });
    setCurrentScreen("title");
  };

  const handleStageComplete = () => {
    if (gameState.currentStage < 3) {
      setGameState({ ...gameState, currentStage: gameState.currentStage + 1 });
    } else {
      setCurrentScreen("result");
    }
  };

  switch (currentScreen) {
    case "title":
      return <TitleScreen onStart={() => setCurrentScreen("mode-select")} />;

    case "mode-select":
      return (
        <ModeSelectScreen
          onCleanNow={() => setCurrentScreen("stage")}
          onSetTime={() => setCurrentScreen("timer-setting")}
        />
      );

    case "timer-setting":
      return (
        <TimerSettingScreen
          timerSettings={gameState.timerSettings}
          onTimerUpdate={(settings) =>
            setGameState({ ...gameState, timerSettings: settings })
          }
          onStart={() => setCurrentScreen("timer-running")}
          onBack={() => setCurrentScreen("mode-select")}
        />
      );

    case "timer-running":
      return (
        <TimerRunningScreen
          timerSettings={gameState.timerSettings}
          onComplete={() => setCurrentScreen("stage")}
        />
      );

    case "stage":
      return (
        <StageScreen
          gameState={gameState}
          onScoreUpdate={(newScore) =>
            setGameState({ ...gameState, score: newScore })
          }
          onToysUpdate={(newToys) =>
            setGameState({ ...gameState, toysCollected: newToys })
          }
          onStageComplete={handleStageComplete}
        />
      );

    case "result":
      return <ResultScreen gameState={gameState} onRestart={resetGame} />;

    default:
      return null;
  }
}

export default GamePage;
