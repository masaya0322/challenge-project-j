import TitleButton from "@/components/TitleButton";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
      <h1 className="text-6xl font-extrabold text-blue-600 mb-4 tracking-tight sm:text-7xl">
        Hello Next.js World!
      </h1>

      <p className="text-xl text-gray-700 mb-8 max-w-lg text-center">
        Tailwind CSS が有効化されています。ここからあなたの素晴らしい開発を始めましょう。
      </p>

      <TitleButton
        value="スタート"
        onChange={(v) => {
          console.log("押されたボタン:", v);
        }}
      />

      <footer className="mt-12 text-sm text-gray-400">
        Next.js + pnpm + Tailwind
      </footer>
    </div>
  );
}
