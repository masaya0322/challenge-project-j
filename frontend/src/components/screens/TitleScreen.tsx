import { Button } from "@/components/button";

type TitleScreenProps = {
  onStart: () => void;
};

export function TitleScreen({ onStart }: TitleScreenProps) {
  const TITLE_IMAGE_URL = "/images/title.jpg";

  return (
    <div
      className="min-h-screen bg-cover bg-center"
      style={{ backgroundImage: `url(${TITLE_IMAGE_URL})` }}
    >
      <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-black/30">
        <h1 className="text-6xl font-extrabold text-white mb-8 tracking-tight sm:text-7xl drop-shadow-lg">
          お片付けチャレンジ
        </h1>
        <p className="text-xl text-white mb-12 max-w-lg text-center drop-shadow-md">
          おもちゃを片付けてスコアを競おう！
        </p>
        <Button label="START" onClick={onStart} />
      </div>
    </div>
  );
}
