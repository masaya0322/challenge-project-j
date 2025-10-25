// frontend/app/page.tsx

export default function Home() {
  return (
    // 全体を画面いっぱいに広げ、中央揃えにするためのクラス
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
      
      {/* メインの見出し */}
      <h1 className="text-6xl font-extrabold text-blue-600 mb-4 tracking-tight sm:text-7xl">
        Hello Next.js World!
      </h1>
      
      {/* サブテキスト */}
      <p className="text-xl text-gray-700 mb-8 max-w-lg text-center">
        Tailwind CSS が有効化されています。ここからあなたの素晴らしい開発を始めましょう。
      </p>
      
      {/* ボタン（動作確認用） */}
      <button className="px-6 py-3 bg-indigo-500 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition duration-300 transform hover:scale-105">
        開発スタート！
      </button>
      
      {/* バージョン情報 */}
      <footer className="mt-12 text-sm text-gray-400">
        Next.js + pnpm + Tailwind
      </footer>
    </div>
  );
}