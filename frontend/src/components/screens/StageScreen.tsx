"use client";

import { Layout } from "@/components/layout";
import { StageMessage } from "@/components/stage/stage-message";
import { StageTitle } from "@/components/stage/stage-title";
import { useState, useEffect, useMemo } from "react";
import Image from "next/image";
import { GameState } from "@/types/game"; // 型定義をインポート

const STAGE_TITLE_DISPLAY_TIME = 2000;

// ステージごとのデータ定義
const STAGES = [
  {
    id: 1,
    name: "Stage 1",
    message: "おもちゃをかたづけてスライムをたおせ！",
    backgroundImageURL: "/stage_background/stage1_bg.png",
    characterURL: "/charactor/slime.png",
    animation: "animate-squishy",
    requiredToys: 0, // 0個以上で表示
  },
  {
    id: 2,
    name: "Stage 2",
    message: "おもちゃをかたづけてドラゴンをたおせ！",
    backgroundImageURL: "/stage_background/stage2_bg.png",
    characterURL: "/charactor/doragon.png",
    animation: "animate-float",
    requiredToys: 2, // 2個以上で表示
  },
  {
    id: 3,
    name: "Bonus Stage",
    message: "たからばこをあけろ！",
    backgroundImageURL: "/stage_background/stage3_bg.png",
    characterURL: "/charactor/treasure_chest.png",
    animation: "animate-sparkle",
    requiredToys: 4, // 4個以上で表示
  },
];

type StageScreenProps = {
  gameState: GameState | null; // 親から現在のスコアをもらう
  onComplete?: () => void;
};

export const StageScreen = ({ gameState, onComplete }: StageScreenProps) => {
  const [showTitle, setShowTitle] = useState(true);
  
  // 現在のスコア（おもちゃの数）
  const cleanedCount = gameState?.cleanedToys || 0;

  // 現在のスコアに最適なステージを計算
  const currentStageIndex = useMemo(() => {
    // 条件に合う（requiredToysを満たす）最大のインデックスを探す
    const index = STAGES.findLastIndex(s => cleanedCount >= s.requiredToys);
    return index !== -1 ? index : 0;
  }, [cleanedCount]);

  const currentStage = STAGES[currentStageIndex];

  // ステージが変わるたびにタイトルを表示する
  useEffect(() => {
    setShowTitle(true);
    const timer = setTimeout(() => {
      setShowTitle(false);
    }, STAGE_TITLE_DISPLAY_TIME);

    return () => clearTimeout(timer);
  }, [currentStageIndex]);

  // 全てのおもちゃが片付いたら完了（親に通知）
  // ※ GamePage側のuseEffectでも判定していますが、ここでもケアしておくと安全です。

  if (showTitle) {
    return (
      <Layout>
        <StageTitle stageName={currentStage.name} />
      </Layout>
    );
  }

  return (
    <Layout backgroundImageUrl={currentStage.backgroundImageURL}>
      <div className="flex flex-col items-center justify-between min-h-screen w-screen h-screen p-6 animate-fade-in">
        {/* スコア表示（デバッグ用・または演出用） */}
        <div className="absolute top-4 right-4 bg-white/80 p-2 rounded-lg font-bold">
          おもちゃ: {cleanedCount} / {gameState?.totalToys}
        </div>

        <div className="flex-1 flex items-center justify-center w-full max-w-4xl">
          <div className={`relative w-full h-full ${currentStage.animation}`}>
            <Image
              src={currentStage.characterURL}
              alt={currentStage.name}
              fill
              className="object-contain"
              priority
              unoptimized
            />
          </div>
        </div>
        
        <div className="w-full mb-16">
          <StageMessage message={currentStage.message} />
        </div>
      </div>
    </Layout>
  );
};
