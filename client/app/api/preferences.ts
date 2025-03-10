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
