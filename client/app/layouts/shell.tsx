import {
  createContext,
  useContext,
  useState,
  type UIEventHandler,
} from "react";
import { Outlet } from "react-router";
import { AppSidebar } from "~/components/app-sidebar";
import { InspectorSidebar } from "~/components/inspector-sidebar";

import { SidebarInset, SidebarProvider } from "~/components/ui/sidebar";
import { useInspector } from "~/hooks/use-inspector";

const ShellContext = createContext({ fixedToTop: true });

export function useShell() {
  return useContext(ShellContext);
}

export default function Shell() {
  const { isOpen: isInspectorOpen } = useInspector();
  const [fixedToTop, setFixedToTop] = useState(true);

  const handleScroll: UIEventHandler<HTMLElement> = (e) => {
    setFixedToTop(e.currentTarget.scrollTop <= 0);
  };

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset
        className="overflow-y-scroll max-h-[calc(100vh-1rem)]"
        onScroll={handleScroll}
      >
        <ShellContext.Provider value={{ fixedToTop }}>
          <Outlet />
        </ShellContext.Provider>
      </SidebarInset>

      <InspectorSidebar open={isInspectorOpen} />
    </SidebarProvider>
  );
}
