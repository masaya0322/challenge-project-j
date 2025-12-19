import { Button } from "@/components/button";
import { Layout } from "@/components/layout";
import { Logo } from "@/components/logo";

type TitleScreenProps = {
  onStart: () => void
}

export const TitleScreen = ({ onStart }: TitleScreenProps) => {
  const TITLE_IMAGE_URL = "/images/title.jpg";

  return (
    <Layout backgroundImageUrl={TITLE_IMAGE_URL}>
      <div className="flex flex-col items-center min-h-screen p-4 md:p-5 lg:p-6">
        <div className="mt-16 md:mt-24 lg:mt-32 mb-auto">
          <Logo />
        </div>
        <div className="mb-8 md:mb-12 lg:mb-16">
          <Button label="START" onClick={onStart} />
        </div>
      </div>
    </Layout>
  );
}
