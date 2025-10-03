import TitleLogo from "../src/components/TitleLogo";

export default function Home() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "16px",
      }}
    >
      <TitleLogo />
    </main>
  );
}

