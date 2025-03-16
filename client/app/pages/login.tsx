import { getInfo } from "~/api/info";
import type { Route } from "./+types/login";
import { LoginPage } from "~/components/pages/login";
import { z } from "zod";
import { data, redirect } from "react-router";

const LoginFormSchema = z.object({
  username: z.string(),
  password: z.string(),
});

export async function loader() {
  return await getInfo();
}

export async function action({ request }: Route.ActionArgs) {
  let formData = await request.formData();
  const {
    success,
    data: loginFormData,
    error,
  } = LoginFormSchema.safeParse(Object.fromEntries(formData.entries()));

  if (!success) {
    return data(error, { status: 401 });
  }

  return redirect("/files");
}

export default function LoginRoute({ loaderData }: Route.ComponentProps) {
  const { organizationName } = loaderData;
  return <LoginPage organizationName={organizationName} />;
}
