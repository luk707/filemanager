import { createCookie } from "react-router";
import { preferencesCookieName } from "~/api/preferences";

export const preferencesCookie = createCookie(preferencesCookieName, {
  maxAge: 604_800, // one week
});
