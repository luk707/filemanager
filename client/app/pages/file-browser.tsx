import { FileGrid } from "~/components/file-grid";
import { Button } from "~/components/ui/button";
import { getFiles } from "~/api/files";
import type { Route } from "./+types/file-browser";

export async function loader({}: Route.LoaderArgs) {
  return await getFiles();
}

export async function clientLoader({}: Route.ClientLoaderArgs) {
  return await getFiles();
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
