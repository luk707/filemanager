"use client";

import * as React from "react";
import {
  Box,
  FileArchive,
  FileUp,
  FolderPlus,
  FolderUp,
  Home,
  Plus,
  PoundSterling,
  Search,
  Shapes,
  Sparkles,
  User,
} from "lucide-react";

import { NavMain } from "~/components/nav-main";
import { WorkspaceSwitcher } from "~/components/workspace-switcher";
import { Sidebar, SidebarHeader, SidebarRail } from "~/components/ui/sidebar";
import { Button } from "~/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu";
import { useFileUpload } from "~/hooks/use-file-upload";

// This is sample data.
const data = {
  workspaces: [
    {
      name: "Luke's Workspace",
      logo: User,
      plan: "Enterprise",
    },
    {
      name: "Dan's Workspace",
      logo: User,
      plan: "Startup",
    },
    {
      name: "Finances",
      logo: PoundSterling,
      plan: "Free",
    },
    {
      name: "3D Modelling",
      logo: Box,
      plan: "Free",
    },
  ],
  navMain: [
    {
      title: "Search",
      url: "#",
      icon: Search,
    },
    {
      title: "Home",
      url: "#",
      icon: Home,
      isActive: true,
    },
    {
      title: "Ask AI",
      url: "#",
      icon: Sparkles,
    },
    {
      title: "Workspaces",
      url: "#",
      icon: Shapes,
    },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { handleFileUpload } = useFileUpload("files");

  return (
    <Sidebar className="border-r-0" {...props}>
      <SidebarHeader>
        <WorkspaceSwitcher workspaces={data.workspaces} />
        <div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="lg">
                <Plus /> New
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-56">
              <DropdownMenuGroup>
                <DropdownMenuItem>
                  <FolderPlus />
                  New folder
                  <DropdownMenuShortcut>⌃C+F</DropdownMenuShortcut>
                </DropdownMenuItem>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem onClick={handleFileUpload}>
                  <FileUp />
                  File upload
                  <DropdownMenuShortcut>⌃C+U</DropdownMenuShortcut>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <FolderUp />
                  Folder upload
                  <DropdownMenuShortcut>⌃C+I</DropdownMenuShortcut>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <FileArchive />
                  Archive upload
                  <DropdownMenuShortcut>⌃C+W</DropdownMenuShortcut>
                </DropdownMenuItem>
              </DropdownMenuGroup>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <NavMain items={data.navMain} />
      </SidebarHeader>
      <SidebarRail />
    </Sidebar>
  );
}
