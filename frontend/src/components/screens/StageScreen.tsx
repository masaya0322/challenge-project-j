"use client";

import { Layout } from "@/components/layout";
import { StageMessage } from "@/components/stage/stage-message";
import { StageTitle } from "@/components/stage/stage-title";
import { Button } from "@/components/button";
import { useState, useEffect } from "react";
import Image from "next/image";

const STAGE_TITLE_DISPLAY_TIME = 2000;

type StageData = {
  id: number;
  name: string;
  message: string;
  backgroundImageURL: string;
  characterURL: string;
};

const STAGES: StageData[] = [
  {
    id: 1,
    name: "Stage 1",
    message: "おもちゃをかたづけてスライムをたおせ！",
    backgroundImageURL: "/stage_background/stage1_bg.png",
    characterURL: "/charactor/slime.png",
  },
  {
    id: 2,
    name: "Stage 2",
    message: "おもちゃをかたづけてドラゴンをたおせ！",
    backgroundImageURL: "/stage_background/stage2_bg.png",
    characterURL: "/charactor/doragon.png",
  },
  {
    id: 3,
    name: "Bonus Stage",
    message: "おもちゃをかたづけてたからばこをあけろ！",
    backgroundImageURL: "/stage_background/stage3_bg.png",
    characterURL: "/charactor/treasure_chest.png",
  },
];

const getCharacterAnimation = (stageId: number): string => {
  switch (stageId) {
    case 1:
      return "animate-squishy";
    case 2:
      return "animate-float";
    case 3:
      return "animate-sparkle";
    default:
      return "animate-float";
  }
};

type StageScreenProps = {
  onComplete?: () => void;
};

export const StageScreen = ({ onComplete }: StageScreenProps) => {
  const [currentStageIndex, setCurrentStageIndex] = useState(0);
  const [showTitle, setShowTitle] = useState(true);

  const currentStage = STAGES[currentStageIndex];
  const isLastStage = currentStageIndex === STAGES.length - 1;
  const characterAnimation = getCharacterAnimation(currentStage.id);

  useEffect(() => {
    setShowTitle(true);
    const timer = setTimeout(() => {
      setShowTitle(false);
    }, STAGE_TITLE_DISPLAY_TIME);

    return () => clearTimeout(timer);
  }, [currentStageIndex]);

  const handleNext = () => {
    if (isLastStage) {
      onComplete?.();
    } else {
      setCurrentStageIndex(currentStageIndex + 1);
    }
  };

  if (showTitle) {
    return (
      <Layout>
        <StageTitle stageName={currentStage.name} />
      </Layout>
    );
  }

  return (
    <Layout backgroundImageUrl={currentStage.backgroundImageURL} >
      <div className={`flex flex-col items-center justify-between min-h-screen w-screen h-screen p-6 animate-fade-in`}>
        <div className="flex-1 flex items-center justify-center w-full max-w-4xl">
          <div className={`relative w-full h-full ${characterAnimation}`}>
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
        <div className="w-full mb-8">
          <StageMessage message={currentStage.message} />
        </div>
        <div className="mb-8">
          <Button label="NEXT" onClick={handleNext} />
        </div>
      </div>
    </Layout>
  );
};
