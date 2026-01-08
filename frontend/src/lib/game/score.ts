export const STAGE_POINTS = {
  1: 500,
  2: 1000,
  3: 1500,
  4: 2000, // ボーナスステージ
} as const;

export const calculateStage = (cleanedToys: number): number => {
  if (cleanedToys < 3) return 1;
  if (cleanedToys < 6) return 2;
  if (cleanedToys < 9) return 3;
  return 4; // ボーナスステージ
};

export const calculateScore = (cleanedToys: number): number => {
  let score = 0;

  for (let i = 0; i < cleanedToys; i++) {
    const stage = calculateStage(i);
    score += STAGE_POINTS[stage as keyof typeof STAGE_POINTS];
  }

  return score;
};

export const isGameFinished = (totalToys: number, cleanedToys: number): boolean => {
  return totalToys > 0 && cleanedToys >= totalToys;
};
