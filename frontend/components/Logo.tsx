// frontend/components/Logo.tsx
import Image from "next/image";

export default function Logo() {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center", // 横中央揃え
        alignItems: "center",     // 縦中央揃え
        height: "100vh",          // 画面全体に高さを合わせる
      }}
    >
      <Image
        src="/logo.png" // publicフォルダに配置する画像パス
        alt="お片付けレンジャー ロゴ"
        width={600} // 適宜調整
        height={200}
      />
    </div>
  );
}
