import { Button } from "@/components/button";
import { GameState } from "@/types/game";

type StageScreenProps = {
  gameState: GameState;
  onScoreUpdate: (newScore: number) => void;
  onToysUpdate: (newToys: number) => void;
  onStageComplete: () => void;
};

export function StageScreen({
  gameState,
  onScoreUpdate,
  onToysUpdate,
  onStageComplete,
}: StageScreenProps) {
  const handleCollectToy = () => {
    const newToys = gameState.toysCollected + 1;
    const newScore = gameState.score + 10;
    onToysUpdate(newToys);
    onScoreUpdate(newScore);
  };

  const getStageName = () => {
    switch (gameState.currentStage) {
      case 1:
        return "Stage 1";
      case 2:
        return "Stage 2";
      case 3:
        return "Bonus Stage";
      default:
        return "Stage";
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-purple-400 to-pink-500">
      <div className="bg-white rounded-lg p-8 shadow-xl mb-6">
        <h1 className="text-4xl font-bold text-purple-600 mb-4">
          {getStageName()}
        </h1>
        <div className="grid grid-cols-2 gap-4 text-center">
          <div>
            <p className="text-gray-600">スコア</p>
            <p className="text-3xl font-bold text-purple-600">
              {gameState.score}
            </p>
          </div>
          <div>
            <p className="text-gray-600">おもちゃ</p>
            <p className="text-3xl font-bold text-pink-600">
              {gameState.toysCollected}
            </p>
          </div>
        </div>
      </div>
      <div className="flex gap-4">
        <Button label="おもちゃを片付ける" onClick={handleCollectToy} />
        <Button label="ステージクリア" onClick={onStageComplete} />
      </div>
    </div>
  );
}
