"use client";

import { Button } from "@/components/ui/button";

export function ModeSelect() {
  return (
    <div className="flex flex-col items-center py-12 gap-6">
      <Button onClick={() => {}}>START</Button>
      <div className="flex gap-12 justify-center items-center">
        <Button onClick={() => {}}>CLEAN NOW</Button>
        <Button onClick={() => {}}>SET TIME</Button>
      </div>
    </div>
  );
}
