import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

export const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent-weak)] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-60",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-soft",
        outline: "border border-border bg-transparent text-foreground",
        ghost: "bg-transparent text-foreground",
        destructive: "bg-destructive text-destructive-foreground",
        gradient: "bg-gradient-to-br from-blue-500 to-blue-700 text-white border-none shadow-soft hover:from-blue-600 hover:to-blue-800 active:from-blue-700 active:to-blue-900",
        dangerGradient: "bg-gradient-to-br from-red-500 to-red-600 text-white border-none shadow-soft hover:from-red-600 hover:to-red-700 active:from-red-700 active:to-red-800",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-6",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export type ButtonVariants = VariantProps<typeof buttonVariants>;

export function resolveButtonClass(variant?: ButtonVariants["variant"], size?: ButtonVariants["size"], className?: string) {
  return cn(buttonVariants({ variant, size }), className);
}
