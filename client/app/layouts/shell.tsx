import { User } from "lucide-react";
import { useRef, useState } from "react";
import { Outlet } from "react-router";
import { AppSidebar } from "~/components/app-sidebar";
import { InspectorSidebar } from "~/components/inspector-sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "~/components/ui/breadcrumb";
import { Separator } from "~/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar";
import { useInspector } from "~/hooks/use-inspector";
import { cn } from "~/lib/utils";

export default function Shell() {
  const { isOpen: isInspectorOpen } = useInspector();
  const mainViewRef = useRef<HTMLElement>(null);

  const [mainViewAtTop, setMainViewAtTop] = useState(true);
  const handleScroll = () => {
    if (mainViewRef.current) {
      const { scrollTop } = mainViewRef.current;
      setMainViewAtTop(scrollTop === 0);
    }
  };

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset
        ref={mainViewRef}
        className="overflow-y-scroll max-h-[calc(100vh-1rem)]"
        onScroll={handleScroll}
      >
        <header
          className={cn(
            "flex h-14 shrink-0 items-center gap-2 top-0 sticky bg-background/70 backdrop-blur-lg border-b transition-colors",
            mainViewAtTop && "border-transparent"
          )}
        >
          <div className="flex flex-1 items-center gap-2 px-3">
            <SidebarTrigger />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbPage className="line-clamp-1">
                    <span className="flex gap-2">
                      <div className="flex aspect-square size-5 items-center justify-center rounded-md bg-sidebar-primary text-sidebar-primary-foreground">
                        <User className="size-3" />
                      </div>
                      Luke's Workspace
                    </span>
                  </BreadcrumbPage>
                </BreadcrumbItem>
                <BreadcrumbSeparator>/</BreadcrumbSeparator>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        </header>
        <div>
          <Outlet />
        </div>
      </SidebarInset>

      <InspectorSidebar open={isInspectorOpen} />
    </SidebarProvider>
  );
}
