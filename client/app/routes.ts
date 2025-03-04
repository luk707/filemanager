import { type RouteConfig, index, layout } from "@react-router/dev/routes";

export default [
  layout("layouts/shell.tsx", [index("pages/file-browser.tsx")]),
] satisfies RouteConfig;
