import { FileGrid } from "~/components/file-grid";
import { Button } from "~/components/ui/button";
import { getFiles } from "~/api/files";
import type { Route } from "./+types/file-browser";

export async function loader({}: Route.LoaderArgs) {
  // TODO: Remove hardcoded workspaceId
  return await getFiles("files");
}

export async function clientLoader({}: Route.ClientLoaderArgs) {
  // TODO: Remove hardcoded workspaceId
  return await getFiles("files");
}

export default function FileBrowser({ loaderData }: Route.ComponentProps) {
  const files = loaderData;
  return (
    <>
      <h2 className="text-muted-foreground font-bold pb-2 select-none">
        Files
      </h2>
      <FileGrid files={files} />
    </>
  );
}
