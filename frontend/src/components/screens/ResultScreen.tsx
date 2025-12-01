import { Button } from "@/components/button";
import { GameState } from "@/types/game";

type ResultScreenProps = {
  gameState: GameState;
  onRestart: () => void;
};

export function ResultScreen({ gameState, onRestart }: ResultScreenProps) {
  const getRank = () => {
    if (gameState.score >= 100) return "S";
    if (gameState.score >= 80) return "A";
    if (gameState.score >= 60) return "B";
    if (gameState.score >= 40) return "C";
    return "D";
  };

  const getMessage = () => {
    const rank = getRank();
    switch (rank) {
      case "S":
        return "完璧なお片付け！素晴らしい！";
      case "A":
        return "とても上手にお片付けできたね！";
      case "B":
        return "よくできました！";
      case "C":
        return "もう少し頑張ろう！";
      default:
        return "次はもっと頑張ろう！";
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-indigo-400 to-purple-600">
      <div className="bg-white rounded-lg p-12 shadow-xl text-center max-w-md">
        <h1 className="text-4xl font-bold text-purple-600 mb-6">
          チャレンジ完了！
        </h1>
        <div className="mb-6">
          <p className="text-gray-600 mb-2">ランク</p>
          <p className="text-8xl font-bold text-yellow-500 mb-4">
            {getRank()}
          </p>
          <p className="text-xl text-gray-700 mb-6">{getMessage()}</p>
        </div>
        <div className="space-y-3 mb-8">
          <div className="flex justify-between items-center border-b pb-2">
            <span className="text-gray-600">最終スコア</span>
            <span className="text-2xl font-bold text-purple-600">
              {gameState.score}
            </span>
          </div>
          <div className="flex justify-between items-center border-b pb-2">
            <span className="text-gray-600">片付けたおもちゃ</span>
            <span className="text-2xl font-bold text-pink-600">
              {gameState.toysCollected}
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">到達ステージ</span>
            <span className="text-2xl font-bold text-indigo-600">
              {gameState.currentStage}
            </span>
          </div>
        </div>
        <Button label="もう一度プレイ" onClick={onRestart} />
      </div>
    </div>
  );
}
