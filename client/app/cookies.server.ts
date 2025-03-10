import { createCookie } from "react-router";
import { z } from "zod";

export const UserPreferencesSchema = z.object({
  theme: z
    .union([z.literal("dark"), z.literal("light"), z.literal("system")])
    .default("system"),
});

export const userPreferencesCookie = createCookie("user-preferences", {
  maxAge: 604_800, // one week
});
