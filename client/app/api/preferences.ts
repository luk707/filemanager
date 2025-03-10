import { z } from "zod";
import Cookies from "js-cookie";

// Must not change
export const preferencesCookieName = "__preferences";

export const ThemeSchema = z.union([
  z.literal("dark"),
  z.literal("light"),
  z.literal("system"),
]);

export const PreferencesSchema = z.object({
  theme: ThemeSchema.default("system"),
});

export function getPreferences() {
  const preferencesCookie = Cookies.get(preferencesCookieName);

  try {
    const preferencesData = JSON.parse(atob(preferencesCookie ?? ""));
    return PreferencesSchema.parse(preferencesData);
  } catch {
    return PreferencesSchema.parse({});
  }
}

export function setTheme(theme: z.infer<typeof ThemeSchema>) {
  Cookies.set(
    preferencesCookieName,
    btoa(
      JSON.stringify(
        PreferencesSchema.parse({
          ...getPreferences(),
          theme,
        })
      )
    )
  );
}
