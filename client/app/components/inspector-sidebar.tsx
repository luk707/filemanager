import type { ComponentProps, CSSProperties } from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarProvider,
} from "~/components/ui/sidebar";
import { cn } from "~/lib/utils";
import { FileIcon } from "./file-icon";
import { Button } from "./ui/button";
import { X } from "lucide-react";
import { useInspector } from "~/hooks/use-inspector";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "~/components/ui/tabs";
import { z } from "zod";
import type { FileSchema } from "~/api/files";
import prettyBytes from "pretty-bytes";
import { format, parseISO } from "date-fns";

interface InspectorSidebarProps {
  open?: boolean;
}

// TODO: Actually pull this from the currently inspected file
const demoFile = {
  name: "CV design.pdf",
  contentType: "application/pdf",
  size: 2287442,
  lastModified: "2025-03-08T17:12:03.116000Z",
} satisfies z.infer<typeof FileSchema>;

export function InspectorSidebar({
  open,
  ...props
}: ComponentProps<typeof Sidebar> & InspectorSidebarProps) {
  const { close } = useInspector();
  return (
    <SidebarProvider
      open={open}
      className={cn(
        "transition-all duration-300",
        open ? "w-(--sidebar-width)" : "w-0"
      )}
      style={
        {
          "--sidebar-width": "20rem",
          "--sidebar-width-mobile": "20rem",
        } as CSSProperties
      }
    >
      <Sidebar
        variant="panel"
        collapsible="offcanvas"
        side="right"
        className="sticky top-0 h-svh"
        {...props}
      >
        <SidebarHeader className="flex flex-row gap-3 px-4 py-3">
          <FileIcon contentType={demoFile.contentType} className="shrink-0" />
          <span className="flex-1 break-all">{demoFile.name}</span>
          <Button
            variant="ghost"
            size="icon-xs"
            className="shrink-0"
            onClick={close}
          >
            <X />
          </Button>
        </SidebarHeader>

        <SidebarContent className="px-3">
          <Tabs defaultValue="details">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="details">Details</TabsTrigger>
              <TabsTrigger value="activity">Activity</TabsTrigger>
            </TabsList>
            <TabsContent value="details" className="flex flex-col gap-4">
              <div className="aspect-[4/3] bg-background rounded-md border" />
              <dl className="flex flex-col gap-1">
                <dt className="text-sm">Type</dt>
                <dd className="text-sm text-muted-foreground pb-1 font-mono">
                  PDF
                </dd>

                <dt className="text-sm">Size</dt>
                <dd className="text-sm text-muted-foreground pb-1 font-mono">
                  {prettyBytes(demoFile.size)}
                </dd>

                <dt className="text-sm">Modified</dt>
                <dd className="text-sm text-muted-foreground pb-1 font-mono">
                  {format(parseISO(demoFile.lastModified), "MMM d, yyyy")}
                </dd>
              </dl>
            </TabsContent>
          </Tabs>
        </SidebarContent>
      </Sidebar>
    </SidebarProvider>
  );
}
