import {
  File,
  FileImage,
  FileMusic,
  FileSpreadsheet,
  type LucideProps,
} from "lucide-react";
import type { ComponentType } from "react";
import { cn } from "~/lib/utils";

interface FileIconComponentAndOverrides {
  Component: ComponentType<LucideProps>;
  overrides?: Partial<LucideProps>;
}

function GetFileIconComponent(
  contentType: string
): FileIconComponentAndOverrides {
  switch (contentType) {
    default:
      return { Component: File };
    case "audio/wav":
      return { Component: FileMusic, overrides: { className: "text-red-600" } };
    case "text/csv":
      return {
        Component: FileSpreadsheet,
        overrides: { className: "text-emerald-600" },
      };
    case "image/jpeg":
      return {
        Component: FileImage,
        overrides: { className: "text-amber-500" },
      };
  }
}

export interface FileIconProps {
  contentType: string;
}

export function FileIcon({
  contentType,
  ...rest
}: FileIconProps & LucideProps) {
  const { Component, overrides } = GetFileIconComponent(contentType);
  const className = cn(overrides?.className, rest.className);
  return <Component {...overrides} {...rest} className={className} />;
}
