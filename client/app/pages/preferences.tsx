import { Settings2 } from "lucide-react";
import { Toolbar } from "~/components/toolbar";
import { Label } from "~/components/ui/label";
import { RadioGroup, RadioGroupItem } from "~/components/ui/radio-group";
import type { Route } from "./+types/preferences";
import { preferencesCookie } from "~/cookies.server";
import { PreferencesSchema, ThemeSchema } from "~/api/preferences";
import { data, Form } from "react-router";
import { Button } from "~/components/ui/button";
import { PreferencesSection } from "~/components/preferences-section";
import { PreferencesField } from "~/components/preferences-field";
import { Switch } from "~/components/ui/switch";
import type { z } from "zod";

export async function loader({ request }: Route.LoaderArgs) {
  const cookieHeader = request.headers.get("Cookie");
  const cookie = (await preferencesCookie.parse(cookieHeader)) || {};
  const preferences = PreferencesSchema.parse(cookie);
  return { preferences };
}

export async function action({ request }: Route.ActionArgs) {
  let formData = await request.formData();
  const preferences = PreferencesSchema.parse({
    theme: formData.get("theme"),
    developerAPIDocumentationEnabled:
      formData.get("developer-api-documentation-enabled") === "enabled",
  });
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
          <div className="grid grid-cols-1 gap-x-8 gap-y-10 pb-12 lg:grid-cols-[1fr_2fr]">
            <PreferencesSection
              title="Appearance"
              description="Adjust the look and feel of the application."
            >
              <PreferencesField
                title="Theme"
                description="Change the color theme of the application."
              >
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
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="plum" id="theme-plum" />
                    <Label htmlFor="theme-plum">Plum</Label>
                  </div>
                </RadioGroup>
              </PreferencesField>
            </PreferencesSection>
            <PreferencesSection
              title="Developer"
              description="Customize app features for development purposes."
            >
              <PreferencesField
                title="API Documentation"
                description="Toggle the visibility of the API Documentation tab."
              >
                <div className="flex items-center space-x-2 pt-3">
                  <Switch
                    name="developer-api-documentation-enabled"
                    value="enabled"
                    defaultChecked={
                      preferences.developerAPIDocumentationEnabled
                    }
                    id="airplane-mode"
                  />
                  <Label htmlFor="airplane-mode">
                    Enable API documentation tab
                  </Label>
                </div>
              </PreferencesField>
            </PreferencesSection>
          </div>
          <div>
            <Button type="submit">Update preferences</Button>
          </div>
        </div>
      </div>
    </Form>
  );
}
