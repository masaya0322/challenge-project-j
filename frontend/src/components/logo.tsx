import Image from "next/image";

export const Logo = () => {
  return (
    <div className="relative w-screen h-60 md:h-80 lg:h-100">
      <Image
        src="/logo.png"
        alt="お片付けレンジャー ロゴ"
        fill
        className="object-contain"
      />
    </div>
  );
}
