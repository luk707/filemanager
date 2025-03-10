import { Settings2 } from "lucide-react";
import { Toolbar } from "~/components/toolbar";

export async function action() {
  console.log("HELLO, WORLD!");
}

export default function UserPreferencesPage() {
  return (
    <div className="h-full">
      <Toolbar>
        <div className="flex gap-2 items-center select-none">
          <div className="flex aspect-square size-5 items-center justify-center rounded-md bg-sidebar-primary text-sidebar-primary-foreground">
            <Settings2 className="size-3" />
          </div>
          Preferences
        </div>
      </Toolbar>
      <div className="space-y-12 p-3">
        <div className="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3">
          <div>
            <h2 className="text-base/7 font-semibold">Appearance</h2>
            <p className="mt-1 text-sm/6 text-muted-foreground">
              Adjust the look and feel of the application.
            </p>
          </div>
          <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8">
            <fieldset>
              <legend className="text-sm/6 font-semibold">Theme</legend>
              <p className="mt-1 text-sm/6 text-muted-foreground">
                Change the color theme of the application.
              </p>
            </fieldset>
          </div>
        </div>
      </div>
    </div>
  );
}
