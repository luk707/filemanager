import type { ReactNode } from "react";
import { SidebarTrigger } from "./ui/sidebar";
import { useShell } from "~/layouts/shell";

export interface ToolbarProps {
  left?: ReactNode;
  right?: ReactNode;
  children: ReactNode;
}

export function Toolbar({ left, right, children }: ToolbarProps) {
  const { fixedToTop } = useShell();
  return (
    <header
      data-fixed-to-top={String(fixedToTop)}
      className="flex h-14 shrink-0 items-center gap-2 top-0 sticky bg-background/70 backdrop-blur-lg border-b transition-colors duration-300 data-[fixed-to-top=true]:border-transparent hover:data-[fixed-to-top=true]:border-border"
    >
      <div className="flex flex-1 items-center gap-2 px-3">
        <SidebarTrigger />
        {left}
        {children}
        {right && <div className="flex gap-1">{right}</div>}
      </div>
    </header>
  );
}
