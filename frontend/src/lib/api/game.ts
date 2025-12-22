import type { GameProgress } from "@/types/game";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const getGameProgress = async (): Promise<GameProgress> => {
  const response = await fetch(`${API_BASE_URL}/api/game/progress`);

  if (!response.ok) {
    throw new Error(`Failed to fetch game progress: ${response.statusText}`);
  }

  return response.json();
};
