import { z } from "zod";

// Must not change
export const preferencesCookieName = "__preferences";

export const ThemeSchema = z.union([
  z.literal("dark"),
  z.literal("light"),
  z.literal("system"),
  z.literal("plum"),
]);

export const PreferencesSchema = z.object({
  theme: ThemeSchema.default("system"),
});
