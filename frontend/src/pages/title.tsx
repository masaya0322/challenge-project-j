import * as React from "react";
import { TitleButton } from "@/components/TitleButton";

export default function TitlePage() {
  const [selected, setSelected] = React.useState("start");

  return (
    <main
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        backgroundColor: "#0f172a",
        color: "white",
        gap: "24px",
      }}
    >
      <h1 style={{ fontSize: "2rem", fontWeight: "bold" }}>タイトル画面</h1>

      <div style={{ display: "flex", gap: "16px" }}>
        <TitleButton
          value="start"
          currentValue={selected}
          onChange={setSelected}
          label="はじめる"
        />
        <TitleButton
          value="continue"
          currentValue={selected}
          onChange={setSelected}
          label="つづきから"
        />
      </div>

      <p>選択中: {selected}</p>
    </main>
  );
}
