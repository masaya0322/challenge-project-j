import * as React from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type TitleButtonProps<T extends string | number> = {
  value: T;
  currentValue?: T;
  onChange: (value: T) => void;
  label: string;
  disabled?: boolean;
  selected?: boolean;
  className?: string;
};

export function TitleButton<T extends string | number>({
  value,
  currentValue,
  onChange,
  label,
  disabled,
  selected,
  className,
}: TitleButtonProps<T>) {
  const isSelected = selected ?? (currentValue !== undefined && currentValue === value);

  return (
    <Button
      type="button"
      disabled={disabled}
      onClick={() => onChange(value)}
      variant={isSelected ? "default" : "secondary"}
      className={cn(
        "rounded-xl text-lg font-semibold px-6 py-4 transition-all",
        isSelected ? "opacity-100 shadow-lg" : "opacity-80 hover:opacity-100",
        className
      )}
    >
      {label}
    </Button>
  );
}
