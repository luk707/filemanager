import { Settings2 } from "lucide-react";
import { Toolbar } from "~/components/toolbar";
import { Label } from "~/components/ui/label";
import { RadioGroup, RadioGroupItem } from "~/components/ui/radio-group";
import type { Route } from "./+types/preferences";
import { preferencesCookie } from "~/cookies.server";
import { PreferencesSchema } from "~/api/preferences";
import { data, Form } from "react-router";
import { Button } from "~/components/ui/button";

export async function loader({ request }: Route.LoaderArgs) {
  const cookieHeader = request.headers.get("Cookie");
  const cookie = (await preferencesCookie.parse(cookieHeader)) || {};
  const preferences = PreferencesSchema.parse(cookie);
  return { preferences };
}

export async function action({ request }: Route.ActionArgs) {
  let formData = await request.formData();
  const preferences = PreferencesSchema.parse(
    Object.fromEntries(formData.entries())
  );
  return data(undefined, {
    headers: {
      "Set-Cookie": await preferencesCookie.serialize(preferences),
    },
  });
}

export default function UserPreferencesPage({
  loaderData,
}: Route.ComponentProps) {
  const { preferences } = loaderData;

  return (
    <Form action="/preferences" method="POST">
      <div className="h-full">
        <Toolbar>
          <div className="flex gap-2 items-center select-none">
            <div className="flex aspect-square size-5 items-center justify-center rounded-md bg-sidebar-primary text-sidebar-primary-foreground">
              <Settings2 className="size-3" />
            </div>
            Preferences
          </div>
        </Toolbar>
        <div className="space-y-12 py-3 px-5">
          <div className="grid grid-cols-1 gap-x-8 gap-y-10 border-b pb-12 lg:grid-cols-3">
            <div>
              <h2 className="text-base/7 font-semibold">Appearance</h2>
              <p className="mt-1 text-sm/6 text-muted-foreground">
                Adjust the look and feel of the application.
              </p>
            </div>
            <div className="grid grid-cols-1 gap-x-6 gap-y-8">
              <fieldset>
                <legend className="text-sm/6 font-semibold">Theme</legend>
                <p className="mt-1 text-sm/6 text-muted-foreground">
                  Change the color theme of the application.
                </p>
                <RadioGroup
                  defaultValue={preferences.theme}
                  name="theme"
                  className="pt-3"
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="light" id="theme-light" />
                    <Label htmlFor="theme-light">Light</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="dark" id="theme-dark" />
                    <Label htmlFor="theme-dark">Dark</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="system" id="theme-system" />
                    <Label htmlFor="theme-system">System</Label>
                  </div>
                </RadioGroup>
              </fieldset>
            </div>
          </div>
          <div>
            <Button type="submit">Update preferences</Button>
          </div>
        </div>
      </div>
    </Form>
  );
}
