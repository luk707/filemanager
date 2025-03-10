import { createContext, useState } from "react";
import type { z } from "zod";
import { setTheme, type ThemeSchema } from "~/api/preferences";

type ThemeProviderProps = {
  children: React.ReactNode;
  defaultTheme?: z.infer<typeof ThemeSchema>;
  storageKey?: string;
};

type ThemeProviderState = {
  theme: z.infer<typeof ThemeSchema>;
  setTheme: (theme: z.infer<typeof ThemeSchema>) => void;
};

const initialState: ThemeProviderState = {
  theme: "system",
  setTheme: () => null,
};

export const ThemeProviderContext =
  createContext<ThemeProviderState>(initialState);

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "vite-ui-theme",
  ...props
}: ThemeProviderProps) {
  const [theme, setThemeState] = useState<z.infer<typeof ThemeSchema>>(
    () =>
      (localStorage.getItem(storageKey) as z.infer<typeof ThemeSchema>) ||
      defaultTheme
  );

  const value = {
    theme,
    setTheme: (theme: z.infer<typeof ThemeSchema>) => {
      setTheme(theme);
      setThemeState(theme);
    },
  };

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
}
