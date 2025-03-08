import { FileGrid } from "~/components/file-grid";
import { getFiles } from "~/api/files";
import type { Route } from "./+types/file-browser";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "~/components/ui/breadcrumb";
import {
  ChevronLeft,
  ChevronRight,
  Columns3,
  GalleryThumbnails,
  LayoutGrid,
  List,
  User,
} from "lucide-react";
import { cn } from "~/lib/utils";
import { SidebarTrigger } from "~/components/ui/sidebar";
import { useShell } from "~/layouts/shell";
import { Button } from "~/components/ui/button";

export async function loader({}: Route.LoaderArgs) {
  // TODO: Remove hardcoded workspaceId
  return await getFiles("files");
}

export async function clientLoader({}: Route.ClientLoaderArgs) {
  // TODO: Remove hardcoded workspaceId
  return await getFiles("files");
}

export default function FileBrowser({ loaderData }: Route.ComponentProps) {
  const files = loaderData;
  const { mainViewAtTop } = useShell();
  return (
    <>
      <header
        className={cn(
          "flex h-14 shrink-0 items-center gap-2 top-0 sticky bg-background/70 backdrop-blur-lg border-b transition-colors duration-300",
          mainViewAtTop && "[&:not(:hover)]:border-transparent"
        )}
      >
        <div className="flex flex-1 items-center gap-2 px-3">
          <SidebarTrigger />
          <div className="flex gap-0">
            <Button variant="ghost" size="icon-xs">
              <ChevronLeft />
            </Button>
            <Button variant="ghost" size="icon-xs">
              <ChevronRight />
            </Button>
          </div>
          <Breadcrumb className="flex-1">
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbPage className="line-clamp-1">
                  <span className="flex gap-2">
                    <div className="flex aspect-square size-5 items-center justify-center rounded-md bg-sidebar-primary text-sidebar-primary-foreground">
                      <User className="size-3" />
                    </div>
                    Luke's Workspace
                  </span>
                </BreadcrumbPage>
              </BreadcrumbItem>
              <BreadcrumbSeparator>/</BreadcrumbSeparator>
            </BreadcrumbList>
          </Breadcrumb>
          <div className="flex gap-1">
            <Button variant="secondary" size="sm">
              <LayoutGrid />
            </Button>
            <Button variant="ghost" size="sm">
              <List />
            </Button>
            <Button variant="ghost" size="sm">
              <Columns3 />
            </Button>
            <Button variant="ghost" size="sm">
              <GalleryThumbnails />
            </Button>
          </div>
        </div>
      </header>
      <div className="px-3 pb-3">
        <h2 className="text-muted-foreground font-bold pb-2 select-none">
          Files
        </h2>
        <FileGrid files={files} />
      </div>
    </>
  );
}
