import { Layout } from "@/components/layout";
import { Button } from "@/components/button";
import { dodGothicFont } from "@/utils/fonts";

type ModeSelectScreenProps = {
  onPlayNowButtonClick: () => void;
  onTimerSettingButtonClick: () => void;
}

export const ModeSelectScreen = ( {onPlayNowButtonClick,onTimerSettingButtonClick} : ModeSelectScreenProps) => {
  const TITLE_IMAGE_URL = "/images/title.jpg";
  return (
    <Layout backgroundImageUrl={TITLE_IMAGE_URL}>
      <div className="flex flex-col items-center justify-center min-h-screen gap-16 p-6">
        <h1 className={`${dodGothicFont.className} text-6xl font-extrabold tracking-tight sm:text-7xl`}>
          モードを選んでね！
        </h1>
        <div className="flex gap-16">
          <Button label="PLAY NOW" onClick={onPlayNowButtonClick} />
          <Button label="TIMER SETTING" onClick={onTimerSettingButtonClick} />
        </div>
      </div>
    </Layout>
  );
}
