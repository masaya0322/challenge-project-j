export type ScreenType =
  | "title"
  | "mode-select"
  | "timer-setting"
  | "timer-running"
  | "stage"
  | "result";

export type GameState = {
  score: number;
  toysCollected?: number;
};
