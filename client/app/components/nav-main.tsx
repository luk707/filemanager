"use client";

import { type LucideIcon } from "lucide-react";
import { Link } from "react-router";

import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "~/components/ui/sidebar";

export function NavMain({
  items,
}: {
  items: (
    | {
        title: string;
        url: string;
        icon: LucideIcon;
        isActive?: boolean;
        shortcut?: string;
      }
    | null
    | false
  )[];
}) {
  return (
    <SidebarMenu>
      {items
        .filter((item) => !!item)
        .map((item) => (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton asChild isActive={item.isActive}>
              <Link to={item.url} className="cursor-default">
                <item.icon />
                <span className="shrink-0">{item.title}</span>
                {item.shortcut && (
                  <span className="text-muted-foreground text-xs ml-auto tracking-widest">
                    {item.shortcut}
                  </span>
                )}
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
    </SidebarMenu>
  );
}
