import { type File } from "~/api/files";
import { FileIcon } from "~/components/file-icon";
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
  Download,
  Files,
  FolderInput,
  FolderOpen,
  Info,
  PencilLine,
  Star,
  Trash2,
} from "lucide-react";

export interface FileGridProps {
  files: File[];
}

export function FileGrid({ files }: FileGridProps) {
  return (
    <ul className="w-full grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-2">
      {files.map((file) => (
        <ContextMenu key={file.name}>
          <ContextMenuTrigger asChild>
            <li className="bg-muted/50 hover:bg-muted rounded-lg p-2 border">
              <div className="flex gap-2 p-2">
                <FileIcon contentType={file.contentType} />
                <span className="overflow-ellipsis overflow-hidden whitespace-nowrap select-none">
                  {file.name}
                </span>
              </div>
              <div className="aspect-[4/3] bg-white rounded-md" />
            </li>
          </ContextMenuTrigger>
          <ContextMenuContent className="w-64">
            <ContextMenuItem>
              <Download />
              Download
            </ContextMenuItem>
            <ContextMenuItem>
              <PencilLine />
              Rename
              <ContextMenuShortcut>⌥⌘E</ContextMenuShortcut>
            </ContextMenuItem>
            <ContextMenuItem>
              <Files />
              Make a copy
              <ContextMenuShortcut>⌘R</ContextMenuShortcut>
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
            <ContextMenuItem>
              <Info />
              File details
              <ContextMenuShortcut>
                ⌥V <span className="tracking-normal">then</span> D
              </ContextMenuShortcut>
            </ContextMenuItem>
            <ContextMenuSeparator />
            <ContextMenuItem>
              <Trash2 />
              Remove file
              <ContextMenuShortcut>
                <span className="tracking-normal">Delete</span>
              </ContextMenuShortcut>
            </ContextMenuItem>
          </ContextMenuContent>
        </ContextMenu>
      ))}
    </ul>
  );
}
