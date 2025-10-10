// frontend/tailwind.config.js (修正案)

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // 1. Next.jsの App Router (もしあれば) - App Routerを使うなら必要
    // './src/app/**/*.{js,ts,jsx,tsx}', 
    
    // 💡 ページファイル (src/pages/ 以下、すべての階層)
    './src/pages/**/*.{js,ts,jsx,tsx}', 
    
    // 💡 コンポーネントファイル (src/components/ 以下、すべての階層)
    './src/components/**/*.{js,ts,jsx,tsx}', 
    
    // 💡 ルートCSSのインポート先 (通常はPages Routerの _app.tsx などでカバーされるため不要ですが、念のため)
    // './src/*.{js,ts,jsx,tsx}', 
    
    // 以下の2行は、Next.js環境では通常不要なので削除
    // './*.html',
    // 'src/styles/*.css', // CSSファイル自体はクラス定義を持たないのでスキャン不要
  ],
  theme: {
    // ... 他の設定
  },
  plugins: [
    // ...
  ],
}