import Image from "next/image";

export default function TitleLogo() {
  return (
    <div
      style={{
        width: "100%",
        height: "100vh", // 画面の高さに合わせる
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Image
        src="/23400496.jpg"
        alt="お片付けレンジャーのロゴ"
        fill // 親divいっぱいに広げる
        style={{
          objectFit: "fill", // ← 縦横比を無視して完全フィット
        }}
        priority
      />
    </div>
  );
}
