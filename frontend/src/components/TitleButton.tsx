import React from "react"
import { Button } from "./ui/button"

export type TitleButtonProps = {
  // そのボタンが表す値。ラベルにも使う
  value: string

  // 親に「このボタンが押されたよ」って知らせる
  // 呼び出し側は (newValue) => { ... } の形で渡すイメージ
  onChange?: (value: string) => void
}

export default function TitleButton({ value, onChange }: TitleButtonProps) {
  const handleClick = () => {
    if (onChange) {
      onChange(value)
    }
  }

  return (
    <Button
      variant="default"
      size="lg"
      className="rounded-2xl font-bold tracking-wide"
      onClick={handleClick}
    >
      {value}
    </Button>
  )
}
