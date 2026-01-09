import { useState, useEffect } from "react";
import { getGameProgress } from "@/lib/api/game";
import type { GameProgress } from "@/types/game";

export const useGameProgress = (
  enabled: boolean,
  initialData: GameProgress
) => {
  const [progress, setProgress] = useState<GameProgress>(initialData);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!enabled) return;

    const interval = setInterval(async () => {
      try {
        const data = await getGameProgress();
        setProgress(data);
        setError(null);
      } catch (err) {
        setError(err as Error);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [enabled]);

  return { progress, error };
};
