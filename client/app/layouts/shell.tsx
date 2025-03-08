import { createContext, useContext, useRef, useState } from "react";
import { Outlet } from "react-router";
import { AppSidebar } from "~/components/app-sidebar";
import { InspectorSidebar } from "~/components/inspector-sidebar";

import { SidebarInset, SidebarProvider } from "~/components/ui/sidebar";
import { useInspector } from "~/hooks/use-inspector";

const ShellContext = createContext({ mainViewAtTop: false });

export function useShell() {
  return { ...useContext(ShellContext) };
}

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
        <ShellContext.Provider value={{ mainViewAtTop }}>
          <Outlet />
        </ShellContext.Provider>
      </SidebarInset>

      <InspectorSidebar open={isInspectorOpen} />
    </SidebarProvider>
  );
}
