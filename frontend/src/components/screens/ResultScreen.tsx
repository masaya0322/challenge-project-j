import { Layout } from "@/components/layout";
import { Button } from "@/components/button";
import { pixelFont } from "@/utils/fonts";

export const ResultScreen = () => {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen" style={{ backgroundColor: "#3E5F8A" }}>
        <h1
          className={`${pixelFont.className} text-6xl md:text-7xl lg:text-8xl font-bold text-white tracking-wider m-4`}
        >
          RESULT
        </h1>
        <div className="mt-auto mb-16 md:mb-24">
          <Button label="TOP" onClick={() => {}} />
        </div>
      </div>
    </Layout>
  );
}
