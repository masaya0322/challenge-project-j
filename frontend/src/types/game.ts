export type ScreenType =
  | "title"
  | "mode-select"
  | "timer-setting"
  | "timer-running"
  | "stage"
  | "result";

export type GameProgress = {
  total_toys: number;
  cleaned_toys: number;
};

export type GameState = {
  score: number;
  toysCollected?: number;
};
