import { type File } from "~/api/files";
import { FileIcon } from "./file-icon";

export interface FileGridProps {
  files: File[];
}

export function FileGrid({ files }: FileGridProps) {
  return (
    <ul className="w-full grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-2">
      {files.map((file) => (
        <li
          key={file.id}
          className="bg-muted/50 hover:bg-muted rounded-lg p-2 border"
        >
          <div className="flex gap-2 p-2">
            <FileIcon contentType={file.contentType} className="shrink-0" />
            <span className="overflow-ellipsis overflow-hidden whitespace-nowrap select-none">
              {file.name}
            </span>
          </div>
          <div className="aspect-[4/3] bg-white rounded-md" />
        </li>
      ))}
    </ul>
  );
}
