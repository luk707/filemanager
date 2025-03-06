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

type FileIcon =
  | "audio"
  | "ms-excel"
  | "csv"
  | "jpeg"
  | "gif"
  | "obj"
  | "pdf"
  | "font"
  | "python";

const FILE_ICONS: Record<string, FileIcon> = {
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
  "image/gif": "gif",
  "image/jpeg": "jpeg",
  "text/csv": "csv",
  "text/x-python": "python",
};

function getFileIconComponent(contentType: string): ComponentType<LucideProps> {
  const iconType: FileIcon | undefined = FILE_ICONS[contentType];
  switch (iconType) {
    default:
      return Binary;
    case "audio":
      return AudioLines;
    case "csv":
      return FileSpreadsheet;
    case "jpeg":
    case "gif":
      return Image;
    case "obj":
      return Rotate3D;
    case "pdf":
      return Text;
    case "font":
      return Type;
    case "python":
      return Braces;
    case "ms-excel":
      return Table;
  }
}

function getFileIconColor(contentType: string): string {
  const iconType: FileIcon | undefined = FILE_ICONS[contentType];
  switch (iconType) {
    default:
      return "bg-gray-500";
    case "audio":
      return "bg-red-500";
    case "pdf":
      return "bg-blue-500";
    case "jpeg":
    case "gif":
      return "bg-amber-500";
    case "ms-excel":
    case "python":
      return "bg-emerald-500";
    case "obj":
      return "bg-purple-500";
  }
}

export interface FileIconProps {
  contentType: string;
}

export function FileIcon({
  contentType,
  ...rest
}: FileIconProps & LucideProps) {
  const Component = getFileIconComponent(contentType);
  return (
    <div
      className={cn(
        getFileIconColor(contentType),
        "w-6 h-6 flex items-center justify-center rounded-sm shrink-0"
      )}
    >
      <Component size={18} strokeWidth={2.5} color="white" {...rest} />
    </div>
  );
}
