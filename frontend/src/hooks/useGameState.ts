import { useState, useEffect } from "react";
import { calculateScore, calculateStage } from "@/lib/game/score";
import type { GameProgress, GameState } from "@/types/game";

export const useGameState = (progress: GameProgress | null) => {
  const [gameState, setGameState] = useState<GameState>({
    score: 0,
    currentStage: 1,
    totalToys: 0,
    cleanedToys: 0,
  });

  useEffect(() => {
    if (!progress) return;

    const newScore = calculateScore(progress.cleaned_toys);
    const newStage = calculateStage(progress.cleaned_toys);

    setGameState({
      score: newScore,
      currentStage: newStage,
      totalToys: progress.total_toys,
      cleanedToys: progress.cleaned_toys,
    });
  }, [progress]);

  return gameState;
};
