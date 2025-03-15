import { type RouteConfig, layout, route } from "@react-router/dev/routes";

export default [
  route("login", "pages/login.tsx"),
  layout("layouts/shell.tsx", [
    route("files/*", "pages/files.tsx"),
    route("preferences", "pages/preferences.tsx"),
    route("user-management", "pages/user-management.tsx"),
  ]),
] satisfies RouteConfig;
