export type ScreenType =
  | "title"
  | "mode-select"
  | "timer-setting"
  | "timer-running"
  | "stage"
  | "result";

export type TimerSettings = {
  hours: number;
  minutes: number;
  seconds: number;
};

export type GameState = {
  score: number;
  toysCollected: number;
  currentStage: number;
  timerSettings: TimerSettings;
};
