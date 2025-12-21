import { Layout } from "@/components/layout";
import { Button } from "@/components/button";
import { pixelFont } from "@/utils/fonts";
import { GameState } from "@/types/game";

type ResultScreenProps = {
  gameState?: GameState;
  onBackToTitle: () => void;
};

export const ResultScreen = ({ gameState, onBackToTitle }: ResultScreenProps) => {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen" style={{ backgroundColor: "#3E5F8A" }}>
        <h1
          className={`${pixelFont.className} text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-8 md:mb-12 tracking-wider`}
        >
          RESULT
        </h1>

        {gameState && (
          <div className="mb-12 md:mb-16">
            <p
              className={`${pixelFont.className} text-5xl md:text-6xl lg:text-7xl font-bold text-white text-center`}
            >
              SCORE: {gameState.score}
            </p>
          </div>
        )}

        <div className="mt-auto mb-16 md:mb-24">
          <Button label="TOP" onClick={onBackToTitle} />
        </div>
      </div>
    </Layout>
  );
}
