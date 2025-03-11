import { type RouteConfig, layout, route } from "@react-router/dev/routes";

export default [
  layout("layouts/shell.tsx", [
    route("files/*", "pages/files.tsx"),
    route("preferences", "pages/preferences.tsx"),
    route("api/documentation", "pages/api-documentation.tsx"),
  ]),
] satisfies RouteConfig;
