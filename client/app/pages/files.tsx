import { FileGrid } from "~/components/file-grid";
import { createDirectory, stat } from "~/api/files";
import type { Route } from "./+types/files";
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
  FolderPlus,
  GalleryThumbnails,
  LayoutGrid,
  List,
  User,
} from "lucide-react";
import { SidebarTrigger } from "~/components/ui/sidebar";
import { useShell } from "~/layouts/shell";
import { Button } from "~/components/ui/button";
import { DirectoryGrid } from "~/components/directory-grid";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuShortcut,
  ContextMenuTrigger,
} from "~/components/ui/context-menu";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "~/components/ui/alert-dialog";
import { Link, useNavigate } from "react-router";
import { Fragment, useState } from "react";
import { Input } from "~/components/ui/input";
import { Toolbar } from "~/components/toolbar";

export async function loader({ params }: Route.LoaderArgs) {
  const { "*": path } = params;
  // TODO: Remove hardcoded workspaceId
  return await stat("files", path);
}

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  const { "*": path } = params;
  // TODO: Remove hardcoded workspaceId
  return await stat("files", path);
}

export default function FileBrowser({
  loaderData,
  params,
}: Route.ComponentProps) {
  const directoryListings = loaderData;
  const { "*": path } = params;
  const navigate = useNavigate();

  const directories = directoryListings.filter(
    (listing) => listing.type === "directory"
  );
  const files = directoryListings.filter((listing) => listing.type === "file");

  const { fixedToTop } = useShell();
  const [newDirectoryName, setNewDirectoryName] = useState("Untitled folder");
  return (
    <AlertDialog>
      <ContextMenu>
        <ContextMenuTrigger asChild>
          <div className="h-full">
            <Toolbar
              right={
                <>
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
                </>
              }
            >
              <Breadcrumb className="flex-1">
                <BreadcrumbList>
                  <BreadcrumbItem>
                    <BreadcrumbPage className="line-clamp-1">
                      <Link to="/files" className="flex gap-2">
                        <div className="flex aspect-square size-5 items-center justify-center rounded-md bg-sidebar-primary text-sidebar-primary-foreground">
                          <User className="size-3" />
                        </div>
                        Luke's Workspace
                      </Link>
                    </BreadcrumbPage>
                  </BreadcrumbItem>
                  {path.length > 0 &&
                    path.split("/").map((segment, i, arr) => (
                      <Fragment key={i}>
                        <BreadcrumbSeparator>/</BreadcrumbSeparator>
                        {arr.length > i + 1 ? (
                          <BreadcrumbPage>
                            <Link
                              to={`/files/${arr
                                .filter((_, j) => i >= j)
                                .join("/")}`}
                            >
                              <BreadcrumbItem>{segment}</BreadcrumbItem>
                            </Link>
                          </BreadcrumbPage>
                        ) : (
                          <BreadcrumbItem>{segment}</BreadcrumbItem>
                        )}
                      </Fragment>
                    ))}
                </BreadcrumbList>
              </Breadcrumb>
            </Toolbar>
            <div className="p-3 flex flex-col gap-2">
              {directories.length > 0 && (
                <>
                  <h2 className="text-muted-foreground font-bold select-none">
                    Folders
                  </h2>
                  <DirectoryGrid directories={directories} />
                </>
              )}
              {files.length > 0 && (
                <>
                  <h2 className="text-muted-foreground font-bold select-none">
                    Files
                  </h2>
                  <FileGrid files={files} />
                </>
              )}
              {/* TODO: Add empty state UI if there's no content here */}
            </div>
          </div>
        </ContextMenuTrigger>
        <ContextMenuContent className="w-64">
          <AlertDialogTrigger asChild>
            <ContextMenuItem>
              <FolderPlus />
              New folder
              <ContextMenuShortcut>
                ⌃C <span className="tracking-normal">then</span> F
              </ContextMenuShortcut>
            </ContextMenuItem>
          </AlertDialogTrigger>
        </ContextMenuContent>
      </ContextMenu>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>New folder</AlertDialogTitle>
        </AlertDialogHeader>
        <Input
          autoFocus
          value={newDirectoryName}
          onChange={(e) => setNewDirectoryName(e.target.value)}
        />
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={async () => {
              // TODO: Remove hardcoded workspaceId
              await createDirectory("files", `${path}/${newDirectoryName}`);
              navigate(".", { replace: true });
              setNewDirectoryName("Untitled folder");
            }}
          >
            Create
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
