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
  Settings2,
  Shapes,
  Sparkles,
  Star,
  User,
  Users,
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
import { matchPath, useLocation } from "react-router";

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
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { handleFileUpload } = useFileUpload("files");
  const location = useLocation();

  return (
    <Sidebar
      collapsible="icon"
      variant="inset"
      className="border-r-0"
      {...props}
    >
      <SidebarHeader>
        <WorkspaceSwitcher workspaces={data.workspaces} />
        <div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="lg">
                <Plus /> New
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-64">
              <DropdownMenuGroup>
                <DropdownMenuItem>
                  <FolderPlus />
                  New folder
                  <DropdownMenuShortcut>
                    ⌃C <span className="tracking-normal">then</span> F
                  </DropdownMenuShortcut>
                </DropdownMenuItem>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem onClick={handleFileUpload}>
                  <FileUp />
                  File upload
                  <DropdownMenuShortcut>
                    ⌃C <span className="tracking-normal">then</span> U
                  </DropdownMenuShortcut>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <FolderUp />
                  Folder upload
                  <DropdownMenuShortcut>
                    ⌃C <span className="tracking-normal">then</span> I
                  </DropdownMenuShortcut>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <FileArchive />
                  Archive upload
                  <DropdownMenuShortcut>
                    ⌃C <span className="tracking-normal">then</span> W
                  </DropdownMenuShortcut>
                </DropdownMenuItem>
              </DropdownMenuGroup>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <NavMain
          items={[
            {
              title: "Search",
              url: "#",
              icon: Search,
              shortcut: "⌘K",
            },
            {
              title: "Home",
              url: "/files",
              icon: Home,
              isActive: !!matchPath("/files/*", location.pathname),
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
            {
              title: "Favorites",
              url: "#",
              icon: Star,
            },
            {
              title: "Preferences",
              url: "/preferences",
              icon: Settings2,
              isActive: !!matchPath("/preferences", location.pathname),
            },
            {
              title: "User Management",
              url: "/user-management",
              icon: Users,
              isActive: !!matchPath("/users", location.pathname),
            },
          ]}
        />
      </SidebarHeader>
    </Sidebar>
  );
}
