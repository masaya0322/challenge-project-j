"use client";

import { Button } from "@/components/button";
import { Layout } from "@/components/layout";

export function ModeSelect() {
  return (
    <div className="flex flex-col items-center py-12 gap-6">
      <Button label="START" onClick={() => {}} />

      <div className="flex gap-12 justify-center items-center">
        <Button label="CLEAN NOW" onClick={() => {}} />
        <Button label="SET TIME" onClick={() => {}} />
      </div>
    </div>
  );
}
