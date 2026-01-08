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
  const cleanedCount = gameState?.cleanedToys || 0;

  const currentStageIndex = useMemo(() => {
    const calculatedIndex = Math.floor(cleanedCount / 3);
    return Math.min(calculatedIndex, STAGES.length - 1);
  }, [cleanedCount]);

  const currentStage = STAGES[currentStageIndex];

  // ステージが「実際に切り替わった時」だけタイトルを表示する
  useEffect(() => {
    setShowTitle(true);
    const timer = setTimeout(() => {
      setShowTitle(false);
    }, STAGE_TITLE_DISPLAY_TIME);

    return () => clearTimeout(timer);
  }, [currentStageIndex]); // ここは currentStageIndex の変化を監視

  // 修正ポイント：タイトルとメイン画面を「切り替え」ではなく「重ねる」か「条件分岐を整理」する
  return (
    <Layout backgroundImageUrl={currentStage.backgroundImageURL}>
      {showTitle ? (
        // タイトル表示中
        <StageTitle stageName={currentStage.name} />
      ) : (
        // メインのゲーム画面
        <div className="flex flex-col items-center justify-between min-h-screen w-screen h-screen p-6 animate-fade-in">
          {/* 進捗デバッグ表示 */}
          <div className="absolute top-4 right-4 bg-black/50 text-white p-2 rounded">
            Score: {cleanedCount}
          </div>

          <div className="flex-1 flex items-center justify-center w-full max-w-4xl">
            <div className={`relative w-96 h-96 ${currentStage.animation}`}>
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
      )}
    </Layout>
  );
};
