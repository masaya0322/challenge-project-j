import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

// クラス名をつなげる小さいユーティリティ
function cn(...classes: (string | undefined)[]) {
  return classes.filter(Boolean).join(" ")
}

// ボタンの見た目バリエーション定義
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-2xl text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none h-10 px-4 py-2 shadow-md",
  {
    variants: {
        variant: {
          primary: "bg-black text-white hover:opacity-90",
          outline:
            "border border-black bg-transparent text-black hover:bg-black hover:text-white",
        },
        size: {
          default: "h-10 px-4 py-2 text-base",
          lg: "h-12 px-6 py-3 text-lg",
          sm: "h-8 px-3 py-1 text-sm",
        },
    },
    defaultVariants: {
        variant: "primary",
        size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"

    return (
      <Comp
        className={cn(buttonVariants({ variant, size }), className)}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
