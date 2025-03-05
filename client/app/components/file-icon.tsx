import {
  AudioLines,
  Binary,
  Braces,
  FileSpreadsheet,
  Image,
  Rotate3D,
  Text,
  Type,
  type LucideProps,
} from "lucide-react";
import type { ComponentType } from "react";
import { cn } from "~/lib/utils";

function getFileIconComponent(
  contentType: string | null
): ComponentType<LucideProps> {
  switch (contentType) {
    default:
      return Binary;
    case "audio/wav":
    case "audio/x-wav":
      return AudioLines;
    case "text/csv":
      return FileSpreadsheet;
    case "image/jpeg":
    case "image/gif":
      return Image;
    case "application/x-tgif":
      return Rotate3D;
    case "application/pdf":
      return Text;
    case "font/ttf":
      return Type;
    case "text/x-python":
      return Braces;
  }
}

function getFileIconColor(contentType: string | null): string {
  switch (contentType) {
    default:
      return "bg-gray-500";
    case "audio/wav":
    case "audio/x-wav":
      return "bg-red-500";
    case "application/pdf":
      return "bg-blue-500";
    case "image/jpeg":
    case "image/gif":
      return "bg-amber-500";
    case "text/x-python":
      return "bg-emerald-500";
    case "application/x-tgif":
      return "bg-purple-500";
  }
}

export interface FileIconProps {
  contentType: string | null;
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
