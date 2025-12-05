import { Button } from "@/components/button";
import { Layout } from "@/components/layout";

export const TitleScreen = () => {
  const TITLE_IMAGE_URL = "/images/title.jpg";
  return (
    <Layout backgroundImageUrl={TITLE_IMAGE_URL}>
      <div className="flex flex-col items-center justify-center min-h-screen p-6">
        <h1 className="text-6xl font-extrabold text-blue-600 mb-4 tracking-tight sm:text-7xl">
          Hello Next.js World!
        </h1>
        <p className="text-xl text-gray-700 mb-8 max-w-lg text-center">
          Tailwind CSS
          が有効化されています。ここからあなたの素晴らしい開発を始めましょう。
        </p>
        <Button label="START" onClick={() => {} } />
        <footer className="mt-12 text-sm text-gray-400">
          Next.js + pnpm + Tailwind
        </footer>
      </div>
    </Layout>
  );
}
