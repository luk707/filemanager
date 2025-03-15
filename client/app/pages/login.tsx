import { getInfo } from "~/api/info";
import type { Route } from "./+types/login";
import { LoginPage } from "~/components/pages/login";

export async function loader() {
  return await getInfo();
}

export default function LoginRoute({ loaderData }: Route.ComponentProps) {
  const { organizationName } = loaderData;
  return <LoginPage organizationName={organizationName} />;
}
