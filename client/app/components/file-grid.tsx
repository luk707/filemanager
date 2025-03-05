import { type File } from "~/api/files";
import { FileIcon } from "./file-icon";
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
  ContextMenuCheckboxItem,
  ContextMenuRadioGroup,
  ContextMenuLabel,
  ContextMenuRadioItem,
} from "~/components/ui/context-menu";

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
            <ContextMenuItem inset>
              Back
              <ContextMenuShortcut>⌘[</ContextMenuShortcut>
            </ContextMenuItem>
            <ContextMenuItem inset disabled>
              Forward
              <ContextMenuShortcut>⌘]</ContextMenuShortcut>
            </ContextMenuItem>
            <ContextMenuItem inset>
              Reload
              <ContextMenuShortcut>⌘R</ContextMenuShortcut>
            </ContextMenuItem>
            <ContextMenuSub>
              <ContextMenuSubTrigger inset>More Tools</ContextMenuSubTrigger>
              <ContextMenuSubContent className="w-48">
                <ContextMenuItem>
                  Save Page As...
                  <ContextMenuShortcut>⇧⌘S</ContextMenuShortcut>
                </ContextMenuItem>
                <ContextMenuItem>Create Shortcut...</ContextMenuItem>
                <ContextMenuItem>Name Window...</ContextMenuItem>
                <ContextMenuSeparator />
                <ContextMenuItem>Developer Tools</ContextMenuItem>
              </ContextMenuSubContent>
            </ContextMenuSub>
            <ContextMenuSeparator />
            <ContextMenuCheckboxItem checked>
              Show Bookmarks Bar
              <ContextMenuShortcut>⌘⇧B</ContextMenuShortcut>
            </ContextMenuCheckboxItem>
            <ContextMenuCheckboxItem>Show Full URLs</ContextMenuCheckboxItem>
            <ContextMenuSeparator />
            <ContextMenuRadioGroup value="pedro">
              <ContextMenuLabel inset>People</ContextMenuLabel>
              <ContextMenuSeparator />
              <ContextMenuRadioItem value="pedro">
                Pedro Duarte
              </ContextMenuRadioItem>
              <ContextMenuRadioItem value="colm">
                Colm Tuite
              </ContextMenuRadioItem>
            </ContextMenuRadioGroup>
          </ContextMenuContent>
        </ContextMenu>
      ))}
    </ul>
  );
}
