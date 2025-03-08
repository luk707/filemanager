import {
  AudioLines,
  Binary,
  Braces,
  FileSpreadsheet,
  Image,
  Rotate3D,
  Table,
  Text,
  Type,
  type LucideProps,
} from "lucide-react";
import type { ComponentType } from "react";
import { cn } from "~/lib/utils";

export type FileIcon =
  | "audio"
  | "ms-excel"
  | "csv"
  | "image"
  | "obj"
  | "pdf"
  | "font"
  | "python";

export const FILE_ICONS: Record<string, FileIcon> = {
  "application/pdf": "pdf",
  "application/vnd.ms-excel.addin.macroEnabled.12": "ms-excel",
  "application/vnd.ms-excel.sheet.binary.macroEnabled.12": "ms-excel",
  "application/vnd.ms-excel.sheet.macroEnabled.12": "ms-excel",
  "application/vnd.ms-excel.template.macroEnabled.12": "ms-excel",
  "application/vnd.ms-excel": "ms-excel",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
    "ms-excel",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.template":
    "ms-excel",
  "application/x-tgif": "obj",
  "audio/wav": "audio",
  "audio/x-wav": "audio",
  "font/ttf": "font",
  "image/gif": "image",
  "image/jpeg": "image",
  "text/csv": "csv",
  "text/x-python": "python",
};

const FILE_ICON_COMPONENTS: Record<FileIcon, ComponentType<LucideProps>> = {
  audio: AudioLines,
  csv: FileSpreadsheet,
  image: Image,
  obj: Rotate3D,
  pdf: Text,
  font: Type,
  python: Braces,
  "ms-excel": Table,
};

const FILE_ICON_COLORS: Record<FileIcon, string> = {
  audio: "bg-red-500",
  pdf: "bg-blue-500",
  image: "bg-amber-500",
  "ms-excel": "bg-emerald-500",
  obj: "bg-purple-500",
  python: "bg-emerald-500",
  csv: "bg-emerald-500",
  font: "bg-gray-500",
};

export interface FileIconProps {
  contentType: string;
}

export function FileIcon({
  contentType,
  ...rest
}: FileIconProps & LucideProps) {
  const fileIcon = FILE_ICONS[contentType];
  const Component = FILE_ICON_COMPONENTS[fileIcon] ?? Binary;
  const fileIconColor = FILE_ICON_COLORS[fileIcon] ?? "bg-gray-500";
  return (
    <div
      className={cn(
        fileIconColor,
        "w-6 h-6 flex items-center justify-center rounded-sm shrink-0"
      )}
    >
      <Component size={18} strokeWidth={2.5} color="white" {...rest} />
    </div>
  );
}
