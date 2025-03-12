import { BookOpenText } from "lucide-react";
import { Toolbar } from "~/components/toolbar";
import type { Route } from "./+types/api-documentation";

export async function loader() {
  const data = await fetch(`${import.meta.env.VITE_API_BASE_URL}/openapi.json`);
  return await data.json();
}

export default function APIDocumentation({ loaderData }: Route.ComponentProps) {
  const openapiJson = loaderData;
  return (
    <div>
      <Toolbar>
        <div className="flex gap-2 items-center select-none">
          <div className="flex aspect-square size-5 items-center justify-center rounded-md bg-sidebar-primary text-sidebar-primary-foreground">
            <BookOpenText className="size-3" />
          </div>
          API Documentation
        </div>
      </Toolbar>
      <pre>{JSON.stringify(openapiJson, null, 4)}</pre>
    </div>
  );
}
