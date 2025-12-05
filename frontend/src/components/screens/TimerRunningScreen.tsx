import { Layout } from "@/components/Layout";

export const TimerRunningScreen = () => {
  return (
    <Layout >
      <div className="flex flex-col items-center justify-center min-h-screen p-6">
        <h1 className="text-6xl font-extrabold text-blue-600 mb-4 tracking-tight sm:text-7xl">
          お片付け前の準備中画面です。
        </h1>
        <p className="text-xl text-gray-700 mb-8 max-w-lg text-center">
          Tailwind CSS
          が有効化されています。ここからあなたの素晴らしい開発を始めましょう。
        </p>
        <footer className="mt-12 text-sm text-gray-400">
          Next.js + pnpm + Tailwind
        </footer>
      </div>
    </Layout>
  );
}
