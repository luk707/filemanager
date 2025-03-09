import { DirectorySchema, removeDirectory } from "~/api/files";
import { z } from "zod";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuShortcut,
  ContextMenuSub,
  ContextMenuSubContent,
  ContextMenuSubTrigger,
  ContextMenuTrigger,
  ContextMenuSeparator,
} from "~/components/ui/context-menu";
import {
  FileArchive,
  Files,
  Folder,
  FolderInput,
  FolderOpen,
  Info,
  PencilLine,
  Star,
  Trash2,
} from "lucide-react";
import { Link, useNavigate } from "react-router";
import {
  AlertDialog,
  AlertDialogActionDestructive,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "~/components/ui/alert-dialog";
import { useInspector } from "~/hooks/use-inspector";

export interface DirectoryGridProps {
  directories: z.infer<typeof DirectorySchema>[];
}

export function DirectoryGrid({ directories }: DirectoryGridProps) {
  const { open: openInspector } = useInspector();
  const navigate = useNavigate();
  return (
    <div className="w-full grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-2">
      {directories.map((directory) => (
        <AlertDialog key={directory.name}>
          <ContextMenu>
            <ContextMenuTrigger asChild>
              <Link
                to={`/files/${directory.path}`}
                className="bg-muted/50 hover:bg-muted rounded-lg p-2 border"
              >
                <div className="flex items-center gap-2 p-2">
                  <Folder
                    size={20}
                    className="text-muted-foreground"
                    fill="currentColor"
                  />
                  <span className="overflow-ellipsis overflow-hidden whitespace-nowrap select-none">
                    {directory.name}
                  </span>
                </div>
              </Link>
            </ContextMenuTrigger>
            <ContextMenuContent className="w-64">
              <ContextMenuItem>
                <FileArchive />
                Download archive
              </ContextMenuItem>
              <ContextMenuItem>
                <PencilLine />
                Rename
                <ContextMenuShortcut>⌥⌘E</ContextMenuShortcut>
              </ContextMenuItem>
              <ContextMenuSeparator />
              <ContextMenuSub>
                <ContextMenuSubTrigger>
                  <FolderOpen /> Organize
                </ContextMenuSubTrigger>
                <ContextMenuSubContent className="w-52">
                  <ContextMenuItem>
                    <FolderInput />
                    Move
                    <ContextMenuShortcut>⌥⌘M</ContextMenuShortcut>
                  </ContextMenuItem>
                  <ContextMenuItem>
                    <Star />
                    Add to favorites
                    <ContextMenuShortcut>⌥⌘S</ContextMenuShortcut>
                  </ContextMenuItem>
                </ContextMenuSubContent>
              </ContextMenuSub>
              <ContextMenuItem
                onClick={() => {
                  openInspector();
                }}
              >
                <Info />
                Details
                <ContextMenuShortcut>
                  ⌥V <span className="tracking-normal">then</span> D
                </ContextMenuShortcut>
              </ContextMenuItem>
              <ContextMenuSeparator />
              <AlertDialogTrigger asChild>
                <ContextMenuItem>
                  <Trash2 />
                  Remove folder
                  <ContextMenuShortcut>
                    <span className="tracking-normal">Delete</span>
                  </ContextMenuShortcut>
                </ContextMenuItem>
              </AlertDialogTrigger>
            </ContextMenuContent>
          </ContextMenu>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>
                Are you sure you want to delete "{directory.name}"?
              </AlertDialogTitle>
              <AlertDialogDescription>
                This action cannot be undone. This will permanently delete "
                {directory.name}" and its contents.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogActionDestructive
                onClick={async () => {
                  // TODO: Remove hardcoded workspaceId
                  await removeDirectory("files", directory.name);
                  navigate(".", { replace: true });
                }}
              >
                Delete
              </AlertDialogActionDestructive>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      ))}
    </div>
  );
}
